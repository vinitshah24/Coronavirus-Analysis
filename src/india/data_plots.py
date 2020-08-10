import pandas as pd
import plotly
import plotly.graph_objects as go
import json
import os

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..', 'data'))
india_data_dir = os.path.join(data_dir, 'india')
csv_dir = os.path.join(india_data_dir, 'csv')
csv_data = os.path.join(csv_dir, 'india-cases.csv')
json_dir = os.path.join(india_data_dir, 'json')
json_data = os.path.join(json_dir, 'india_states.json')
maps_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..', 'maps'))
deaths_map = os.path.join(maps_dir, 'india-corona-virus-deaths.html')

dataframe = pd.read_csv(csv_data, header=0)
with open(json_data) as file:
    india = json.load(file)
    file.close()

fig = go.Figure(data=go.Choropleth(geojson=india,
                                   featureidkey='properties.ST_NM',
                                   locationmode='geojson-id',
                                   locations=dataframe['State'],
                                   z=dataframe['Deaths'],
                                   zmin=0, zmax=2000,
                                   autocolorscale=False,
                                   colorscale='Reds',
                                   marker_line_color='darkgray',
                                   colorbar=dict(title={'text': "Deaths"}, thickness=30, len=0.9,
                                                 bgcolor='rgba(255,255,255,0.6)',
                                                 xanchor='right', yanchor='middle')
                                   ))

fig.update_geos(visible=False,
                projection=dict(
                    type='conic conformal',
                    parallels=[12.472944444, 35.172805555556],
                    rotation={'lat': 24, 'lon': 80}
                ),
                lonaxis={'range': [68, 98]},
                lataxis={'range': [6, 38]})

fig.update_layout(mapbox_style="carto-positron",
                  title=dict(
                      text="COVID-19 Deaths in India",
                      xanchor='center',
                      x=0.5,
                      yref='paper',
                      yanchor='bottom',
                      y=1,
                      pad={'b': 10}
                  ),
                  mapbox_zoom=3,
                  mapbox_center={"lat": 35.8617, "lon": 104.1954},
                  margin={"r": 0, "t": 0, "l": 0, "b": 0})

plotly.offline.plot(fig, filename=deaths_map)
