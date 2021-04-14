import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://developers.google.com/public-data/docs/canonical/countries_csv'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find('table')

with open('data/countries_geodata.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        csv_row = [column.get_text() for column in columns]
        writer.writerow(csv_row)
    