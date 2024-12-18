from dash import Dash, dcc, html, Input, Output, no_update, State
import plotly.express as px
import pandas as pd
import consts as CONSTS
from config import *
from datetime import datetime
import dash_bootstrap_components as dbc

# Create Dash app
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.9.1/font/bootstrap-icons.min.css"
    ],
    suppress_callback_exceptions=True
)

# Load data -----------------------------------------------------------------------------------------------------------------------------
accidents_data = pd.read_csv("./data/Verkehrsunfalldaten.csv", delimiter=";", decimal=",")

def generateDateRangeByMinAndMaxDate(df):
    start = str(df[CONSTS.JAHR].min()) + "-" + str(df[CONSTS.MONAT].min()) + "-" + "1"
    end = str(df[CONSTS.JAHR].max()) + "-" + str(df[CONSTS.MONAT].max()) + "-" + "1"
    month_year_range = pd.date_range(
        start=start, end=end, freq="MS"
    )  # MS DateOffset Monthly Starting

    return {
        each: {"label": str(date), "style": {'transform': 'rotate(45deg)'}}
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



# Callback for the Info-Button
@app.callback(
    Output("info-modal", "is_open"),
    Input("info-button", "n_clicks"),
    prevent_initial_call=True
)
def toggle_modal(info_btn_clicks):
    if info_btn_clicks:
        return True
    return False



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
    Output("participants_view_checklist", "value"), 
    Input("map", "clickData")
)
def update_particpants_checklist(click_data):
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

def prepare_marks():
    marks_dict = {key: value for key, value in date_range_monthly.items() if key % 3 == 0}
    last_key = list(date_range_monthly.keys())[-1]
    marks_dict[last_key] = date_range_monthly.get(last_key)
    return marks_dict



# Overview-Tab ------------------------------------------------------------------------------------------------------------------------
# Overview Accidents
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
            xaxis=dict(tickformat="%Y-%m"),  # Format der Datumsanzeige
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



