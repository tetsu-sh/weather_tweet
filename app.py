import urllib3, sys,json,requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from config import CONFIG
import tweepy

CONSUMER_KEY=CONFIG["CONSUMER_KEY"]
CONSUMER_SECRET=CONFIG["CONSUMER_SECRET"]
ACCESS_TOKEN=CONFIG["ACCESS_TOKEN"]
ACCESS_SECRET=CONFIG["ACCESS_SECRET"]



api="http://weather.livedoor.com/forecast/webservice/json/v1?city={city}"

city_code="130010" #tokyo
#saitama 110010  
#city_name="Saitama"
url=api.format(city=city_code)
response=requests.get(url)
data=json.loads(response.text)



now_hour=datetime.now().hour
if 0 <= now_hour < 6:
    tomorrow_high=data["forecasts"][0]["temperature"]["max"]["celsius"]
    tomorrow_low=data["forecasts"][0]["temperature"]["min"]["celsius"]
else:
    tomorrow_high=data["forecasts"][1]["temperature"]["max"]["celsius"]
    tomorrow_low=data["forecasts"][1]["temperature"]["min"]["celsius"]
    





url_2="https://tenki.jp/live/3/16/47662.html" #tokyo
#3/14/47626.html saitama(kumagaya)
response=requests.get(url_2)
res= BeautifulSoup(response.text,"html.parser")
today_high_data=res.find_all("span",class_="max-min-temp-entry-value red")
today_low_data=res.find_all("span",class_="max-min-temp-entry-value blue")
if 0 <= now_hour < 6:
    today_high=today_high_data[0].string
    today_low=today_low_data[0].string
else:
    today_high=today_high_data[1].string
    today_low=today_low_data[1].string

message_low=""
message_high=""
low_delta=float(tomorrow_low)-float(today_low)
high_delta=float(tomorrow_high)-float(today_high)
if low_delta > 4:
    message_low="明日の朝は今日比べて"+str(abs(round(low_delta)))+"℃暖かいです"
elif low_delta < -4:
    message_low="明日の朝は今日と比べて"+str(abs(round(low_delta)))+"℃寒くなります"

if  high_delta > 4:
    message_high="明日の昼間は今日よりも"+str(abs(round(high_delta)))+"℃暖かくなります"
elif high_delta < -4:
    message_high="明日の昼間は今日よりも"+str(abs(round(high_delta)))+"℃寒いです"

auth =tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)
api=tweepy.API(auth)

if message_low or message_high  !="":
    api.update_status(message_low+" "+message_high)