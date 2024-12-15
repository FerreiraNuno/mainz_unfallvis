from dash import Dash, dcc, html, Input, Output, no_update
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import consts as CONSTS
from config import *
from datetime import datetime

import dash_bootstrap_components as dbc

# Create Dash app
app = Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])


# Load data
accidents_data = pd.read_csv("./data/Verkehrsunfalldaten.csv", delimiter=";", decimal=",")

def generateDateRangeByMinAndMaxDate(df):
    start = str(df[CONSTS.JAHR].min()) + "-" + str(df[CONSTS.MONAT].min()) + "-" + "1"
    end = str(df[CONSTS.JAHR].max()) + "-" + str(df[CONSTS.MONAT].max()) + "-" + "1"
    month_year_range = pd.date_range(
        start=start, end=end, freq="MS"
    )  # MS DateOffset Monthly Starting

    return {
        each: {"label": str(date), "style": {'transform': 'rotate(90deg)'}}
        for each, date in enumerate(month_year_range.unique().strftime("%m.%Y"))
    }

date_range_monthly = generateDateRangeByMinAndMaxDate(accidents_data)

def init():
    # Prepare data
    accidents_data[CONSTS.CUSTOM_DATETIME] = pd.to_datetime(
        {
            "year": accidents_data[CONSTS.JAHR],
            "month": accidents_data[CONSTS.MONAT],
            "day": 1,
        }
    )  # prepare datetime column
    accidents_data[CONSTS.UNFALLKLASSE_WAHR] = accidents_data[
        CONSTS.UNFALLKLASSE_WAHR
    ].astype(str)
    accidents_data[CONSTS.UNFALLART] = accidents_data[CONSTS.UNFALLART].astype(str)
    accidents_data[CONSTS.UNFALLTYP] = accidents_data[CONSTS.UNFALLTYP].astype(str)
    accidents_data[CONSTS.LICHTVERHAELTNISSE] = accidents_data[
        CONSTS.LICHTVERHAELTNISSE
    ].astype(str)
    accidents_data[CONSTS.STRASSENVERHAELTNISSE] = accidents_data[
        CONSTS.STRASSENVERHAELTNISSE
    ].astype(str)
    accidents_data[CONSTS.STRASSENART] = accidents_data[CONSTS.STRASSENART].astype(str)
    accidents_data[CONSTS.TAGKATEGORIE] = accidents_data[CONSTS.TAGKATEGORIE].astype(str)


