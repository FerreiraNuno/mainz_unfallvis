from dash import Dash, dcc, html, Input, Output, no_update
import plotly.express as px
import pandas as pd
import consts as CONSTS
from config import *
from datetime import datetime
import dash_bootstrap_components as dbc

# Create Dash app
app = Dash(__name__, suppress_callback_exceptions=True)

# Load data
accidents_data = pd.read_csv("./data/Verkehrsunfalldaten.csv", delimiter=";", decimal=",")


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
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return map_fig


@app.callback(
    Output("map", "figure"),
    Input("year_range_slider", "marks"),
    Input("year_range_slider", "value"),
    Input("highlighting_dropdown", "value"),
)
def update_map(marks_dict, values, highlighting_dropdown):
    if None not in (marks_dict, values):
        marks_dict = dict(marks_dict)
        start = datetime.strptime(
            marks_dict.get(str(values[0]))["label"], "%m-%Y"
        )
        end = datetime.strptime(marks_dict.get(str(values[1]))["label"], "%m-%Y")
        filtered_data = accidents_data.loc[
            lambda x: (
                (x[CONSTS.CUSTOM_DATETIME] >= start)
                & (x[CONSTS.CUSTOM_DATETIME] <= end)
            )
        ]
        return prepare_map(highlighting_dropdown, filtered_data)
    return prepare_map(highlighting_dropdown, accidents_data)


@app.callback(
    Output("bar-chart-predicted-accident-class", "figure"), 
    Input("map", "clickData")
)
def update_bar_chart(click_data):
    if click_data:
        hovered_lat = click_data["points"][0]["lat"]
        hovered_lon = click_data["points"][0]["lon"]

        point_data = accidents_data.loc[
            (accidents_data[CONSTS.LATITUDE] == hovered_lat)
            & (accidents_data[CONSTS.LONGITUDE] == hovered_lon)
        ]

        if not point_data.empty:
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

            fig = px.bar(
                bar_data,
                x="Unfallklasse Vorhersage",
                y="Value",
                title="Vorhersage nach Unfallklasse",
            )
            fig.update_yaxes(title_text="Berechnete Wahrscheinlichkeit in %")
            fig.update_traces(marker_color=["red", "orange", "green"])
            return fig

    return no_update


@app.callback(
    Output("bar-chart-accident-participants", "figure"), 
    Input("map", "clickData")
)
def update_accident_participants_bar_chart(click_data):
    if click_data:
        hovered_lat = click_data["points"][0]["lat"]
        hovered_lon = click_data["points"][0]["lon"]

        point_data = accidents_data.loc[
            (accidents_data[CONSTS.LATITUDE] == hovered_lat)
            & (accidents_data[CONSTS.LONGITUDE] == hovered_lon)
        ]

        if not point_data.empty:
            bar_data = pd.DataFrame(
                {
                    "Beteiligte": ["IstRad", "IstPKW", "IstFuss", "IstKrad", "IstSonstig"],
                    "Value": [
                        point_data[CONSTS.ISTFUSS].values[0],
                        point_data[CONSTS.ISTKRAD].values[0],
                        point_data[CONSTS.ISTPKW].values[0],
                        point_data[CONSTS.ISTRAD].values[0],
                        point_data[CONSTS.ISTSONSTIG].values[0],
                    ],
                }
            )

            bar_data["Color"] = bar_data["Value"].apply(
                lambda x: "darkblue" if x == 1 else "lightgray"
            )

            fig = px.bar(
                bar_data,
                x="Beteiligte",
                y="Value",
                title="Unfallbeteiligte",
            )

            fig.update_traces(
                marker_color=bar_data["Color"],
                textposition="none",
            )
            fig.update_layout(
                yaxis=dict(
                    tickmode="array",
                    tickvals=[0, 1],
                    ticktext=["Unbeteiligt", "Beteiligt"],
                ),
                height=300,
            )

            return fig

    return no_update



def generateMonthAndYearMarks(df):
    start = str(df[CONSTS.JAHR].min()) + "-" + str(df[CONSTS.MONAT].min()) + "-" + "1"
    end = str(df[CONSTS.JAHR].max()) + "-" + str(df[CONSTS.MONAT].max()) + "-" + "1"
    month_year_range = pd.date_range(
        start=start, end=end, freq="QS"
    )

    return {
        each: {"label": str(date), "style": {"transform": "rotate(45deg)"}}
        for each, date in enumerate(month_year_range.unique().strftime("%m-%Y"))
    }



