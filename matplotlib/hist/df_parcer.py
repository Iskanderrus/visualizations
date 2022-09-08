import pandas as pd
import requests
from bs4 import BeautifulSoup

wikiurl = 'https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions'
table_class = 'wikitable sortable jquery-tablesorter'

response = requests.get(wikiurl)
# status 200: The server successfully answered the http request
print(response.status_code)

soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table', {'class': "wikitable"})

df2018 = pd.read_html(str(table))[0]

emi_ = df2018[('2018 CO2 emissions[21]', 'Total excluding LUCF[23]')]
country_ = list(df2018[('Country[20]', 'Country[20]')])
country_mod = [i.replace('\xa0', ' ') for i in country_]

# create df
df = pd.DataFrame(zip(country_mod, emi_), columns=['countries', 'emission_2018'])

# delete a row that cannot be converted
df = df[df['countries'] != 'Serbia & Montenegro']
df.iloc[:, 1] = df.iloc[:, 1].astype('float')

df = df[(df['emission_2018'] > 200) & (df['emission_2018'] < 1000)]
df['percentage'] = [i * 100 / sum(df['emission_2018']) for i in df['emission_2018']]
df_s = df.sort_values(by='emission_2018', ascending=False)

df.to_csv('carbon_dioxide_emissions.csv', encoding='utf-8')
