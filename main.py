from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from datetime import datetime
import consts as CONSTS

# Create Dash app
app = Dash(__name__)

# Load data
accidents_data = pd.read_csv("./data/Verkehrsunfalldaten.csv", delimiter=';', decimal=',')

#Prepare data
accidents_data[CONSTS.UNFALLKLASSE_WAHR] = accidents_data[CONSTS.UNFALLKLASSE_WAHR].astype(str)

#Prepare time slider values
marks_time_range_slider = dict([(i,x) for i, x in zip(accidents_data[CONSTS.JAHR], accidents_data[CONSTS.JAHR].astype(str))])


def prepare_map(attr_to_color_by, coloring_map, data):
    # Add scatter map with coordinates of accidents
    map = px.scatter_map(data, lat=CONSTS.LATITUDE, lon=CONSTS.LONGITUDE, hover_name="Stadtteil", hover_data=[CONSTS.JAHR, CONSTS.UNFALLKLASSE_BESTIMMT,CONSTS.WAHRSCHEINLICHKEIT_KLASSE_0, CONSTS.WAHRSCHEINLICHKEIT_KLASSE_1, CONSTS.WAHRSCHEINLICHKEIT_KLASSE_2, CONSTS.UNSICHERHEITS_SCORE],
                    zoom=12, color=attr_to_color_by, color_discrete_map=coloring_map)
    # Set background map style
    map.update_layout(map_style="https://tiles-eu.stadiamaps.com/styles/alidade_smooth_dark.json") # API-Key not needed while running on localhost https://docs.stadiamaps.com/themes/
    # Set size of map
    map.update_layout(autosize=False, width=1600, height=800, margin={"r":0,"t":0,"l":0,"b":0}) # erstmal hardcoded :/
    return map


@app.callback(
    Output('map', 'figure'),
    Input('year_range_slider', 'value')
    )
def update_map(year):
    if year is not None:
        filtered_data = accidents_data.loc[lambda x : (x[CONSTS.JAHR] >= year[0] ) & (x[CONSTS.JAHR] <= year[1])] 
        return prepare_map(CONSTS.UNFALLKLASSE_WAHR, {"0": "red", "1": "yellow", "2": "green"}, filtered_data)
    return prepare_map(CONSTS.UNFALLKLASSE_WAHR, {"0": "red", "1": "yellow", "2": "green"}, accidents_data)


app.layout = html.Div([
    html.H4('Unfall-Dashboard'),
    dcc.Graph(id="map", figure=prepare_map(CONSTS.UNFALLKLASSE_WAHR, {"0": "red", "1": "yellow", "2": "green"}, accidents_data)),
    dcc.RangeSlider(id="year_range_slider", min=accidents_data[CONSTS.JAHR].min(), max=accidents_data[CONSTS.JAHR].max(), value=[accidents_data[CONSTS.JAHR].min(), accidents_data[CONSTS.JAHR].max()], step=1, marks=marks_time_range_slider),
])


def main():
    app.run_server(debug=False, port=8081)

if __name__ == "__main__":
    main()