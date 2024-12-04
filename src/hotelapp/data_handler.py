import requests
import pandas as pd
from io import StringIO
from decouple import config
from django.apps import apps
from .models import City, Hotel


class DataHandler:
    URL_CITY = config('URL_CITY')
    URL_HOTEL = config('URL_HOTEL')

    def __init__(self, db_model_name):
        """
        Class for handling all data-related actions like fetching, parsing and writing data.
        """

        self.response = None
        self.df = None
        self.db_model_name = db_model_name

    def fetch_data(self):
        """
        Method for retrieving the data from the webserver by performing an authenticated HTTP GET request.
        """

        url = config(f'URL_{self.db_model_name.upper()}')
        headers = {
            "Username": config('URL_USERNAME'),
            "Password": config('URL_PASSWORD')
        }
        try:
            self.response = requests.get(url, headers=headers)
        except:
            self.response = None

    def get_status_code(self):
        return self.response.status_code

    def parse_data(self):
        """
        Method for parsing the raw text response data and transforming it into a pandas dataframe
        """

        data = StringIO(self.response.text)
        if self.db_model_name == 'City':
            self.df = pd.read_csv(data, delimiter=";", header=None, names=['code', 'name'])
        if self.db_model_name == 'Hotel':
            self.df = pd.read_csv(data, delimiter=";", header=None, names=['city_code', 'code', 'name'])

    def write_to_db(self):
        """
        Method for writing the model data into the database.
        """

        if self.db_model_name == 'City':
            for _, row in self.df.iterrows():
                City.objects.create(**row)

        if self.db_model_name == 'Hotel':
            cities = City.objects.all()
            for _, row in self.df.iterrows():
                matching_city = cities.get(code=row['city_code'])
                Hotel.objects.create(**row, city=matching_city)
