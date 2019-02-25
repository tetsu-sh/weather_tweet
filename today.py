from bs4 import BeautifulSoup
import requests
import pandas as pd

url="https://tenki.jp/live/3/16/47662.html"


response=requests.get(url)
res= BeautifulSoup(response.text,"html.parser")
test=res.find_all("span",class_="blue")
print(test)
