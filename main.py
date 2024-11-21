from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

# Load data
accidents_data = pd.read_csv("./data/Verkehrsunfalldaten.csv", delimiter=';', decimal=',')
accidents_data["Unfallklasse Wahr"] = accidents_data["Unfallklasse Wahr"].astype(str)

# Add scatter map with coordinates of accidents
fig = px.scatter_map(accidents_data, lat="Latitude", lon="Longitude", hover_name="Stadtteil", hover_data=['Stunde', 'Monat', 'Jahr', 'IstRad', 'IstPKW', 'IstFuss', 'IstKrad', 'IstSonstig'],
                    zoom=12, color="Unfallklasse Wahr", color_discrete_map={"0": "red", "1": "yellow", "2": "green"})
# Add background map
fig.update_layout(map_style="https://tiles-eu.stadiamaps.com/styles/alidade_smooth_dark.json") # API-Key not needed while running on localhost https://docs.stadiamaps.com/themes/
# Set size of map
fig.update_layout(autosize=False, width=1600, height=800, margin={"r":0,"t":0,"l":0,"b":0}) # erstmal hardcoded :/


# Create Dash app
app = Dash(__name__)
app.layout = html.Div([
    html.H4('Header'),
    dcc.Graph(figure=fig, id="map"),
    html.P("Paragraph")
])
app.run_server(debug=True, port=8081)