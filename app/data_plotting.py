import pandas as pd
import plotly
import plotly.graph_objs as go
import json
import os

data_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'data'))
csv_dir = os.path.join(data_dir, 'csv')
csv_data = os.path.join(csv_dir, '20200322-141025-dxy-2019ncov-data.csv')
covid19_data = pd.read_csv(csv_data, sep='|', skiprows=2)
covid19_data.drop(['notes', 'sources'], axis=1, inplace=True)
covid19_data.columns = ['region', 'confirmed_cases', 'deaths']
covid19_data.drop(covid19_data.tail(1).index, inplace=True)

json_dir = os.path.join(data_dir, 'json')
geojson_file = os.path.join(json_dir, 'china_geojson.json')
with open(geojson_file) as file:
    china = json.load(file)
    file.close()

maps_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'maps'))
confirmed_cases_map = os.path.join(
    maps_dir, 'china-corona-virus-confirmed-cases.html')
fig = go.Figure(go.Choroplethmapbox(geojson=china, locations=covid19_data.region, z=covid19_data.confirmed_cases,
                                    colorscale='Jet',
                                    zmin=0, zmax=2000,
                                    marker_opacity=0.5, marker_line_width=0
                                    ))
fig.update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=3, mapbox_center={"lat": 35.8617, "lon": 104.1954})
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
plotly.offline.plot(fig,
                    filename=confirmed_cases_map)

deaths_map = os.path.join(maps_dir, 'china-corona-virus-deaths.html')
fig2 = go.Figure(go.Choroplethmapbox(geojson=china,
                                     locations=covid19_data.region, z=covid19_data.deaths,
                                     colorscale='Jet',
                                     zmin=0, zmax=30,
                                     marker_opacity=0.5, marker_line_width=0))
fig2.update_layout(mapbox_style="carto-positron",
                   mapbox_zoom=3, mapbox_center={"lat": 35.8617, "lon": 104.1954})
fig2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
plotly.offline.plot(fig2, filename=deaths_map)
