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
# Get the last row -> "Total"
total = covid19_data.tail(1).values.tolist()
print("CHINA COVID19 Confirmed Cases: " + str(total[0][1]))
print("CHINA COVID19 Confirmed Deaths: " + str(total[0][2]))
