from urllib.request import urlopen
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import plotly
import json
import os

data_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'usa_data')
)
csv_dir = os.path.join(data_dir, 'csv')
csv_data = os.path.join(csv_dir, 'us-counties.csv')
df = pd.read_csv(csv_data, sep=',', header=0)

# Filtering by latest date
df = df.loc[df['date'] == '2020-04-05']
# Filling empty cells
df = df.fillna(0)
# Converting the column to int32
df["fips"] = df["fips"].astype(int)
print(df)

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

maps_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'maps')
)
result_html = os.path.join(maps_dir, 'usa-counties-coronavirus-heatmap.html')

fig = px.choropleth_mapbox(df,
                           geojson=counties,
                           locations='fips',
                           color='deaths',
                           hover_data=["county", "state", "deaths", "cases"],
                           color_continuous_scale="Jet",
                           range_color=(0, 30),
                           mapbox_style="carto-positron",
                           zoom=3, center={"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'county': 'County', 'state': 'State'}
                           )
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
plotly.offline.plot(fig, filename=result_html)

state_data = os.path.join(csv_dir, 'us-states.csv')
state_code_data = os.path.join(csv_dir, 'us-agr-exports-2011.csv')
df_state = pd.read_csv(state_data, sep=',', header=0)
junk_data = pd.read_csv(state_code_data, sep=',', header=0)
df_code = junk_data[['code', 'state']]
plot_data = df_state.merge(df_code, on=['state'], how='left')
plot_data = plot_data.loc[plot_data['date'] == '2020-04-05']
print(plot_data)
states_plot = os.path.join(maps_dir, 'usa-states-coronavirus-heatmap.html')

plot_data['text'] = 'State: ' + plot_data['state'].astype(str) + '<br>' + \
    'Cases: ' + plot_data['cases'].astype(str) + '<br>' + \
    'Deaths: ' + plot_data['deaths'].astype(str)

# Color-scales: https://plotly.com/python/v3/colorscales/
fig = go.Figure(data=go.Choropleth(
    locations=plot_data['code'],
    z=plot_data['deaths'],
    locationmode='USA-states',
    colorscale=[
        [0.0, 'rgb(165,0,38)'],
        [0.1111111111111111, 'rgb(215,48,39)'],
        [0.2222222222222222, 'rgb(244,109,67)'],
        [0.3333333333333333, 'rgb(253,174,97)'],
        [0.4444444444444444, 'rgb(254,224,144)'],
        [0.5555555555555556, 'rgb(224,243,248)'],
        [0.6666666666666666, 'rgb(171,217,233)'],
        [0.7777777777777778, 'rgb(116,173,209)'],
        [0.8888888888888888, 'rgb(69,117,180)'],
        [1.0, 'rgb(49,54,149)']
    ],
    text=plot_data['text'],  # hover text
    colorbar_title='Deaths'
))

fig.update_layout(
    title_text='2020 Coronavirus Deaths in USA',
    geo=dict(
        scope='usa',
        projection=go.layout.geo.Projection(type='albers usa')
    )
)

plotly.offline.plot(fig, filename=states_plot)

# Reference: https://plotly.com/python/choropleth-maps/