# Second Overview ----------------------------------------------------------------------------------------------------------------------
@app.callback(
    Output("overview-extended-graph-container", "children"),
    Input("overview-selection-extended", "value"),
)
def update_extended_overview_graph(selected_chart):
    if selected_chart == "temporal-accidents-distribution":
        # Heatmap: Stunden vs. Monate
        heatmap_data = accidents_data.groupby([CONSTS.MONAT, CONSTS.STUNDE]).size().unstack(fill_value=0)
        heatmap_fig = px.imshow(
            heatmap_data,
            labels=dict(x="Stunde", y="Monat", color="Anzahl"),
            x=heatmap_data.columns,
            y=heatmap_data.index,
            title="Unfallhäufigkeit: Stunden vs. Monate",
        )
        
        order_map = {"2": "Leichtverletzt", "1": "Schwerverletzt", "0": "Tödlicher Ausgang"}
        color_map = {"Leichtverletzt": "green", "Schwerverletzt": "orange", "Tödlicher Ausgang": "red"}
        # Daten für monatliche Unfallzahlen aggregieren
        monthly_data = accidents_data.groupby([CONSTS.MONAT, CONSTS.UNFALLKLASSE_WAHR]).size().reset_index(name="Anzahl")
        monthly_data[CONSTS.UNFALLKLASSE_WAHR] = monthly_data[CONSTS.UNFALLKLASSE_WAHR].map(order_map)

        # Liniendiagramm für Monate
        monthly_line_fig = px.line(
            monthly_data,
            x=CONSTS.MONAT,
            y="Anzahl",
            color=CONSTS.UNFALLKLASSE_WAHR,
            title="Unfallzahlen pro Monat",
            color_discrete_map=color_map,
            markers=True  # Optional: Punkte für die Werte hinzufügen
        )

        # Layout-Anpassungen für Monat-Diagramm
        monthly_line_fig.update_layout(
            xaxis_title="Monat",
            yaxis_title="Anzahl der Unfälle",
            legend_title="Unfallklasse"
        )

        # Daten für stündliche Unfallzahlen aggregieren
        hourly_data = accidents_data.groupby([CONSTS.STUNDE, CONSTS.UNFALLKLASSE_WAHR]).size().reset_index(name="Anzahl")
        hourly_data[CONSTS.UNFALLKLASSE_WAHR] = hourly_data[CONSTS.UNFALLKLASSE_WAHR].map(order_map)

        # Liniendiagramm für Stunden
        hourly_line_fig = px.line(
            hourly_data,
            x=CONSTS.STUNDE,
            y="Anzahl",
            color=CONSTS.UNFALLKLASSE_WAHR,
            title="Unfallzahlen pro Stunde",
            color_discrete_map=color_map,
            markers=True  # Optional: Punkte für die Werte hinzufügen
        )

        # Layout-Anpassungen für Stunden-Diagramm
        hourly_line_fig.update_layout(
            xaxis_title="Stunde",
            yaxis_title="Anzahl der Unfälle",
            legend_title="Unfallklasse"
        )

        # Rückgabe der beiden Diagramme
        return html.Div([
            dcc.Graph(figure=heatmap_fig),
            dcc.Graph(figure=monthly_line_fig),
            dcc.Graph(figure=hourly_line_fig)
        ])

    elif selected_chart == 'accident-region':
        # Daten für die Heatmap vorbereiten: Gruppierung nach Stadtteil und Monat
        heatmap_data = accidents_data.groupby(["Stadtteil", CONSTS.MONAT]).size().reset_index(name="Anzahl")

        # Heatmap erstellen
        heatmap_fig = px.density_heatmap(
            heatmap_data,
            x=CONSTS.MONAT,
            y="Stadtteil",
            z="Anzahl",
            title="Verteilung der Unfälle: Stadtteile vs. Monate",
            color_continuous_scale="Viridis",  # Farbskala
        )

        # Layout-Anpassungen für die Heatmap
        heatmap_fig.update_layout(
            xaxis_title="Monat",
            yaxis_title="Stadtteil",
            coloraxis_colorbar=dict(title="Unfälle"),  # Titel für die Farblegende
            xaxis=dict(tickmode="array", tickvals=list(range(1, 13)), ticktext=[
                "Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"
            ]),  # Monatsnamen
        )


        # Daten für Unfälle pro Stadtteil aggregieren
        district_data = accidents_data.groupby("Stadtteil").size().reset_index(name="Anzahl")
        district_data = district_data.sort_values("Anzahl", ascending=False)  # Optional: Stadtteile nach Anzahl sortieren

        # Balkendiagramm für Stadtteile
        district_bar_fig = px.bar(
            district_data,
            x="Stadtteil",
            y="Anzahl",
            title="Anzahl der Unfälle pro Stadtteil",
            color="Anzahl",
            color_continuous_scale="Viridis",  # Farbskala
        )

        # Layout-Anpassungen für das Diagramm
        district_bar_fig.update_layout(
            xaxis_title="Stadtteil",
            yaxis_title="Anzahl der Unfälle",
            coloraxis_colorbar=dict(title="Unfälle"),  # Titel für die Farblegende
            xaxis_tickangle=45  # Optional: Dreht die Beschriftungen der Stadtteile
        )

        # Rückgabe der Diagramme
        return html.Div([
            dcc.Graph(figure=heatmap_fig),
            dcc.Graph(figure=district_bar_fig)
        ])

    elif selected_chart == "accident-types-frequency":
        # Zuerst definierst du das "order_map" und wandelst die Werte in den richtigen Text um
        order_map_unfallart = {
            "0": "Unfall anderer Art", 
            "1": "Zusammenstoß mit anfahrendem/anhaltendem/ruhendem Fahrzeug", 
            "2": "Zusammenstoß mit vorausfahrendem/wartendem Fahrzeug", 
            "3": "Zusammenstoß mit seitlich in gleicher Richtung fahrendem Fahrzeug", 
            "4": "Zusammenstoß mit entgegenkommendem Fahrzeug", 
            "5": "Zusammenstoß mit einbiegendem/kreuzendem Fahrzeug", 
            "6": "Zusammenstoß zwischen Fahrzeug und Fußgänger", 
            "7": "Aufprall auf Fahrbahnhindernis", 
            "8": "Abkommen von Fahrbahn nach rechts", 
            "9": "Abkommen von Fahrbahn nach links"
        }

        order_map_unfalltyp = {
            "0": "Fahrunfall", 
            "1": "Abbiegeunfall", 
            "2": "Einbiegen / Kreuzen-Unfall", 
            "3": "Überschreiten-Unfall", 
            "4": "Unfall durch ruhenden Verkehr", 
            "5": "Unfall im Längsverkehr", 
            "6": "sonstiger Unfall"
        }

        # Groupiere die Unfalldaten nach Unfallart und -typ
        accident_types_data = accidents_data.groupby([CONSTS.UNFALLART, CONSTS.UNFALLTYP]).size().reset_index(name="Anzahl")

        # Mappe die Unfallerarten und Unfalltypen auf ihre Beschreibungen
        accident_types_data[CONSTS.UNFALLART] = accident_types_data[CONSTS.UNFALLART].map(order_map_unfallart)
        accident_types_data[CONSTS.UNFALLTYP] = accident_types_data[CONSTS.UNFALLTYP].map(order_map_unfalltyp)

        # Diagramm 1: Häufigkeit der Unfallarten (nur Unfallart, ohne Unfalltyp)
        fig_unfallart = px.bar(
            accident_types_data.groupby(CONSTS.UNFALLART)['Anzahl'].sum().reset_index(),  # Gruppierung nur nach Unfallart
            x=CONSTS.UNFALLART,
            y="Anzahl",
            title="Häufigkeit der Unfallarten",
            color=CONSTS.UNFALLART,  # Jede Unfallart wird in einer anderen Farbe dargestellt
            labels={CONSTS.UNFALLART: "Unfallart"},  # Achsenbezeichnung anpassen
        )
        fig_unfallart.update_layout(height=600) 
        # Entferne die Legende im Diagramm 1
        fig_unfallart.update_layout(showlegend=False)

        # Diagramm 2: Häufigkeit der Unfalltypen (nur Unfalltyp, ohne Unfallart)
        fig_unfalltyp = px.bar(
            accident_types_data.groupby(CONSTS.UNFALLTYP)['Anzahl'].sum().reset_index(),  # Gruppierung nur nach Unfalltyp
            x=CONSTS.UNFALLTYP,
            y="Anzahl",
            title="Häufigkeit der Unfalltypen",
            color=CONSTS.UNFALLTYP,  # Jeder Unfalltyp wird in einer anderen Farbe dargestellt
            labels={CONSTS.UNFALLTYP: "Unfalltyp"},  # Achsenbezeichnung anpassen
        )
        fig_unfalltyp.update_layout(height=400) 
        # Entferne die Legende im Diagramm 2
        fig_unfalltyp.update_layout(showlegend=False)

        # Diagramm 3: Kombiniertes Diagramm für Unfallarten und -typen (bereits wie gehabt)
        fig_combined = px.bar(
            accident_types_data,
            x=CONSTS.UNFALLART,
            y="Anzahl",
            color=CONSTS.UNFALLTYP,
            title="Häufigkeit von Unfallarten und -typen",
            barmode="group",  # Gruppiert die Balken für unterschiedliche Unfalltypen nebeneinander
            labels={CONSTS.UNFALLART: "Unfallart", CONSTS.UNFALLTYP: "Unfalltyp"},  # Achsenbezeichnungen
        )
        fig_combined.update_layout(height=800) 

        # Rückgabe der Diagramme als mehrere Graphen
        return html.Div([
            dcc.Graph(figure=fig_unfallart),
            dcc.Graph(figure=fig_unfalltyp),
            dcc.Graph(figure=fig_combined)
        ])


    
    elif selected_chart == "environmental-conditions-impact":
        # Mapping der Lichtverhältnisse
        licht_map = {
            "2": "Dunkelheit", 
            "1": "Dämmerung", 
            "0": "Tageslicht"
        }

        # Mapping der Straßenverhältnisse (hier als Beispiel)
        strassen_map = {
            "0": "Trocken",
            "1": "nass/feucht/schlüpfrig",
            "2": "winterglatt"
        }

        # Mapping der Unfallklassen (hier als Beispiel)
        unfallklasse_map = {
            "1": "Leichtverletzte",
            "2": "Schwerverletzte",
            "0": "Tödlicher Ausgang"
        }

        # Gruppiere die Daten nach den relevanten Spalten
        env_conditions_data = accidents_data.groupby([CONSTS.LICHTVERHAELTNISSE, CONSTS.STRASSENVERHAELTNISSE, CONSTS.UNFALLKLASSE_WAHR]).size().reset_index(name="Anzahl")

        # Wende die Mappings auf die entsprechenden Spalten an
        env_conditions_data[CONSTS.LICHTVERHAELTNISSE] = env_conditions_data[CONSTS.LICHTVERHAELTNISSE].map(licht_map)
        env_conditions_data[CONSTS.STRASSENVERHAELTNISSE] = env_conditions_data[CONSTS.STRASSENVERHAELTNISSE].map(strassen_map)
        env_conditions_data[CONSTS.UNFALLKLASSE_WAHR] = env_conditions_data[CONSTS.UNFALLKLASSE_WAHR].map(unfallklasse_map)

        # Erstelle das gestapelte Balkendiagramm
        fig = px.bar(
            env_conditions_data,
            x=CONSTS.LICHTVERHAELTNISSE,
            y="Anzahl",
            color=CONSTS.STRASSENVERHAELTNISSE,
            title="Einfluss der Lichtverhältnisse auf Unfälle",
            barmode="stack",
            facet_col=CONSTS.UNFALLKLASSE_WAHR,
            labels={  # Hier kannst du die Achsenbeschriftungen ändern
                CONSTS.LICHTVERHAELTNISSE: "Lichtverhältnis",
                CONSTS.STRASSENVERHAELTNISSE: "Straßenverhältnis",
                CONSTS.UNFALLKLASSE_WAHR: "Unfallklasse"
            }
        )

        # Rückgabe des Diagramms
        return dcc.Graph(figure=fig)

    
    elif selected_chart == "vehicle-participation":
        # Mapping der Unfallklassen
        unfallklasse_map = {
            "1": "Leichtverletzte",
            "2": "Schwerverletzte",
            "0": "Tödlicher Ausgang"
        }

        # Wandle die Fahrzeugdaten um, um die verschiedenen Fahrzeugarten als Variablen zu haben
        vehicle_data = accidents_data.melt(
            id_vars=[CONSTS.UNFALLKLASSE_WAHR],
            value_vars=[CONSTS.ISTPKW, CONSTS.ISTKRAD, CONSTS.ISTRAD, CONSTS.ISTFUSS, CONSTS.ISTSONSTIG],
            var_name="Fahrzeugart",
            value_name="Beteiligung",
        )

        # Filtere die Daten, um nur die beteiligten Fahrzeuge zu behalten (Beteiligung == 1)
        vehicle_data = vehicle_data[vehicle_data["Beteiligung"] == 1]

        # Wende das Mapping für die Unfallklassen an
        vehicle_data[CONSTS.UNFALLKLASSE_WAHR] = vehicle_data[CONSTS.UNFALLKLASSE_WAHR].map(unfallklasse_map)

        # Entferne das "ist" aus den Fahrzeugart-Spaltennamen
        vehicle_data["Fahrzeugart"] = vehicle_data["Fahrzeugart"].replace({
            CONSTS.ISTPKW: "PKW",
            CONSTS.ISTKRAD: "K-Rad",
            CONSTS.ISTRAD: "Fahrrad",
            CONSTS.ISTFUSS: "Fußgänger",
            CONSTS.ISTSONSTIG: "Sonstige"
        })

        # Erstelle das gestapelte Balkendiagramm
        fig = px.bar(
            vehicle_data.groupby(["Fahrzeugart", CONSTS.UNFALLKLASSE_WAHR]).size().reset_index(name="Anzahl"),
            x="Fahrzeugart",
            y="Anzahl",
            color=CONSTS.UNFALLKLASSE_WAHR,
            title="Unfallbeteiligte Fahrzeugarten",
            barmode="stack",
            color_discrete_map={  # Farben für die Unfallklassen anpassen
                "Tödlicher Ausgang": "red",  # 0 wird rot
                "Leichtverletzte": "green",  # 1 wird grün
                "Schwerverletzte": "orange"  # 2 wird orange
            },
            labels={  # Achsenbezeichner anpassen
                "Fahrzeugart": "Fahrzeugart",
                CONSTS.UNFALLKLASSE_WAHR: "Unfallklasse",
                "Anzahl": "Anzahl der Beteiligungen"  # Optional: Auch Y-Achse für "Anzahl" anpassen
            }
        )

        # Rückgabe des Diagramms
        return dcc.Graph(figure=fig)    
    return html.Div("Bitte eine valide Option auswählen.")




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
                html.H5("Überblick über die Anzahl an Unfälle:", className="header-bar-h3"),
                html.Div(
                    dcc.RadioItems(
                        id="overview-selection",
                        options=[
                            {"label": "Unfälle gesamt", "value": "bar-chart-accidents-overview"},
                            {"label": "Unfälle nach Jahr", "value": "bar-chart-accidents-years-overview"},
                            {"label": "Unfälle nach Monat", "value": "line-chart-accidents-date-overview"},
                        ],
                        value="bar-chart-accidents-overview",  # Standardwert
                        labelStyle={"display": "inline-block", "margin-right": "15px"},
                    ),
                    style={"margin-bottom": "20px"},
                ),
                html.Div(id="overview-graph-container"),  # Platzhalter für das Diagramm
                # Second RadioItem
                html.H5("Überblick über die Unfallverhältnisse:", className="header-bar-h3"),
                html.Div(
                    dcc.RadioItems(
                        id="overview-selection-extended",
                        options=[
                            {"label": "Zeitliche Verteilung der Unfälle", "value": "temporal-accidents-distribution"},
                            {"label": "Verteilung der Unfälle auf Stadtteile", "value": "accident-region"},
                            {"label": "Häufigkeit von Unfallarten und -typen", "value": "accident-types-frequency"},
                            {"label": "Einfluss der Umweltbedingungen", "value": "environmental-conditions-impact"},
                            {"label": "Unfallbeteiligte Fahrzeugarten", "value": "vehicle-participation"},
                        ],
                        value="temporal-accidents-distribution",  # Standardwert
                        labelStyle={"display": "inline-block", "margin-right": "15px"},
                    ),
                    style={"margin-bottom": "20px"},
                ),
                html.Div(id="overview-extended-graph-container"),  # Platzhalter für die neuen Diagramme
            ]
        )
    elif tab_value == "erkunden":
        marks_dict = prepare_marks()

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
                                        )
                                    )
                                ),
                            ],
                        ),
                    ],
                    style={"align-items": "end"} 
                )
            ]
        )


