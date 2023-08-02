from bs4 import BeautifulSoup
import requests

URL = 'https://www.billboard.com/charts/hot-100/'


# year = input("What is the date (YYYY-MM-DD) you wanna use for your playlist:")

year = '2000-01-01'

response = requests.get(url=f"{URL}{year}/")
soup = BeautifulSoup(markup=response.text, features="html.parser")
songs = [x.find(name='h3').getText().strip() for x in soup.findAll(class_='o-chart-results-list-row-container')]

print(songs)

