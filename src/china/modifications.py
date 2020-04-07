import pandas as pd
import os

data_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..\..', 'data')
)
china_data_dir = os.path.join(data_dir, 'china')
csv_dir = os.path.join(china_data_dir, 'csv')

"""
a = os.path.join(csv_dir, '20200122-032810-dxy-2019ncov-data.csv')
b = os.path.join(csv_dir, '20200314-213110-dxy-2019ncov-data.csv')

df = pd.read_csv(a, sep='|', skiprows=2)
df.drop(['notes', 'sources'], axis=1, inplace=True)
print(df)
print()

df2 = pd.read_csv(b, sep='|', skiprows=2)
df2.drop(['notes', 'sources'], axis=1, inplace=True)
print(df2)
print()

c = pd.merge(df, df2, on=['# place'], how='outer')
c = c.fillna(0)
c['confirmed_cases'] = c['confirmed_cases_x'] + c['confirmed_cases_y']
c['deaths'] = c['deaths_x'] + c['deaths_y']
c.drop(['confirmed_cases_x', 'confirmed_cases_y', 'deaths_x', 'deaths_y'], axis=1, inplace=True)
print(c)
"""

df = pd.DataFrame(columns=['# place', 'confirmed_cases', 'deaths'])
for found_file in os.listdir(csv_dir):
    current_file = os.path.join(csv_dir, found_file)
    print(current_file)
    if os.path.isfile(current_file):
        open_file = open(current_file, encoding="utf8").readlines()
        header = open_file[2].strip()
        if '# place|confirmed_cases|deaths|notes|sources' in header:
            if df.empty:
                df = pd.read_csv(current_file, sep='|', skiprows=2)
                df.drop(df.tail(1).index, inplace=True)
                df.drop(['notes', 'sources'], axis=1, inplace=True)
                print("df populated")
            else:
                df2 = pd.read_csv(current_file, sep='|', skiprows=2)
                df2.drop(df2.tail(1).index, inplace=True)
                df2.drop(['notes', 'sources'], axis=1, inplace=True)
                df_merged = pd.merge(df, df2, on=['# place'], how='outer')
                df_merged = df_merged.fillna(0)
                print(df_merged)
                df_merged['confirmed_cases'] = df_merged['confirmed_cases_x'] + \
                    df_merged['confirmed_cases_y']
                df_merged['deaths'] = df_merged['deaths_x'] + \
                    df_merged['deaths_y']
                #df_merged.drop(['confirmed_cases_x', 'confirmed_cases_y', 'deaths_x', 'deaths_y'], axis=1, inplace=True)
                print(df_merged)
        else:
            df2 = pd.read_csv(current_file, sep='|', skiprows=2, header=None,
                              names=['# place', 'confirmed_cases', 'deaths', 'notes', 'sources'])
            df2.drop(df2.tail(1).index, inplace=True)
            df2.drop(['notes', 'sources'], axis=1, inplace=True)
            df_merged = df_merged.fillna(0)
            df_merged['confirmed_cases'] = df_merged['confirmed_cases_x'] + \
                df_merged['confirmed_cases_y']
            df_merged['deaths'] = df_merged['deaths_x'] + df_merged['deaths_y']
            #df_merged.drop(['confirmed_cases_x', 'confirmed_cases_y', 'deaths_x', 'deaths_y'], axis=1, inplace=True)
            print(df_merged)
df_merged.drop(['confirmed_cases_x', 'deaths_x'], axis=1, inplace=True)
df_merged.columns = ['place', 'confirmed_cases', 'deaths']

df_merged.sort_values(by=['confirmed_cases'], ascending=False, inplace=True)
print(df_merged)
