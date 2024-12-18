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
            # Second RadioItem
            html.H5("Überblick über die Unfallverhältnisse:",
                    className="header-bar-h3"),
            html.Div(
                dcc.RadioItems(
                    id="overview-selection-extended",
                    options=[
                        {"label": "Zeitliche Verteilung der Unfälle",
                                  "value": "temporal-accidents-distribution"},
                        {"label": "Verteilung der Unfälle auf Stadtteile",
                                  "value": "accident-region"},
                        {"label": "Häufigkeit von Unfallarten und -typen",
                                  "value": "accident-types-frequency"},
                        {"label": "Einfluss der Umweltbedingungen",
                                  "value": "environmental-conditions-impact"},
                        {"label": "Unfallbeteiligte Fahrzeugarten",
                                  "value": "vehicle-participation"},
                    ],
                    value="temporal-accidents-distribution",  # Standardwert
                    labelStyle={"display": "inline-block",
                                "marginRight": "15px"},
                ),
                style={"marginBottom": "20px"},
            ),
            # Platzhalter für die neuen Diagramme
            html.Div(id="overview-extended-graph-container"),
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


def update_extended_overview_graph(selected_chart, accidents_data):
    if selected_chart == "temporal-accidents-distribution":
        # Heatmap: Stunden vs. Monate
        heatmap_data = accidents_data.groupby(
            [CONSTS.MONAT, CONSTS.STUNDE]).size().unstack(fill_value=0)
        heatmap_fig = px.imshow(
            heatmap_data,
            labels=dict(x="Stunde", y="Monat", color="Anzahl"),
            x=heatmap_data.columns,
            y=heatmap_data.index,
            title="Unfallhäufigkeit: Stunden vs. Monate",
        )

        # Mapping für Unfallklassen
        order_map = {"2": "Leichtverletzt",
                     "1": "Schwerverletzt", "0": "Tödlicher Ausgang"}
        color_map = {"Leichtverletzt": "green",
                     "Schwerverletzt": "orange", "Tödlicher Ausgang": "red"}

        # 1. Monatsdaten auffüllen
        all_months = pd.DataFrame(
            {"Monat": range(1, 13)})  # Monate von 1 bis 12
        all_classes = pd.DataFrame(order_map.values(), columns=[
                                   CONSTS.UNFALLKLASSE_WAHR])

        # Erstelle ein vollständiges Raster mit allen Kombinationen von Monat und Unfallklasse
        full_monthly_data = all_months.merge(all_classes, how="cross")

        # Aggregiere die Unfallzahlen nach Monat und Unfallklasse
        monthly_data = accidents_data.groupby(
            [CONSTS.MONAT, CONSTS.UNFALLKLASSE_WAHR]).size().reset_index(name="Anzahl")
        monthly_data[CONSTS.UNFALLKLASSE_WAHR] = monthly_data[CONSTS.UNFALLKLASSE_WAHR].map(
            order_map)

        # Mische die aggregierten Daten mit dem vollständigen Raster und fülle fehlende Werte mit 0
        monthly_data = full_monthly_data.merge(
            monthly_data, on=[CONSTS.MONAT, CONSTS.UNFALLKLASSE_WAHR], how="left").fillna(0)

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

        # 2. Stundendaten auffüllen
        # Stunden von 0 bis 23
        all_hours = pd.DataFrame({"Stunde": range(0, 24)})
        full_hourly_data = all_hours.merge(all_classes, how="cross")

        # Aggregiere die Unfallzahlen nach Stunde und Unfallklasse
        hourly_data = accidents_data.groupby(
            [CONSTS.STUNDE, CONSTS.UNFALLKLASSE_WAHR]).size().reset_index(name="Anzahl")
        hourly_data[CONSTS.UNFALLKLASSE_WAHR] = hourly_data[CONSTS.UNFALLKLASSE_WAHR].map(
            order_map)

        # Mische die aggregierten Daten mit dem vollständigen Raster und fülle fehlende Werte mit 0
        hourly_data = full_hourly_data.merge(
            hourly_data, on=[CONSTS.STUNDE, CONSTS.UNFALLKLASSE_WAHR], how="left").fillna(0)

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
            dcc.Graph(figure=monthly_line_fig),
            dcc.Graph(figure=hourly_line_fig),
            dcc.Graph(figure=heatmap_fig)
        ])

    elif selected_chart == 'accident-region':
        # Mapping der Unfallschwere
        order_map = {"2": "Leichtverletzt",
                     "1": "Schwerverletzt", "0": "Tödlicher Ausgang"}
        color_map = {"Leichtverletzt": "green",
                     "Schwerverletzt": "orange", "Tödlicher Ausgang": "red"}

        # Vorbereitung der Daten
        severity_data = (
            accidents_data.groupby(
                [CONSTS.STADTTEIL, CONSTS.UNFALLKLASSE_WAHR])
            .size()
            .reset_index(name="Anzahl")
        )
        severity_data[CONSTS.UNFALLKLASSE_WAHR] = severity_data[CONSTS.UNFALLKLASSE_WAHR].map(
            order_map)

        # Gesamtsumme der Unfälle pro Stadtteil berechnen und sortieren
        total_accidents_per_district = severity_data.groupby(
            CONSTS.STADTTEIL)["Anzahl"].sum().sort_values(ascending=False)
        sorted_districts = total_accidents_per_district.index.tolist()

        # Erstellung des Diagramms
        severity_fig = px.bar(
            severity_data,
            x=CONSTS.STADTTEIL,
            y="Anzahl",
            color=CONSTS.UNFALLKLASSE_WAHR,
            title="Anzahl der Unfälle nach Unfallschwere in den Stadtteilen",
            color_discrete_map=color_map,
            # Stadtteile sortieren
            category_orders={"Stadtteil": sorted_districts},
        )

        # Layout-Anpassungen
        severity_fig.update_layout(
            xaxis_title="Stadtteil",
            yaxis_title="Anzahl der Unfälle",
            barmode="stack",  # Gestapelte Balken
            legend_title="Unfallschwere",
        )

        # Rückgabe der Diagramme
        return html.Div([
            dcc.Graph(figure=severity_fig)
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

        # Mapping der Unfallklassen
        order_map_unfallklasse = {"2": "Leichtverletzt",
                                  "1": "Schwerverletzt", "0": "Tödlicher Ausgang"}
        color_map_unfallklasse = {"Leichtverletzt": "green",
                                  "Schwerverletzt": "orange", "Tödlicher Ausgang": "red"}

        # Groupiere die Unfalldaten nach Unfallart, -typ und Unfallklasse
        accident_types_data1 = accidents_data.groupby(
            [CONSTS.UNFALLART, CONSTS.UNFALLKLASSE_WAHR]).size().reset_index(name="Anzahl")
        accident_types_data2 = accidents_data.groupby(
            [CONSTS.UNFALLTYP, CONSTS.UNFALLKLASSE_WAHR]).size().reset_index(name="Anzahl")
        accident_types_data = accidents_data.groupby(
            [CONSTS.UNFALLART, CONSTS.UNFALLTYP]).size().reset_index(name="Anzahl")

        # Mappe die Unfallerarten, Unfalltypen und Unfallklassen auf ihre Beschreibungen
        accident_types_data[CONSTS.UNFALLART] = accident_types_data[CONSTS.UNFALLART].map(
            order_map_unfallart)
        accident_types_data1[CONSTS.UNFALLART] = accident_types_data1[CONSTS.UNFALLART].map(
            order_map_unfallart)
        accident_types_data[CONSTS.UNFALLTYP] = accident_types_data[CONSTS.UNFALLTYP].map(
            order_map_unfalltyp)
        accident_types_data2[CONSTS.UNFALLTYP] = accident_types_data2[CONSTS.UNFALLTYP].map(
            order_map_unfalltyp)
        accident_types_data1[CONSTS.UNFALLKLASSE_WAHR] = accident_types_data1[CONSTS.UNFALLKLASSE_WAHR].map(
            order_map_unfallklasse)
        accident_types_data2[CONSTS.UNFALLKLASSE_WAHR] = accident_types_data2[CONSTS.UNFALLKLASSE_WAHR].map(
            order_map_unfallklasse)

        # Diagramm 1: Häufigkeit der Unfallarten gestapelt nach Unfallklassen
        fig_unfallart = px.bar(
            accident_types_data1,
            x=CONSTS.UNFALLART,
            y="Anzahl",
            color=CONSTS.UNFALLKLASSE_WAHR,  # Gestapelte Balken nach Unfallklasse
            title="Häufigkeit der Unfallarten nach Unfallschwere",
            color_discrete_map=color_map_unfallklasse,  # Farbmapping für die Unfallklassen
            # Achsenbezeichnung anpassen
            labels={CONSTS.UNFALLART: "Unfallart",
                    CONSTS.UNFALLKLASSE_WAHR: "Unfallschwere"},
            barmode="stack"  # Balken gestapelt
        )
        fig_unfallart.update_layout(height=600)
        fig_unfallart.update_layout(showlegend=True)  # Legende anzeigen

        # Diagramm 2: Häufigkeit der Unfalltypen gestapelt nach Unfallklassen
        fig_unfalltyp = px.bar(
            accident_types_data2,
            x=CONSTS.UNFALLTYP,
            y="Anzahl",
            color=CONSTS.UNFALLKLASSE_WAHR,  # Gestapelte Balken nach Unfallklasse
            title="Häufigkeit der Unfalltypen nach Unfallschwere",
            color_discrete_map=color_map_unfallklasse,  # Farbmapping für die Unfallklassen
            # Achsenbezeichnung anpassen
            labels={CONSTS.UNFALLTYP: "Unfalltyp",
                    CONSTS.UNFALLKLASSE_WAHR: "Unfallschwere"},
            barmode="stack"  # Balken gestapelt
        )
        fig_unfalltyp.update_layout(height=400)
        fig_unfalltyp.update_layout(showlegend=True)  # Legende anzeigen

        # Diagramm 3: Kombiniertes Diagramm für Unfallarten und -typen (bereits wie gehabt)
        fig_combined = px.bar(
            accident_types_data,
            x=CONSTS.UNFALLART,
            y="Anzahl",
            color=CONSTS.UNFALLTYP,
            title="Häufigkeit von Unfallarten und -typen",
            barmode="group",  # Gruppiert die Balken für unterschiedliche Unfalltypen nebeneinander
            labels={CONSTS.UNFALLART: "Unfallart",
                    CONSTS.UNFALLTYP: "Unfalltyp"},  # Achsenbezeichnungen
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
        env_conditions_data = accidents_data.groupby(
            [CONSTS.LICHTVERHAELTNISSE, CONSTS.STRASSENVERHAELTNISSE, CONSTS.UNFALLKLASSE_WAHR]).size().reset_index(name="Anzahl")

        # Wende die Mappings auf die entsprechenden Spalten an
        env_conditions_data[CONSTS.LICHTVERHAELTNISSE] = env_conditions_data[CONSTS.LICHTVERHAELTNISSE].map(
            licht_map)
        env_conditions_data[CONSTS.STRASSENVERHAELTNISSE] = env_conditions_data[CONSTS.STRASSENVERHAELTNISSE].map(
            strassen_map)
        env_conditions_data[CONSTS.UNFALLKLASSE_WAHR] = env_conditions_data[CONSTS.UNFALLKLASSE_WAHR].map(
            unfallklasse_map)

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
            value_vars=[CONSTS.ISTPKW, CONSTS.ISTKRAD,
                        CONSTS.ISTRAD, CONSTS.ISTFUSS, CONSTS.ISTSONSTIG],
            var_name="Fahrzeugart",
            value_name="Beteiligung",
        )

        # Filtere die Daten, um nur die beteiligten Fahrzeuge zu behalten (Beteiligung == 1)
        vehicle_data = vehicle_data[vehicle_data["Beteiligung"] == 1]

        # Wende das Mapping für die Unfallklassen an
        vehicle_data[CONSTS.UNFALLKLASSE_WAHR] = vehicle_data[CONSTS.UNFALLKLASSE_WAHR].map(
            unfallklasse_map)

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
            vehicle_data.groupby(
                ["Fahrzeugart", CONSTS.UNFALLKLASSE_WAHR]).size().reset_index(name="Anzahl"),
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
                # Optional: Auch Y-Achse für "Anzahl" anpassen
                "Anzahl": "Anzahl der Beteiligungen"
            }
        )

        # Rückgabe des Diagramms
        return dcc.Graph(figure=fig)
    return html.Div("Bitte eine valide Option auswählen.")
