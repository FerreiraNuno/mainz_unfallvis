from dash import no_update
from datetime import datetime
import pandas as pd
import plotly.express as px
from dash import html, dcc, no_update
import dash_bootstrap_components as dbc
import consts as CONSTS
import plotly.express as px
from config import *
import dash_daq as daq

theme_dropdown = dcc.Dropdown(
    id="theme-dropdown",
    options=[
        {"label": "Normal", "value": "normal"},
        {"label": "Protanopia", "value": "protanopia"},
        {"label": "Tritanopia", "value": "tritanopia"},
    ],
    value="normal",
    clearable=False,
    style={"marginRight": "10px", "fontWeight": "bold",
           "width": "200px", "color": "black"}
)

def render_map_tab(marks_dict, accidents_data, date_range_monthly):
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [   
                            dbc.Row([
                                dbc.Col(
                                    html.Div(
                                        dcc.Dropdown(
                                            highlighting_dropdown,
                                            id="highlighting_dropdown",
                                            searchable=False,
                                            clearable=False,
                                            value=highlighting_dropdown[0],
                                        ),
                                        style={
                                            "width": "90%", 
                                            "margin": "0 auto", 
                                            "padding": "10px",  
                                        }),
                                    ), 
                                dbc.Col(
                                    html.Div([
                                            daq.ToggleSwitch(
                                                    id="toggle-map-theme_bright",
                                                    label=['Dark', 'Bright'],
                                                    value=False,
                                                    style={"display": "flex", "align-items": "center"}
                                                    ),
                                        ]),
                                        width=3
                                ), 
                            ],
                            className="hstack gap-1"
                            ),
                            dbc.Row([
                                dbc.Col(
                                   html.Div(
                                        dcc.Graph(
                                            id="map",
                                            figure=prepare_map(
                                                CONSTS.UNFALLKLASSE_WAHR, accidents_data
                                            ),
                                            config={
                                                "scrollZoom": True,
                                                "displayModeBar": False,
                                                "displaylogo": False,
                                                "responsive": True
                                            },
                                        ),
                                        style={
                                            "width": "100%",
                                            "justify-content": "center",
                                            "align-items": "center",
                                        },
                                    ),
                                ),
                            ],
                                className="hstack gap-3"
                            ),
                            dbc.Row([
                                dbc.Col(
                                    html.Div(
                                        dcc.Checklist(
                                            participants_checklist,
                                            id="participants_checklist",
                                            value=[],
                                            inline=True,
                                        ),
                                        style={
                                            "display": "flex",
                                            "justify-content": "center",
                                            "align-items": "center",
                                        }
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
                                ),
                                style={
                                    "margin-bottom": "20px"  # Adds space below the slider
                                }
                            ),
                        ],
                    ),
                    dbc.Col(
                        [   
                            html.Div([
                                html.Div("Farbmodus:", style={"display": "inline-block",
                                                            "color": "gray"}),
                                theme_dropdown
                            ], style={"display": "flex", "flexDirection": "row", "alignItems": "baseline", "gap": "20px", "padding":"10px"}),
                            html.Div(id="details-row")
                        ],
                    ),
                ],
                
            ),

            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                dcc.Graph(
                                    id="pairplot-shap-values",
                                    config={"displayModeBar": False},
                                    style={"height": "400px", "width": "600px"}
                                ),
                                className="d-flex justify-content-center align-items-center"
                            ),
                        ]
                    ),

                    dbc.Col(
                        [
                            html.Div(
                                dcc.Graph(
                                    id="bar-chart-predicted-accident-class",
                                    config={"displayModeBar": False},
                                    # Adjust as needed for consistent sizing
                                    style={"height": "400px", "width": "700px"}
                                ),
                                className="d-flex justify-content-center align-items-center"
                            ),
                        ]
                    ),

                    dbc.Col(
                        [
                            html.Div(
                                dcc.Graph(
                                    id="uncertainty-graph",
                                    config={"displayModeBar": False},
                                    # Adjust as needed for consistent sizing
                                    style={"height": "400px", "width": "350px"}
                                ),
                                className="d-flex justify-content-center align-items-center"
                            ),
                        ]
                    ),

                ]
            ),
        ]
    )


