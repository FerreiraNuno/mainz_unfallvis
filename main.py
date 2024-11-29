from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import consts as CONSTS

# Create Dash app
app = Dash(__name__)
# Load data
accidents_data = pd.read_csv("./data/Verkehrsunfalldaten.csv", delimiter=';', decimal=',')
# Prepare data
accidents_data[CONSTS.UNFALLKLASSE_WAHR] = accidents_data[CONSTS.UNFALLKLASSE_WAHR].astype(str)


def prepare_map(attr_to_color_by, coloring_map, data):
    # Add scatter map with coordinates of accidents
    map_fig = px.scatter_mapbox(
        data,
        lat=CONSTS.LATITUDE,
        lon=CONSTS.LONGITUDE,
        hover_name="Stadtteil",
        hover_data=[
            CONSTS.JAHR,
            CONSTS.UNFALLKLASSE_BESTIMMT,
            CONSTS.WAHRSCHEINLICHKEIT_KLASSE_0,
            CONSTS.WAHRSCHEINLICHKEIT_KLASSE_1,
            CONSTS.WAHRSCHEINLICHKEIT_KLASSE_2,
            CONSTS.UNSICHERHEITS_SCORE
        ],
        custom_data=[data.index],  # Pass the DataFrame index as custom data
        zoom=12,
        color=attr_to_color_by,
        color_discrete_map=coloring_map
    )
    map_fig.update_layout(mapbox_style="https://tiles-eu.stadiamaps.com/styles/alidade_smooth_dark.json")
    map_fig.update_layout(autosize=False, width=800, height=800, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    map_fig.update_layout(showlegend=False)  # Legende ausblenden
    return map_fig

@app.callback(
    Output('map', 'figure'),
    Input('year_range_slider', 'value')
)
def update_map(year):
    if year is not None:
        filtered_data = accidents_data.loc[
            lambda x: (x[CONSTS.JAHR] >= year[0]) & (x[CONSTS.JAHR] <= year[1])
        ]
        return prepare_map(CONSTS.UNFALLKLASSE_WAHR, {"0": "red", "1": "yellow", "2": "green"}, filtered_data)
    return prepare_map(CONSTS.UNFALLKLASSE_WAHR, {"0": "red", "1": "yellow", "2": "green"}, accidents_data)

@app.callback(
    Output('bar-chart', 'figure'),
    Input('map', 'hoverData')
)
def update_bar_chart(hover_data):
    if hover_data:
        # Extract latitude and longitude from hoverData
        hovered_lat = hover_data['points'][0]['lat']
        hovered_lon = hover_data['points'][0]['lon']

        # Filter the dataset to find the corresponding row
        point_data = accidents_data.loc[
            (accidents_data[CONSTS.LATITUDE] == hovered_lat) &
            (accidents_data[CONSTS.LONGITUDE] == hovered_lon)
        ]

        if not point_data.empty:
            # Prepare data for the bar chart
            bar_data = pd.DataFrame({
                "Unfallklasse Vorhersage": ["Tödlicher Ausgang", "Schwerverletzte", "Leichtverletzte"],
                "Value": [
                    point_data[CONSTS.WAHRSCHEINLICHKEIT_KLASSE_0].values[0],
                    point_data[CONSTS.WAHRSCHEINLICHKEIT_KLASSE_1].values[0],
                    point_data[CONSTS.WAHRSCHEINLICHKEIT_KLASSE_2].values[0]
                ]
            })

            # Create bar chart
            fig = px.bar(bar_data, x="Unfallklasse Vorhersage", y="Value", title="Vorhersage nach Unfallklasse")
            fig.update_layout(height=800)
            return fig

    # Default empty figure
    return go.Figure()



def main():
  # Set Dash layout for displaying the map and the bar chart
  app.layout = html.Div([
      html.H4('Unfall-Dashboard'),
      html.Div([
        dcc.Graph(id="map",figure=prepare_map(CONSTS.UNFALLKLASSE_WAHR, {"0": "red", "1": "yellow", "2": "green"}, accidents_data), config={'scrollZoom': True}),
        dcc.Graph(id="bar-chart")
      ], style={'display': 'flex'}),
      dcc.RangeSlider(
          id="year_range_slider",
          min=accidents_data[CONSTS.JAHR].min(),
          max=accidents_data[CONSTS.JAHR].max(),
          value=[accidents_data[CONSTS.JAHR].min(), accidents_data[CONSTS.JAHR].max()],
          step=1,
          marks=dict([(i, x) for i, x in zip(accidents_data[CONSTS.JAHR], accidents_data[CONSTS.JAHR].astype(str))])
      )
  ])
  
  app.run_server(debug=True, port=8081)

if __name__ == "__main__":
    main()
