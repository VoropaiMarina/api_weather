from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import logging
import gzip
import requests
import shutil
import os

with open("./city_name.cfg", "r") as file:
    city_name = list(file.read().split(','))

url = "http://api.openweathermap.org/data/2.5/weather"
load_dotenv()
api_key = os.getenv('my_api_key')

weather = []
for city in city_name:
    params = {
        'q': city,
        'units': 'metric',
        'lang': 'ru',
        'APPID': api_key
    }
    
    try:
        res = requests.get(url, params=params, timeout=1)
    except requests.exceptions.Timeout:
        logging.error("timeout raised, recovering")

    data = res.json()
    weather_city = {}
    for key, value in data.items():
        if isinstance(value, dict):
            weather_city.update(data[key])
        elif isinstance(value, list):
            value = value[0]
            weather_city.update(value)
        else:
            weather_city.update({key:value})
    # Название города есть в name - поэтому его добавлять не стала
    weather_city.update({
        'measuring_dt': datetime.now().timestamp()
    })
    
    weather.append(weather_city)
print(type(weather))
# df = pd.DataFrame(weather)
# df.to_csv(r"./weather.csv")

# with open('./weather.csv', 'rb') as f_in:
#     with gzip.open('./weather.csv.gz', 'wb') as f_out:
#         shutil.copyfileobj(f_in, f_out)