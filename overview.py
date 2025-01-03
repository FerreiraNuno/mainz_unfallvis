from dash import dcc, html
import consts as CONSTS
from config import *
import pandas as pd


def render_overview():
    return html.Div(
        [
            # Auswahl für den Nutzer
            html.H5("Überblick über die Anzahl an Unfälle:",
                    className="header-bar-h3"),
            html.Div(
                dcc.RadioItems(
                    id="overview-selection",
                    options=[
                        {"label": "Unfälle gesamt",
                                  "value": "bar-chart-accidents-overview"},
                        {"label": "Unfälle nach Jahr",
                                  "value": "bar-chart-accidents-years-overview"},
                        {"label": "Unfälle nach Monat",
                                  "value": "line-chart-accidents-date-overview"},
                    ],
                    value="bar-chart-accidents-overview",  # Standardwert
                    labelStyle={"display": "inline-block",
                                "marginRight": "15px"},
                ),
                style={"marginBottom": "20px"},
            ),
            # Platzhalter für das Diagramm
            html.Div(id="overview-graph-container"),
        ]
    )


def update_overview_graph(selected_chart, accidents_data):
    if selected_chart == "bar-chart-accidents-overview":
        # Gruppieren der Daten nach Unfallklasse
        data_by_class = accidents_data.groupby(
            CONSTS.UNFALLKLASSE_WAHR).size().reset_index(name="Anzahl")

        # Mapping für die Labels
        order_map = {"2": "Leichtverletzt",
                     "1": "Schwerverletzt", "0": "Tödlicher Ausgang"}
        data_by_class[CONSTS.UNFALLKLASSE_WAHR] = data_by_class[CONSTS.UNFALLKLASSE_WAHR].map(
            order_map)
        data_by_class[CONSTS.UNFALLKLASSE_WAHR] = pd.Categorical(
            data_by_class[CONSTS.UNFALLKLASSE_WAHR],
            categories=["Leichtverletzt",
                        "Schwerverletzt", "Tödlicher Ausgang"],
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
        data_by_year = accidents_data.groupby(
            [CONSTS.JAHR, CONSTS.UNFALLKLASSE_WAHR]).size().reset_index(name="Anzahl")
        data_by_year = data_by_year.loc[data_by_year[CONSTS.JAHR].between(
            2016, 2022)]

        # Mapping für die Reihenfolge und Labels
        order_map = {"2": "Leichtverletzt",
                     "1": "Schwerverletzt", "0": "Tödlicher Ausgang"}
        data_by_year[CONSTS.UNFALLKLASSE_WAHR] = data_by_year[CONSTS.UNFALLKLASSE_WAHR].map(
            order_map)
        data_by_year[CONSTS.UNFALLKLASSE_WAHR] = pd.Categorical(
            data_by_year[CONSTS.UNFALLKLASSE_WAHR],
            categories=["Leichtverletzt",
                        "Schwerverletzt", "Tödlicher Ausgang"],
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
        # Gruppiere die Daten nach Jahr und Unfallklasse, dann reindexiere und fülle fehlende Werte mit 0 -> wird benötigt um bei Liniendiagramme 0-Werte zu ergänzen
        data_by_year_filled = (
            data_by_year
            # Setze Index für MultiIndex-Gruppierung
            .set_index([CONSTS.JAHR, CONSTS.UNFALLKLASSE_WAHR])
            .unstack(fill_value=0)  # Fehlende Kombinationen mit 0 auffüllen
            .stack()  # MultiIndex zurück in eine flache Struktur konvertieren
            .reset_index()
        )
        line_fig = px.line(
            data_by_year_filled,
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
        data_by_date = accidents_data.groupby(
            [CONSTS.CUSTOM_DATETIME, CONSTS.UNFALLKLASSE_WAHR]).size().reset_index(name="Anzahl")

        # Mapping für die Labels
        order_map = {"2": "Leichtverletzt",
                     "1": "Schwerverletzt", "0": "Tödlicher Ausgang"}
        data_by_date[CONSTS.UNFALLKLASSE_WAHR] = data_by_date[CONSTS.UNFALLKLASSE_WAHR].map(
            order_map)
        data_by_date[CONSTS.UNFALLKLASSE_WAHR] = pd.Categorical(
            data_by_date[CONSTS.UNFALLKLASSE_WAHR],
            categories=["Leichtverletzt",
                        "Schwerverletzt", "Tödlicher Ausgang"],
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
        # Für das Datum: Füge einen vollständigen Datumsbereich hinzu -> Notwendig um Null im Liniendiagramm anzuzeigen
        # Gruppiere die Daten nach Datum und Unfallklasse, dann reindexiere und fülle fehlende Werte mit 0
        data_by_date_filled = (
            data_by_date
            # Setze Index für MultiIndex-Gruppierung
            .set_index([CONSTS.CUSTOM_DATETIME, CONSTS.UNFALLKLASSE_WAHR])
            .unstack(fill_value=0)  # Fehlende Kombinationen mit 0 auffüllen
            .stack()  # MultiIndex zurück in eine flache Struktur konvertieren
            .reset_index()
        )
        line_fig_date = px.line(
            data_by_date_filled,
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
        line_fig_date.update_layout(
            xaxis_title="Datum",
            yaxis_title="Anzahl der Unfälle",
            legend_title="Unfallklasse",
            xaxis=dict(tickformat="%Y-%m-%d"),
        )

        return html.Div([
            dcc.Graph(figure=bar_fig),
            dcc.Graph(figure=line_fig_date),
        ])

    return html.Div("Bitte eine valide Option auswählen.")  # Fallback