def main():
    # Info-Button und Modal
    info_button_and_modal = html.Div([
        # Info-Button
        dbc.Button(
            html.I(className="bi bi-info-circle"),  # Bootstrap Info-Icon
            id="info-button",
            color="secondary",
            outline=True,
            className="float-end",
            style={"margin-right": "10px"}
        ),
        # Modal
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Informationen über den Datensatz"), close_button=True),
                dbc.ModalBody(
                    "Die zugrunde liegenden Daten umfassen Verkehrsunfälle in Mainz und wurden verwendet, "
                    "um ein Machine-Learning-Modell (XGBoost) zu trainieren. Dieses Modell klassifiziert Unfälle "
                    "nach ihrem Ausgang in drei Kategorien: Unfälle mit Leichtverletzten, Schwerverletzten und "
                    "tödlichem Ausgang. Neben den geographischen Informationen der Unfallorte beinhalten die "
                    "Daten auch Merkmale wie die Art der Beteiligten (z. B. Pkw, Fahrrad, Fußgänger), zeitliche "
                    "Faktoren (Monat, Stunde, Wochentag/ Wochenende) sowie Bedingungen am Unfallort wie "
                    "Straßen- und Lichtverhältnisse. Zusätzlich wurden SHAP-Werte berechnet, um den Einfluss "
                    "jedes Merkmals auf die Modellvorhersagen zu erklären und die Transparenz zu erhöhen. "
                    "Durch die Integration von Unsicherheitsfaktoren und erklärbarer KI bietet die Analyse eine "
                    "detaillierte Grundlage für die Bewertung und Verbesserung der Verkehrssicherheit."
                ),

            ],
            id="info-modal",
            is_open=False,
            centered=True,
        )
    ])

    # Layout der App
    app.layout = html.Div(
        [
            html.Div(
                [
                    html.H3("Unfall-Dashboard", style={"display": "inline-block"}),
                    info_button_and_modal,  # Info-Button und Modal hinzufügen
                ],
                className="header-bar"  # Optional: Styling für die Leiste
            ),
            dcc.Tabs(
                id="tabs",
                value="ueberblick",
                children=[
                    dcc.Tab(label="Überblick", value="ueberblick", style={"font-weight": "bold"}),
                    dcc.Tab(label="Erkunden", value="erkunden", style={"font-weight": "bold"}),
                ]
            ),
            html.Div(id="tab-content"),
        ]
    )

    # Server starten
    app.run_server(debug=True, port=8081)




if __name__ == "__main__":
    init()
    main()
