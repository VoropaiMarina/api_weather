from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import logging
import gzip
import requests
import shutil
import tomli

import os

load_dotenv()

def get_weather_forecast(city_name, api_key):
    '''Получает данные из API и возвращает список с содержимым ответа'''
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
            res = requests.get(url, params=params, timeout=2)
        except requests.exceptions.Timeout:
            logging.error("timeout raised, recovering")

        data = res.json()
        weather_city = {}

        for key, value in data.items():
            if isinstance(value, dict):
                # Допишу к каждому ключу нижнего уровня ключ верхнего уровня 
                source = data[key]
                result = {}

                for k, v in source.items():
                    new_key = key + '_' + k
                    result.update({
                        new_key : v
                    })

                weather_city.update(data[key])
            elif isinstance(value, list):
                value = value[0]
                value["weather_id"] = value.pop("id")
                weather_city.update(value)
            else:
                weather_city.update({key:value})
        # Название города есть в name - поэтому его добавлять не стала
        weather_city.update({
            'request_st': datetime.now().timestamp()
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


with open("./city_name.toml", "rb") as file:
    city_names_in_file = tomli.load(file)
    city_names = city_names_in_file['city_names']

if __name__=='__main__':
    api_key = os.getenv('my_api_key')
    weather = get_weather_forecast(city_name=city_names, api_key=api_key)
    convert_list_to_gzip(lst=weather)