# Overview-Tab ------------------------------------------------------------------------------------------------------------------------
@app.callback(
    Output("overview-graph-container", "children"),  # Dynamischer Platzhalter
    Input("overview-selection", "value"),
)
def update_overview_graph(selected_chart):
    if selected_chart == "bar-chart-accidents-overview":
        # Gruppieren der Daten nach Unfallklasse
        data_by_class = accidents_data.groupby(CONSTS.UNFALLKLASSE_WAHR).size().reset_index(name="Anzahl")
        
        # Mapping für die Labels
        order_map = {"2": "Leichtverletzt", "1": "Schwerverletzt", "0": "Tödlicher Ausgang"}
        data_by_class[CONSTS.UNFALLKLASSE_WAHR] = data_by_class[CONSTS.UNFALLKLASSE_WAHR].map(order_map)
        data_by_class[CONSTS.UNFALLKLASSE_WAHR] = pd.Categorical(
            data_by_class[CONSTS.UNFALLKLASSE_WAHR],
            categories=["Leichtverletzt", "Schwerverletzt", "Tödlicher Ausgang"],
            ordered=True,
        )
        
        # Erstellung des Balkendiagramms
        fig = px.bar(
            data_by_class,
            x=CONSTS.UNFALLKLASSE_WAHR,
            y="Anzahl",
            title="Anzahl der Unfälle nach Unfallklasse",
            color=CONSTS.UNFALLKLASSE_WAHR,
            color_discrete_map={
                "Leichtverletzt": "green",
                "Schwerverletzt": "orange",
                "Tödlicher Ausgang": "red",
            },
        )
        
        fig.update_layout(
            xaxis_title="Unfallklasse",
            yaxis_title="Anzahl der Unfälle",
            showlegend=False,
        )
        return dcc.Graph(figure=fig)

    elif selected_chart == "bar-chart-accidents-years-overview":
        # Gruppieren der Daten nach Jahr und Unfallklasse
        data_by_year = accidents_data.groupby([CONSTS.JAHR, CONSTS.UNFALLKLASSE_WAHR]).size().reset_index(name="Anzahl")
        data_by_year = data_by_year.loc[data_by_year[CONSTS.JAHR].between(2016, 2022)]
        
        # Mapping für die Reihenfolge und Labels
        order_map = {"2": "Leichtverletzt", "1": "Schwerverletzt", "0": "Tödlicher Ausgang"}
        data_by_year[CONSTS.UNFALLKLASSE_WAHR] = data_by_year[CONSTS.UNFALLKLASSE_WAHR].map(order_map)
        data_by_year[CONSTS.UNFALLKLASSE_WAHR] = pd.Categorical(
            data_by_year[CONSTS.UNFALLKLASSE_WAHR],
            categories=["Leichtverletzt", "Schwerverletzt", "Tödlicher Ausgang"],
            ordered=True,
        )
        
        # Erstellung des Balkendiagramms
        bar_fig = px.bar(
            data_by_year,
            x=CONSTS.JAHR,
            y="Anzahl",
            color=CONSTS.UNFALLKLASSE_WAHR,
            title="Unfälle pro Jahr nach Unfallklasse - Balkendiagramm",
            color_discrete_map={
                "Leichtverletzt": "green",
                "Schwerverletzt": "orange",
                "Tödlicher Ausgang": "red",
            },
            barmode="group",
        )
        bar_fig.update_layout(
            xaxis_title="Jahr",
            yaxis_title="Anzahl der Unfälle",
            legend_title="Unfallklasse",
        )
        
        # Erstellung des Liniendiagramms
        line_fig = px.line(
            data_by_year,
            x=CONSTS.JAHR,
            y="Anzahl",
            color=CONSTS.UNFALLKLASSE_WAHR,
            title="Unfälle pro Jahr nach Unfallklasse - Liniendiagramm",
            color_discrete_map={
                "Leichtverletzt": "green",
                "Schwerverletzt": "orange",
                "Tödlicher Ausgang": "red",
            },
        )
        line_fig.update_layout(
            xaxis_title="Jahr",
            yaxis_title="Anzahl der Unfälle",
            legend_title="Unfallklasse",
        )
        
        return html.Div([
            dcc.Graph(figure=bar_fig),
            dcc.Graph(figure=line_fig),
        ])

    elif selected_chart == "line-chart-accidents-date-overview":
        # Gruppieren der Daten nach Datum und Unfallklasse
        data_by_date = accidents_data.groupby([CONSTS.CUSTOM_DATETIME, CONSTS.UNFALLKLASSE_WAHR]).size().reset_index(name="Anzahl")
        
        # Mapping für die Labels
        order_map = {"2": "Leichtverletzt", "1": "Schwerverletzt", "0": "Tödlicher Ausgang"}
        data_by_date[CONSTS.UNFALLKLASSE_WAHR] = data_by_date[CONSTS.UNFALLKLASSE_WAHR].map(order_map)
        data_by_date[CONSTS.UNFALLKLASSE_WAHR] = pd.Categorical(
            data_by_date[CONSTS.UNFALLKLASSE_WAHR],
            categories=["Leichtverletzt", "Schwerverletzt", "Tödlicher Ausgang"],
            ordered=True,
        )
        
        # Erstellung des Balkendiagramms
        bar_fig = px.bar(
            data_by_date,
            x=CONSTS.CUSTOM_DATETIME,
            y="Anzahl",
            color=CONSTS.UNFALLKLASSE_WAHR,
            title="Unfälle über die Zeit nach Unfallklasse - Balkendiagramm",
            color_discrete_map={
                "Leichtverletzt": "green",
                "Schwerverletzt": "orange",
                "Tödlicher Ausgang": "red",
            },
        )
        bar_fig.update_layout(
            xaxis_title="Datum",
            yaxis_title="Anzahl der Unfälle",
            legend_title="Unfallklasse",
            xaxis=dict(tickformat="%Y-%m-%d"),  # Format der Datumsanzeige
        )
        
        # Erstellung des Liniendiagramms
        line_fig = px.line(
            data_by_date,
            x=CONSTS.CUSTOM_DATETIME,
            y="Anzahl",
            color=CONSTS.UNFALLKLASSE_WAHR,
            title="Unfälle über die Zeit nach Unfallklasse - Liniendiagramm",
            color_discrete_map={
                "Leichtverletzt": "green",
                "Schwerverletzt": "orange",
                "Tödlicher Ausgang": "red",
            },
        )
        line_fig.update_layout(
            xaxis_title="Datum",
            yaxis_title="Anzahl der Unfälle",
            legend_title="Unfallklasse",
            xaxis=dict(tickformat="%Y-%m-%d"),
        )
        
        return html.Div([
            dcc.Graph(figure=bar_fig),
            dcc.Graph(figure=line_fig),
        ])

    return html.Div("Bitte eine valide Option auswählen.")  # Fallback



