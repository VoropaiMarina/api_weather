from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import logging
import gzip
import requests
import shutil
import os

load_dotenv()

def get_weather_forecast(city_name, api_key):
    '''Получает данные из API '''
    weather = []
    url = "http://api.openweathermap.org/data/2.5/weather"
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
    return weather

def convert_list_to_gzip(lst):
    '''Сохраняет список как csv и затем конвертирует в gzip с новым сохранением'''
    df = pd.DataFrame(lst)
    df.to_csv(r"./weather.csv")
    with open('./weather.csv', 'rb') as f_in:
        with gzip.open('./weather.csv.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


with open("./city_name.cfg", "r") as file:
    city_names = file.read().split(',')

if __name__=='__main__':
    api_key = os.getenv('my_api_key')
    weather = get_weather_forecast(city_name=city_names, api_key=api_key)
    convert_list_to_gzip(lst=weather)