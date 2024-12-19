from dash import no_update
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from dash import html, dcc, no_update
import dash_bootstrap_components as dbc
import consts as CONSTS
import plotly.express as px
from config import *


def render_map_tab(marks_dict, accidents_data, date_range_monthly):
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
                                ),
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
                            ],
                                className="hstack gap-3"
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
                    ),
                    dbc.Col(
                        [
                            dbc.Col(
                                [
                                    html.Div(
                                        dcc.Graph(
                                            id="pairplot-shap-values",
                                            config={"displayModeBar": False},
                                            style={"height": "400px"}
                                        )
                                    ),
                                ]
                            ),

                            html.Div(
                                dcc.Graph(
                                    id="bar-chart-predicted-accident-class",
                                    config={"displayModeBar": False},
                                    # Adjust as needed for consistent sizing
                                    style={"height": "400px"}
                                )
                            ),
                        ]
                    ),


                ],
                style={"alignItems": "end"}
            )
        ]
    )


def prepare_map(attr_to_color_by, data):
    # Add scatter map with coordinates of accidents
    map_fig = px.scatter_mapbox(
        data,
        lat=CONSTS.LATITUDE,
        lon=CONSTS.LONGITUDE,
        hover_name=CONSTS.STADTTEIL,
        hover_data=[
            CONSTS.UNFALLKLASSE_BESTIMMT,
            CONSTS.STRASSENVERHAELTNISSE,
            CONSTS.STRASSENART,
            CONSTS.LICHTVERHAELTNISSE,
            CONSTS.UNFALLTYP,
        ],
        custom_data=[data.index],  # Pass the DataFrame index as custom data
        zoom=12,
        color=attr_to_color_by,
        color_discrete_map=customColoringMap.get(attr_to_color_by)
    )
    map_fig.update_layout(
        mapbox_style="https://tiles-eu.stadiamaps.com/styles/alidade_smooth_dark.json",
        legend=dict(orientation="h", yanchor="bottom",
                    y=1.02, xanchor="right", x=1),
        height=700,
        width=800,
        margin={"l": 10, "r": 0, "t": 0, "b": 0},  # Remove all margins
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


def update_map(values, highlighting_dropdown, participants_checklist, accidents_data, date_range_monthly):
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


def update_particpants_checklist(click_data, accidents_data):
    if click_data:
        hovered_lat = click_data["points"][0]["lat"]
        hovered_lon = click_data["points"][0]["lon"]

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


def update_bar_chart(click_data, accidents_data):
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


def update_scatter_plot(click_data, accidents_data):
    if click_data:
        hovered_lat = click_data["points"][0]["lat"]
        hovered_lon = click_data["points"][0]["lon"]

        # Filtern der Daten für den ausgewählten Punkt
        point_data = accidents_data.loc[
            (accidents_data[CONSTS.LATITUDE] == hovered_lat)
            & (accidents_data[CONSTS.LONGITUDE] == hovered_lon)
        ]

        if not point_data.empty:
            # Daten für den Scatterplot vorbereiten
            scatter_data = pd.DataFrame(
                {
                    "Feature": [
                        "IstRad",
                        "IstPKW",
                        "IstFuss",
                        "IstKrad",
                        "IstSonstig",
                        "TagKategorie",
                        "Monat",
                        "Stunde",
                        "Unfallart",
                        "Unfalltyp",
                        "Lichtverhältnisse",
                        "Straßenverhältnisse",
                        "Straßenart",
                    ],
                    "SHAP-Wert": [
                        point_data[CONSTS.SHAP_0_ISTRAD].values[0],
                        point_data[CONSTS.SHAP_0_ISTPKW].values[0],
                        point_data[CONSTS.SHAP_0_ISTFUSS].values[0],
                        point_data[CONSTS.SHAP_0_ISTKRAD].values[0],
                        point_data[CONSTS.SHAP_0_ISTSONSTIG].values[0],
                        point_data[CONSTS.SHAP_0_TAGKATEGORIE].values[0],
                        point_data[CONSTS.SHAP_0_MONAT].values[0],
                        point_data[CONSTS.SHAP_0_STUNDE].values[0],
                        point_data[CONSTS.SHAP_0_UNFALLART].values[0],
                        point_data[CONSTS.SHAP_0_UNFALLTYP].values[0],
                        point_data[CONSTS.SHAP_0_LICHTVERHAELTNISSE].values[0],
                        point_data[CONSTS.SHAP_0_STRASSENVERHAELTNISSE].values[0],
                        point_data[CONSTS.SHAP_0_STRASSENART].values[0],
                    ],
                }
            )

            # Scatterplot erstellen
            fig = px.scatter(
                scatter_data,
                x="Feature",
                y="SHAP-Wert",
                title="Einfluss der Features auf die Vorhersage",
            )

            fig.update_yaxes(title_text="SHAP-Wert")
            fig.update_xaxes(title_text="Feature")
            fig.update_traces(marker=dict(size=10, color="blue"))

            return fig
    return no_update
