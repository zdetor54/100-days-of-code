import requests
from bs4 import BeautifulSoup
import smtplib

URL = "https://www.amazon.co.uk/Philips-Hue-Wireless-Installation-Free-Exclusive/dp/B08PKMT2DV/ref=sr_1_5?keywords" \
      "=philips%2Bhue%2Bswitch%2Bv2&qid=1690988122&sprefix=philips%2Bhue%2Bswi%2Caps%2C80&sr=8-5&th=1"
my_email = 'zacbjss@gmail.com'
my_password = 'liacwrjuqvdmtqrm'
TARGET_PRICE = 21

header = {
    "Accept-Language": 'en',
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

# Scrape amazon website and get the current item price
response = requests.get(url=URL, headers=header)
soup = BeautifulSoup(markup=response.content, features="html.parser")
current_price = float(soup.find(class_="a-offscreen").getText()[1:])

def send_email(price, link):
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs='zdetor54@gmail.com',
            msg=f'Subject:Price Drop to {price}!\n\nGo to: \n{URL}.\n The price has dropped so you can buy the item'
        )

if current_price <= TARGET_PRICE:
    send_email(current_price, URL)
else:
    print("Don't buy")