def prepare_map(attr_to_color_by, data):
    # Add scatter map with coordinates of accidents
    map_fig = px.scatter_mapbox(
        data,
        lat=CONSTS.LATITUDE,
        lon=CONSTS.LONGITUDE,
        hover_name=CONSTS.STADTTEIL,
        hover_data=[
            CONSTS.JAHR,
            CONSTS.UNFALLKLASSE_BESTIMMT,
            CONSTS.STRASSENVERHAELTNISSE,
            CONSTS.STRASSENART,
            CONSTS.UNSICHERHEITS_SCORE,
            CONSTS.LICHTVERHAELTNISSE,
            CONSTS.UNFALLTYP,
        ],
        custom_data=[data.index],  # Pass the DataFrame index as custom data
        zoom=12,
        color=attr_to_color_by,
        color_discrete_sequence=customColoringMap.get(attr_to_color_by),
        color_discrete_map={
            "0": "red",
            "1": "orange",
            "2": "green",
        },
    )
    map_fig.update_layout(
        mapbox_style="https://tiles-eu.stadiamaps.com/styles/alidade_smooth_dark.json",
        #autosize=False, width=800, height=800, margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    # Rewrite Labels
    map_fig.for_each_trace(
        lambda trace: (
            trace.update(name=rewriteDict.get(attr_to_color_by)[trace.name])
            if trace.name in rewriteDict.get(attr_to_color_by)
            else None
        )
    )
    return map_fig


@app.callback(
    Output("map", "figure"),
    Input("year_range_slider", "value"),
    Input("highlighting_dropdown", "value"),
    Input("participants_checklist", "value")
)
def update_map(values, highlighting_dropdown, participants_checklist):
    filtered_data = accidents_data
    if values is not None:
        marks_dict = dict(date_range_monthly)
        start = datetime.strptime(
            marks_dict.get(values[0])["label"], "%m.%Y"
        )  # create datetime objects to compare against
        end = datetime.strptime(marks_dict.get(values[1])["label"], "%m.%Y")
        filtered_data = accidents_data.loc[
            lambda x: (
                (x[CONSTS.CUSTOM_DATETIME] >= start)
                & (x[CONSTS.CUSTOM_DATETIME] <= end)
            )
        ]
    if participants_checklist is not None:
        for participant in participants_checklist:
            filtered_data = filtered_data.loc[
                lambda x: (
                (x[participant] == 1)
            )]
    return prepare_map(highlighting_dropdown, filtered_data)


@app.callback(
    Output("bar-chart-predicted-accident-class", "figure"), 
    Input("map", "clickData")
)
def update_bar_chart(click_data):
    if click_data:
        # Extract latitude and longitude from hoverData
        hovered_lat = click_data["points"][0]["lat"]
        hovered_lon = click_data["points"][0]["lon"]

        # Filter the dataset to find the corresponding row
        point_data = accidents_data.loc[
            (accidents_data[CONSTS.LATITUDE] == hovered_lat)
            & (accidents_data[CONSTS.LONGITUDE] == hovered_lon)
        ]

        if not point_data.empty:
            # Prepare data for the bar chart
            bar_data = pd.DataFrame(
                {
                    "Unfallklasse Vorhersage": [
                        "Tödlicher Ausgang",
                        "Schwerverletzte",
                        "Leichtverletzte",
                    ],
                    "Value": [
                        point_data[CONSTS.WAHRSCHEINLICHKEIT_KLASSE_0].values[0],
                        point_data[CONSTS.WAHRSCHEINLICHKEIT_KLASSE_1].values[0],
                        point_data[CONSTS.WAHRSCHEINLICHKEIT_KLASSE_2].values[0],
                    ],
                }
            )

            # Create bar chart
            fig = px.bar(
                bar_data,
                x="Unfallklasse Vorhersage",
                y="Value",
                title="Vorhersage nach Unfallklasse",
            )
            fig.update_yaxes(title_text="Berechnete Wahrscheinlichkeit in %")
            fig.update_traces(marker_color=["red", "orange", "green"])
            #fig.update_layout(height=800)
            return fig

    # Default empty figure
    return no_update
    #return go.Figure()

@app.callback(
    Output("participants_view_checklist", "value"), 
    Input("map", "clickData")
)
def update_particpants_checklist(click_data):
    if click_data:
        # Extract latitude and longitude from hoverData
        hovered_lat = click_data["points"][0]["lat"]
        hovered_lon = click_data["points"][0]["lon"]

        # Filter the dataset to find the corresponding row
        point_data = accidents_data.loc[
            (accidents_data[CONSTS.LATITUDE] == hovered_lat)
            & (accidents_data[CONSTS.LONGITUDE] == hovered_lon)
        ]

        if not point_data.empty:
            to_select = list()
            if point_data[CONSTS.ISTFUSS].values[0] == 1:
                to_select.append(CONSTS.ISTFUSS)
            if point_data[CONSTS.ISTKRAD].values[0] == 1:
                to_select.append(CONSTS.ISTKRAD)
            if point_data[CONSTS.ISTPKW].values[0] == 1:
                to_select.append(CONSTS.ISTPKW)
            if point_data[CONSTS.ISTRAD].values[0] == 1:
                to_select.append(CONSTS.ISTRAD)
            if point_data[CONSTS.ISTSONSTIG].values[0] == 1:
                to_select.append(CONSTS.ISTSONSTIG)
            return to_select

    # Default empty figure
    return []

def prepare_marks():
    marks_dict = {key: value for key, value in date_range_monthly.items() if key % 3 == 0}
    last_key = list(date_range_monthly.keys())[-1]
    marks_dict[last_key] = date_range_monthly.get(last_key)
    return marks_dict

def main():
    marks_dict = prepare_marks()
    # Set Dash layout for displaying the map and the bar chart
    stack = html.Div(
        [
            html.H3("Unfall-Dashboard"),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                dcc.Dropdown(
                                    highlighting_dropdown,
                                    id="highlighting_dropdown",
                                    searchable=False,
                                    value=highlighting_dropdown[0],
                                ),
                            ),
                            dbc.Row([
                                dbc.Col(
                                        html.Div(
                                            dcc.Checklist(
                                                participants_checklist,
                                                id="participants_checklist",
                                                value=[],
                                                inline=True,
                                            )
                                        ),
                                    ),
                                dbc.Col(
                                        html.Div(
                                            dcc.Checklist(
                                                participants_view_checklist,
                                                id="participants_view_checklist",
                                                value=[],
                                                inline=True,
                                            )
                                        ),
                                )   
                            ], 
                            className="hstack gap-3"
                            ),
                            html.Div(
                                dcc.Graph(
                                    id="map",
                                    figure=prepare_map(
                                        CONSTS.UNFALLKLASSE_WAHR, accidents_data
                                    ),
                                    config={"scrollZoom": True},
                                ),
                                style={
                                    # TODO
                                },
                            ),
                            html.Div(
                                dcc.RangeSlider(
                                    id="year_range_slider",
                                    min=0,
                                    max=len(date_range_monthly) - 1,
                                    step=1,
                                    marks=marks_dict,
                                    pushable=1
                                )
                            ),
                        ],
                        style={
                            # TODO
                        },
                    ),
                    dbc.Col(
                        [
                            dbc.Row(
                                dbc.Col(
                                    html.Div(
                                        dcc.Graph(
                                            id="bar-chart-predicted-accident-class"
                                        )
                                    ),
                                )
                            ),
                            dbc.Row(
                                dbc.Col(
                                    html.Div(
                                    ),
                                )
                            ),
                        ],
                        style={},  # todo
                    ),
                ],
                style={"align-items": "end"},
            ),
        ]
    )
    app.layout = dbc.Container(stack)
    app.run_server(debug=True, port=8081)


if __name__ == "__main__":
    init()
    main()
