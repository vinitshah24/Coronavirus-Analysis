from bs4 import BeautifulSoup
import pandas as pd
import requests
import os

LATITUDES = {'Delhi': 28.7041, 'Haryana': 29.0588, 'Kerala': 10.8505, 'Rajasthan': 27.0238,
             'Telengana': 18.1124, 'Telangana': 18.1124, 'Uttar Pradesh': 26.8467,
             'Ladakh': 34.2996, 'Tamil Nadu': 11.1271, 'Jammu and Kashmir': 33.7782,
             'Punjab': 31.1471, 'Karnataka': 15.3173, 'Maharashtra': 19.7515,
             'Andhra Pradesh': 15.9129, 'Odisha': 20.9517, 'Uttarakhand': 30.0668,
             'West Bengal': 22.9868, 'Puducherry': 11.9416, 'Chandigarh': 30.7333,
             'Chhattisgarh': 21.2787, 'Gujarat': 22.2587, 'Himachal Pradesh': 31.1048,
             'Madhya Pradesh': 22.9734, 'Bihar': 25.0961, 'Manipur': 24.6637,
             'Mizoram': 23.1645, 'Goa': 15.2993, 'Andaman and Nicobar Islands': 11.7401,
             'Assam': 26.2006, 'Jharkhand': 23.6102, 'Arunachal Pradesh': 28.2180,
             'Tripura': 23.9408, 'Nagaland': 26.1584, 'Meghalaya': 25.4670,
             'Dadar Nagar Haveli': 20.1809, 'Sikkim': 27.5330,
             'Dadra and Nagar Haveli and Daman and Diu': 20.1809}

LONGITUDES = {'Delhi': 77.1025, 'Haryana': 76.0856, 'Kerala': 76.2711, 'Rajasthan': 74.2179,
              'Telengana': 79.0193, 'Telangana': 79.0193, 'Uttar Pradesh': 80.9462,
              'Ladakh': 78.2932, 'Tamil Nadu': 78.6569, 'Jammu and Kashmir': 76.5762,
              'Punjab': 75.3412, 'Karnataka': 75.7139, 'Maharashtra': 75.7139,
              'Andhra Pradesh': 79.7400, 'Odisha': 85.0985, 'Uttarakhand': 79.0193,
              'West Bengal': 87.8550, 'Puducherry': 79.8083, 'Chandigarh': 76.7794,
              'Chhattisgarh': 81.8661, 'Gujarat': 71.1924, 'Himachal Pradesh': 77.1734,
              'Madhya Pradesh': 78.6569, 'Bihar': 85.3131, 'Manipur': 93.9063,
              'Mizoram': 92.9376, 'Goa': 74.1240, 'Andaman and Nicobar Islands': 92.6586,
              'Assam': 92.9376, 'Jharkhand': 85.2799, 'Arunachal Pradesh': 94.7278,
              'Tripura': 91.9882, 'Nagaland': 94.5624, 'Meghalaya': 91.3662,
              'Dadar Nagar Haveli': 73.0169, 'Sikkim': 88.5122,
              'Dadra and Nagar Haveli and Daman and Diu': 73.0169}

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/84.0.4147.89 Safari/537.36'
}

URL = 'https://www.mohfw.gov.in/'
req = requests.get(URL, headers=HEADER)
soup = BeautifulSoup(req.content, "html.parser")

# with open("data.html", "w", encoding='utf-8') as file:
#    file.write(str(soup))

soup = BeautifulSoup(str(soup).replace("<!--<tbody>", "<tbody>"), "html.parser")
thead = soup.find_all('thead')[-1]
# Table Header
head = thead.find_all('tr')
# Table Body
tbody = soup.find_all('tbody')[-1]
body = tbody.find_all('tr')

table_header = []
table_data = []

for tr in head:
    td = tr.find_all('td')
    row = [i.text for i in td]
    table_header.append(row)

for tr in body:
    td = tr.find_all('td')
    row = [i.text for i in td]
    table_data.append(row)

dataframe = pd.DataFrame(table_data[:len(table_data)-2])
dataframe = dataframe.set_index([0])
dataframe.columns = ['State', 'Active Cases', 'Recovered', 'Deaths']
dataframe['Latitude'] = dataframe['State'].map(LATITUDES)
dataframe['Longitude'] = dataframe['State'].map(LONGITUDES)
dataframe['Date'] = pd.to_datetime('today').strftime("%m/%d/%Y")

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..', 'data'))
india_data_dir = os.path.join(data_dir, 'india')
csv_dir = os.path.join(india_data_dir, 'csv')
csv_data = os.path.join(csv_dir, 'india-cases.csv')
dataframe.to_csv(csv_data, index=False)
