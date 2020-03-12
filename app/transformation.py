import pandas as pd
import os

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
csv_dir = os.path.join(data_dir, 'csv')

df = pd.DataFrame(columns=['# place', 'confirmed_cases', 'deaths'])
for found_file in os.listdir(csv_dir):
    current_file = os.path.join(csv_dir, found_file)
    print(current_file)
    if os.path.isfile(current_file):
        open_file = open(current_file, encoding="utf8").readlines()
        header = open_file[2].strip()
        if '# place|confirmed_cases|deaths|notes|sources' in header:
            df2 = pd.read_csv(current_file, sep='|', skiprows=2)
            df2.drop(['notes', 'sources'], axis=1, inplace=True)
            df_merged = pd.merge(df, df2, how='right', on='# place')
        else:
            df2 = pd.read_csv(current_file,
                              sep='|',
                              skiprows=2,
                              names=['# place', 'confirmed_cases', 'deaths', 'notes', 'sources'],
                              header=None)
            df2.drop(['notes', 'sources'], axis=1, inplace=True)
            df_merged = pd.merge(df, df2, how='right', on='# place')
df_merged.drop(['confirmed_cases_x', 'deaths_x'], axis=1, inplace=True)
df_merged.columns = ['place', 'confirmed_cases', 'deaths']

df_merged.sort_values(by=['confirmed_cases'], ascending=False, inplace=True)
print(df_merged)