def prepare_map(attr_to_color_by, data, theme="normal", selected_bright_map_theme=False):
    if not selected_bright_map_theme:
        map_style = "https://tiles-eu.stadiamaps.com/styles/alidade_smooth_dark.json"
    else:
        map_style = "https://tiles-eu.stadiamaps.com/styles/alidade_smooth.json"
    map_fig = px.scatter_mapbox(
        data,
        lat=CONSTS.LATITUDE,
        lon=CONSTS.LONGITUDE,
        hover_name=CONSTS.STADTTEIL,
        hover_data=[
        ],
        custom_data=[data.index],
        zoom=12,
        color=attr_to_color_by,
        color_discrete_map=customColoringMap[theme].get(attr_to_color_by)
    )
    map_fig.update_layout(
        mapbox_style=map_style,
        paper_bgcolor="#f8f9fa", # to match background color
        legend=dict(orientation="h", yanchor="bottom",
                    y=1.02, xanchor="center", x=0.5),
        height=700,
        margin={"l": 10, "r": 10, "t": 0, "b": 0},
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


def update_map(values, highlighting_dropdown, participants_checklist, accidents_data, date_range_monthly, theme="normal", selected_bright_map_theme=False):
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
    return prepare_map(highlighting_dropdown, filtered_data, theme, selected_bright_map_theme)


def update_particpants_checklist(click_data, accidents_data):
    if click_data:
        clicked_lat = click_data["points"][0]["lat"]
        clicked_lon = click_data["points"][0]["lon"]

        point_data = accidents_data.loc[
            (accidents_data[CONSTS.LATITUDE] == clicked_lat)
            & (accidents_data[CONSTS.LONGITUDE] == clicked_lon)
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


def update_bar_chart_and_details(click_data, accidents_data, theme="normal"):
    if click_data:
        clicked_lat = click_data["points"][0]["lat"]
        clicked_lon = click_data["points"][0]["lon"]

        point_data = accidents_data.loc[
            (accidents_data[CONSTS.LATITUDE] == clicked_lat) &
            (accidents_data[CONSTS.LONGITUDE] == clicked_lon)
        ]

        if not point_data.empty:
            # Update the bar chart
            bar_data = pd.DataFrame(
                {
                    "Unfallklasse Vorhersage": [
                        "Verstorben",
                        "Schwerverletzte",
                        "Leichtverletzte"
                    ],
                    "Value": [
                        point_data[CONSTS.WAHRSCHEINLICHKEIT_KLASSE_0].values[0],
                        point_data[CONSTS.WAHRSCHEINLICHKEIT_KLASSE_1].values[0],
                        point_data[CONSTS.WAHRSCHEINLICHKEIT_KLASSE_2].values[0],
                    ]
                }
            )

            # oneliner to get string of unfallklasse wahr ("Tödlich, Schwerverletzt, Leichtverletzt")
            unfallklasse_wahr = ["Tödlich", "Schwerverletzt",
                                 "Leichtverletzt"][int(point_data[CONSTS.UNFALLKLASSE_WAHR].values[0])]
            unfallklasse_bestimmt = ["Tödlich", "Schwerverletzt",
                                     "Leichtverletzt"][int(point_data[CONSTS.UNFALLKLASSE_BESTIMMT].values[0])]

            fig = px.bar(
                bar_data,
                x="Unfallklasse Vorhersage",
                y="Value",
                title=f"Vorhersage: {unfallklasse_bestimmt}   Tatsächlich: {
                    unfallklasse_wahr}",
            )

            fig.update_yaxes(title_text="Berechnete Wahrscheinlichkeit in %")
            fig.update_traces(marker_color=list(customColoringMap[theme].get(CONSTS.UNFALLKLASSE_WAHR+"_REPLACED").values()))
            fig.update_layout({
                "paper_bgcolor": "rgba(0, 0, 0, 0)"
            })

            # Update the details row
            unfallklasse = point_data[CONSTS.UNFALLKLASSE_WAHR].values[0]
            background_color = customColoringMap[theme].get(CONSTS.UNFALLKLASSE_WAHR)[unfallklasse]
            details = dbc.Row([
                dbc.Col(html.Div([              
                    html.H1(f"{rewriteDict[CONSTS.UNFALLKLASSE_WAHR].get(
                        str(unfallklasse), 'Unbekannt')}", style={"backgroundColor": background_color, "borderRadius": "5px", "paddingLeft": "10px"}),
                    html.Br(),
                    html.H2("Unfallbeteiligte"),
                    *(html.Img(src="assets/images/icons8-bicycle-50.png", alt="bicycle", style={ "padding-left": 5, "padding-right": 20}, title="Fahrrad")
                      for _ in [1] if point_data[CONSTS.ISTRAD].values[0] == 1),
                    *(html.Img(src="assets/images/icons8-car-50.png", alt="car", style={ "padding-left": 5, "padding-right": 20}, title="Auto")
                      for _ in [1] if point_data[CONSTS.ISTPKW].values[0] == 1),
                    *(html.Img(src="assets/images/icons8-walking-50.png", alt="pedestrian", style={ "padding-left": 5, "padding-right": 20}, title="Fußgänger")
                      for _ in [1] if point_data[CONSTS.ISTFUSS].values[0] == 1),
                    *(html.Img(src="assets/images/icons8-motorcycle-50.png", alt="motorcycle", style={ "padding-left": 5, "padding-right": 20}, title="Motorrad")
                      for _ in [1] if point_data[CONSTS.ISTKRAD].values[0] == 1),
                    *(html.Img(src="assets/images/icons8-train-50.png", alt="misc", style={ "padding-left": 5, "padding-right": 0}, title="Sonstiges")
                      for _ in [1] if point_data[CONSTS.ISTSONSTIG].values[0] == 1),
                    html.Br(),
                    html.H2("Unfallinformationen"),
                    html.P(f"{rewriteDict[CONSTS.UNFALLART].get(
                        str(point_data[CONSTS.UNFALLART].values[0]), 'Unbekannt')}"),
                    html.P(f"{rewriteDict[CONSTS.UNFALLTYP].get(
                        str(point_data[CONSTS.UNFALLTYP].values[0]), 'Unbekannt')}"),
                    html.P(f"Zeitraum: {point_data[CONSTS.STUNDE].values[0]} - {point_data[CONSTS.STUNDE].values[0]+1} Uhr an einem "
                            + ("Wochen" if point_data[CONSTS.TAGKATEGORIE].values[0] in  "1" else "Wochenend")+"tag."),
                    html.Br(),
                    html.H2("Verhältnisse"),
                    html.P(f"{rewriteDict[CONSTS.LICHTVERHAELTNISSE].get(
                        str(point_data[CONSTS.LICHTVERHAELTNISSE].values[0]), 'Unbekannt')}"),
                    html.P(f"{rewriteDict[CONSTS.STRASSENVERHAELTNISSE].get(
                        str(point_data[CONSTS.STRASSENVERHAELTNISSE].values[0]), 'Unbekannt')}"),
                    html.P(f"{rewriteDict[CONSTS.STRASSENART].get(
                        str(point_data[CONSTS.STRASSENART].values[0]), 'Unbekannt')}")
                ]))
            ], className="mt-4")

            return fig, details

    return no_update, no_update


