from urllib.request import urlopen
import pandas as pd
import json
import os

data_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..\..', 'data')
)
usa_data_dir = os.path.join(data_dir, 'usa')
csv_dir = os.path.join(usa_data_dir, 'csv')

csv_data = os.path.join(csv_dir, 'us-counties.csv')
df = pd.read_csv(csv_data, sep=',', header=0)

df = df.loc[df['date'] == '2020-04-06']
print("Total Cases: " + str(df['cases'].sum()))
print("Total Deaths: " + str(df['deaths'].sum()))

# Filling empty cells
df = df.fillna(0)
# Converting the column to int32
df["fips"] = df["fips"].astype(int)
# Removing rows where fips is 0
df = df.loc[df['fips'] != 0]
print(df)

# df.to_csv('results.csv', encoding='utf-8')

with pd.option_context('display.max_rows', 10000, 'display.max_columns', 10):
    # print(df)

state_data = os.path.join(csv_dir, 'us-states.csv')
state_code_data = os.path.join(csv_dir, 'us-agr-exports-2011.csv')

df_state = pd.read_csv(state_data, sep=',', header=0)

junk_data = pd.read_csv(state_code_data, sep=',', header=0)
df_code = junk_data[['code', 'state']]

result = df_state.merge(df_code, on=['state'], how='left')
result = result.loc[result['date'] == '2020-04-05']

# print(result)
