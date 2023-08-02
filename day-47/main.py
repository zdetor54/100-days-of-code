import requests
from bs4 import BeautifulSoup

URL = "https://www.amazon.co.uk/Philips-Hue-Wireless-Installation-Free-Exclusive/dp/B08PKMT2DV/ref=sr_1_5?keywords" \
      "=philips%2Bhue%2Bswitch%2Bv2&qid=1690988122&sprefix=philips%2Bhue%2Bswi%2Caps%2C80&sr=8-5&th=1"
TARGET_PRICE = 21

header = {
    "Accept-Language": 'en',
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

# Scrape amazon website and get the current item price
response = requests.get(url=URL, headers=header)
soup = BeautifulSoup(markup=response.content, features="html.parser")
current_price = float(soup.find(class_="a-offscreen").getText()[1:])

if current_price <= TARGET_PRICE:
    print ('Buy')
else:
    print("Don't buy")


