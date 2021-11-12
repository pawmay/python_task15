from datetime import datetime
import requests
import sys
from os.path import exists, abspath, dirname, join
import json

class WeatherForecast:

    BASE_URL = 'http://api.weatherapi.com/v1/history.json'

    def __init__(self, api_key):
        self.api_key = api_key
        self.cache_path = join(dirname(abspath(__file__)),'cache.txt')
        # zaladowanie cache'a
        if exists(self.cache_path):
            with open(self.cache_path, 'r') as file:
                self.cache = json.loads(file.read())
        else:
            self.cache = {}

    def get_data(self, date=str(datetime.today().date())):
        request_url = f'{self.BASE_URL}?key={self.api_key}&q=Warsaw&dt={date}'
        r = requests.get(request_url)
        self.data = r.json()

    def get_rain_info(self):
        if 'forecast' in self.data:
            totalprecip_mm = float(self.data['forecast']['forecastday'][0]['day']['totalprecip_mm'])
            return self.get_rain_chance(totalprecip_mm)
        return 'Nie wiem!'

    def get_rain_chance(self, totalprecip_mm):
        if totalprecip_mm > 0.0:
            return "Będzie padać"
        elif totalprecip_mm == 0.0:
            return "Nie będzie padać"
        return "Nie wiem!"

    def __getitem__(self, date=str(datetime.today().date())):
        if date in self.cache:
            return self.cache[date]
        self.get_data(date)
        new_value = self.get_rain_info()

        self.cache[date] = new_value

        with open(self.cache_path, 'w') as file:
            file.write(json.dumps(self.cache))
        return new_value

wf = WeatherForecast(api_key=sys.argv[1])
print(wf[sys.argv[2]])