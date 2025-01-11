from dash import html, dcc
import dash_bootstrap_components as dbc

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

info_button_and_modal = html.Div([
    # Info-Button
    dbc.Button(
        html.I(className="bi bi-info-circle"),  # Bootstrap Info-Icon
        id="info-button",
        color="secondary",
        outline=True,
        className="float-end",
        style={"marginRight": "10px"}
    ),
    # Modal
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle(
                "Informationen über den Datensatz"), close_button=True),
            dbc.ModalBody([
                "Die zugrunde liegenden Daten umfassen Verkehrsunfälle in Mainz und wurden verwendet, "
                "um ein Machine-Learning-Modell (XGBoost) zu trainieren. Dieses Modell klassifiziert Unfälle "
                "nach ihrem Ausgang in drei Kategorien: Unfälle mit Leichtverletzten, Schwerverletzten und "
                "tödlichem Ausgang. Neben den geographischen Informationen der Unfallorte beinhalten die "
                "Daten auch Merkmale wie die Art der Beteiligten (z. B. Pkw, Fahrrad, Fußgänger), zeitliche "
                "Faktoren (Monat, Stunde, Wochentag/ Wochenende) sowie Bedingungen am Unfallort wie "
                "Straßen- und Lichtverhältnisse. Zusätzlich wurden SHAP-Werte berechnet, um den Einfluss "
                "jedes Merkmals auf die Modellvorhersagen zu erklären und die Transparenz zu erhöhen. "
                "Durch die Integration von Unsicherheitsfaktoren und erklärbarer KI bietet die Analyse eine "
                "detaillierte Grundlage für die Bewertung und Verbesserung der Verkehrssicherheit.",
                html.Hr(),  # Horizontal rule for separation

                html.H5("Icon Attribution"),
                html.P([
                    "Icons used in this project are provided by", 
                    html.A("Icons8", href="https://icons8.com/icons", target="_blank"), "."
                ])
            ]),
        ],
        id="info-modal",
        is_open=False,
        centered=True,
    )
])


def get_layout():
    return html.Div(
        [
            html.Div(
                [
                    html.H3("Unfall-Dashboard",
                            style={"display": "inline-block"}),
                    html.Div([
                        html.Div("Farbmodus:", style={"display": "inline-block",
                                                      "marginLeft": "10px", "color": "gray"}),
                        theme_dropdown
                    ], style={"display": "flex", "flexDirection": "row", "alignItems": "baseline", "gap": "20px"}),
                    info_button_and_modal,  # Info-Button und Modal hinzufügen
                ],
                className="header-bar"  # Optional: Styling für die Leiste
            ),
            dcc.Tabs(
                id="tabs",
                value="map_tab",
                children=[
                      dcc.Tab(label="Karte", value="map_tab"),
                      dcc.Tab(label="Überblick Unfälle", value="overview_tab"),
                      dcc.Tab(label="Überblick Unfallverhältnisse",
                              value="overview_accident_conditions_tab"),
                ]
            ),
            html.Div(id="tab-content"),
        ]
    )