def update_scatter_plot(click_data, accidents_data, theme="normal"):
    if click_data:
        clicked_lat = click_data["points"][0]["lat"]
        clicked_lon = click_data["points"][0]["lon"]

        # Filtern der Daten für den ausgewählten Punkt
        point_data = accidents_data.loc[
            (accidents_data[CONSTS.LATITUDE] == clicked_lat)
            & (accidents_data[CONSTS.LONGITUDE] == clicked_lon)
        ]

        if not point_data.empty:
            # Daten für den Scatterplot vorbereiten
            scatter_data = pd.DataFrame(
                {
                    "Feature": [
                        CONSTS.ISTRAD,
                        CONSTS.ISTPKW,
                        CONSTS.ISTFUSS,
                        CONSTS.ISTKRAD,
                        CONSTS.ISTSONSTIG,
                        CONSTS.TAGKATEGORIE,
                        CONSTS.MONAT,
                        CONSTS.STUNDE,
                        CONSTS.UNFALLART,
                        CONSTS.UNFALLTYP,
                        CONSTS.LICHTVERHAELTNISSE,
                        CONSTS.STRASSENVERHAELTNISSE,
                        CONSTS.STRASSENART,
                    ] * 3,  # Wiederhole Features für jede Unfallklasse
                    "SHAP-Wert": (
                        [
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
                        ]
                        + [
                            point_data[CONSTS.SHAP_1_ISTRAD].values[0],
                            point_data[CONSTS.SHAP_1_ISTPKW].values[0],
                            point_data[CONSTS.SHAP_1_ISTFUSS].values[0],
                            point_data[CONSTS.SHAP_1_ISTKRAD].values[0],
                            point_data[CONSTS.SHAP_1_ISTSONSTIG].values[0],
                            point_data[CONSTS.SHAP_1_TAGKATEGORIE].values[0],
                            point_data[CONSTS.SHAP_1_MONAT].values[0],
                            point_data[CONSTS.SHAP_1_STUNDE].values[0],
                            point_data[CONSTS.SHAP_1_UNFALLART].values[0],
                            point_data[CONSTS.SHAP_1_UNFALLTYP].values[0],
                            point_data[CONSTS.SHAP_1_LICHTVERHAELTNISSE].values[0],
                            point_data[CONSTS.SHAP_1_STRASSENVERHAELTNISSE].values[0],
                            point_data[CONSTS.SHAP_1_STRASSENART].values[0],
                        ]
                        + [
                            point_data[CONSTS.SHAP_2_ISTRAD].values[0],
                            point_data[CONSTS.SHAP_2_ISTPKW].values[0],
                            point_data[CONSTS.SHAP_2_ISTFUSS].values[0],
                            point_data[CONSTS.SHAP_2_ISTKRAD].values[0],
                            point_data[CONSTS.SHAP_2_ISTSONSTIG].values[0],
                            point_data[CONSTS.SHAP_2_TAGKATEGORIE].values[0],
                            point_data[CONSTS.SHAP_2_MONAT].values[0],
                            point_data[CONSTS.SHAP_2_STUNDE].values[0],
                            point_data[CONSTS.SHAP_2_UNFALLART].values[0],
                            point_data[CONSTS.SHAP_2_UNFALLTYP].values[0],
                            point_data[CONSTS.SHAP_2_LICHTVERHAELTNISSE].values[0],
                            point_data[CONSTS.SHAP_2_STRASSENVERHAELTNISSE].values[0],
                            point_data[CONSTS.SHAP_2_STRASSENART].values[0],
                        ]
                    ),
                    "Unfallklasse": (
                        ["Verstorben"] * 13 + ["Schwerverletzt"] * \
                        13 + ["Leichtverletzt"] * 13
                    ),
                }
            )

            # Scatterplot erstellen
            fig = px.scatter(
                scatter_data,
                x="Feature",
                y="SHAP-Wert",
                color="Unfallklasse",
                title="Einfluss der Features auf die Vorhersage",
                color_discrete_map=customColoringMap[theme].get(CONSTS.UNFALLKLASSE_WAHR+"_REPLACED"),
                hover_data=["Feature"],
            )
            fig.update_yaxes(title_text="SHAP-Wert")
            fig.update_xaxes(title_text="Feature")
            fig.update_traces(marker=dict(size=10))
            fig.update_layout({
                "paper_bgcolor": "rgba(0, 0, 0, 0)"
            })
            return fig
    return no_update


def update_uncertainty_plot(click_data, accidents_data):
    if click_data:
        hovered_lat = click_data["points"][0]["lat"]
        hovered_lon = click_data["points"][0]["lon"]

        # Filtern der Daten für den ausgewählten Punkt
        point_data = accidents_data.loc[
            (accidents_data[CONSTS.LATITUDE] == hovered_lat)
            & (accidents_data[CONSTS.LONGITUDE] == hovered_lon)
        ]

        if not point_data.empty:
            # Unsicherheitsdaten vorbereiten
            uncertainty_score = point_data[CONSTS.UNSICHERHEITS_SCORE].values[0]

            fig = px.bar(
                x=["Unsicherheit"],
                y=[uncertainty_score],
                title="Unsicherheitsfaktor der Vorhersage",
            )

            fig.update_yaxes(title_text="Unsicherheitsfaktor", range=[0, 1])
            fig.update_xaxes(title_text="")
            fig.update_traces(marker_color="purple", width=0.5)
            fig.update_layout({
                "paper_bgcolor": "rgba(0, 0, 0, 0)"
            })

            return fig
    return no_update