# Tab-----------------------------------------------------------------------------------------------------------------------------------
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value"),
)
def render_tab_content(tab_value):
    if tab_value == "ueberblick":
        return html.Div(
            [
                # Auswahl für den Nutzer
                html.Div(
                    dcc.RadioItems(
                        id="overview-selection",
                        options=[
                            {"label": "Unfallübersicht", "value": "bar-chart-accidents-overview"},
                            {"label": "Unfälle nach Jahr", "value": "bar-chart-accidents-years-overview"},
                            {"label": "Unfälle nach Datum", "value": "line-chart-accidents-date-overview"},
                        ],
                        value="bar-chart-accidents-overview",  # Standardwert
                        labelStyle={"display": "inline-block", "margin-right": "15px"},
                    ),
                    style={"margin-bottom": "20px"},
                ),
                 html.Div(id="overview-graph-container"),  # Platzhalter für das Diagramm
            ]
        )
    elif tab_value == "erkunden":
        marksMonthYear = generateMonthAndYearMarks(accidents_data)

        return html.Div(
            [
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
                                    )
                                ),
                                html.Div(
                                    dcc.Graph(
                                        id="map",
                                        figure=prepare_map(
                                            CONSTS.UNFALLKLASSE_WAHR, accidents_data
                                        ),
                                        config={"scrollZoom": True},
                                    ),
                                ),
                                html.Div(
                                    dcc.RangeSlider(
                                        id="year_range_slider",
                                        min=0,
                                        max=len(marksMonthYear) - 1,
                                        step=1,
                                        marks=marksMonthYear,
                                        pushable=1,
                                    )
                                ),
                            ],
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
                                            dcc.Graph(
                                                id="bar-chart-accident-participants"
                                            ),
                                        )
                                    )
                                ),
                            ],
                        ),
                    ],
                )
            ]
        )


def main():
    app.layout = html.Div(
        [
            html.H3("Unfall-Dashboard"),
            dcc.Tabs(
                id="tabs",
                value="erkunden",
                children=[
                    dcc.Tab(label="Überblick", value="ueberblick"),
                    dcc.Tab(label="Erkunden", value="erkunden"),
                ],
            ),
            html.Div(id="tab-content"),
        ]
    )
    app.run_server(debug=True, port=8081)


if __name__ == "__main__":
    init()
    main()
