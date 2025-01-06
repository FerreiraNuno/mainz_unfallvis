from dash import Dash, dcc, html, Input, Output, no_update
import dash_bootstrap_components as dbc
import pandas as pd
from config import *

import consts as CONSTS
from mapbox import prepare_map, render_map_tab, update_particpants_checklist, update_bar_chart_and_details, update_map, update_scatter_plot, update_uncertainty_plot
from helper import generateDateRangeByMinAndMaxDate, prepareData, prepare_marks
from overview import update_overview_graph, render_overview
from overview_accident_conditions import render_overview_accident_conditions, update_extended_overview_graph
from layout import get_layout

# Load data -----------------------------------------------------------------------------------------------------------------------------
accidents_data = pd.read_csv(
    "./data/Verkehrsunfalldaten.csv", delimiter=";", decimal=",")
date_range_monthly = generateDateRangeByMinAndMaxDate(accidents_data)

# Create Dash app ---------------------------------------------------------------------------------------------------------------------
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.9.1/font/bootstrap-icons.min.css"
    ],
    suppress_callback_exceptions=True
)


# Layout ---------------------------------------------------------------------------------------------------------------------

# Callback for the tab contents
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "value"),
)
def render_tab_content(tab_value):
    if tab_value == "overview_tab":
        return render_overview()
    elif tab_value == "overview_accident_conditions_tab":
        return render_overview_accident_conditions()
    elif tab_value == "map_tab":
        marks_dict = prepare_marks(date_range_monthly)
        return render_map_tab(marks_dict, accidents_data, date_range_monthly)


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


# Karte Tab ---------------------------------------------------------------------------------------------------------------------

# Callback for map year range slider
@app.callback(
    Output("map", "figure"),
    Input("year_range_slider", "value"),
    Input("highlighting_dropdown", "value"),
    Input("participants_checklist", "value"),
    Input("theme-dropdown", "value")
)
def update_map_callback(values, highlighting_dropdown, participants_checklist, selected_theme):
    return update_map(values, highlighting_dropdown, participants_checklist, accidents_data, date_range_monthly, selected_theme)


# Callback for bar chart and details
@app.callback(
    [
        Output("bar-chart-predicted-accident-class", "figure"),
        Output("details-row", "children"),
    ],
    Input("map", "clickData")
)
def update_bar_chart_callback(click_data):
    return update_bar_chart_and_details(click_data, accidents_data)


# Callback for the pairplot/scatter plot
@app.callback(
    Output("pairplot-shap-values", "figure"),
    Input("map", "clickData")
)
def update_pairplot_callback(click_data):
    return update_scatter_plot(click_data, accidents_data)


# Callback for the uncertainty graph
@app.callback(
    Output("uncertainty-graph", "figure"),
    Input("map", "clickData")
)
def update_uncertainty_graph(click_data):
    return update_uncertainty_plot(click_data, accidents_data)


# Callback for the participants checklist
@app.callback(
    Output("participants_view_checklist", "value"),
    Input("map", "clickData")
)
def update_particpants_checklist_callback(click_data):
    return update_particpants_checklist(click_data, accidents_data)


# Callback for the theme dropdown
@app.callback(
    Output("theme-dropdown", "value"),
    Input("theme-dropdown", "value"),
)
def update_theme(selected_theme):
    return selected_theme


# Überblick Tab ---------------------------------------------------------------------------------------------------------------------

# Callback for the overview graphs
@app.callback(
    Output("overview-graph-container", "children"),  #
    Input("overview-selection", "value"),
)
def update_graph(selected_chart):
    return update_overview_graph(selected_chart, accidents_data)


# Callback for the extended overview graphs
@app.callback(
    Output("overview-extended-graph-container", "children"),
    Input("overview-selection-extended", "value"),
)
def update_extended_graph(selected_chart):
    return update_extended_overview_graph(selected_chart, accidents_data)


# Main function ---------------------------------------------------------------------------------------------------------------------
def main():
    # Layout der App
    app.layout = get_layout()

    # Server starten
    app.run_server(debug=True, port=8081)


if __name__ == "__main__":
    prepareData(accidents_data)
    main()
