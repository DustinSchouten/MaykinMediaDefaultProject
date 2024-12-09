import requests
import pandas as pd
from io import StringIO
from decouple import config

from .models import City, Hotel


class DataHandler:
    URL_CITY = config('URL_CITY')
    URL_HOTEL = config('URL_HOTEL')

    def __init__(self):
        """
        Class for handling all data-related actions like fetching, parsing and writing data.
        """

        self.response = None
        self.df = None

    def fetch_city_data(self):
        """
        Method for retrieving the City data from the webserver by performing an authenticated HTTP GET request.
        """

        headers = {
            "Username": config('URL_USERNAME'),
            "Password": config('URL_PASSWORD')
        }
        try:
            self.response = requests.get(DataHandler.URL_CITY, headers=headers)
        except:
            self.response = None

    def fetch_hotel_data(self):
        """
        Method for retrieving the Hotel data from the webserver by performing an authenticated HTTP GET request.
        """

        headers = {
            "Username": config('URL_USERNAME'),
            "Password": config('URL_PASSWORD')
        }
        try:
            self.response = requests.get(DataHandler.URL_HOTEL, headers=headers)
        except:
            self.response = None

    def get_status_code(self):
        return self.response.status_code

    def parse_city_data(self):
        """
        Method for parsing the raw City text response data and transforming it into a pandas dataframe
        """

        data = StringIO(self.response.text)
        self.df = pd.read_csv(data, delimiter=";", header=None, names=['code', 'name'])

    def parse_hotel_data(self):
        """
        Method for parsing the raw Hotel text response data and transforming it into a pandas dataframe
        """

        data = StringIO(self.response.text)
        self.df = pd.read_csv(data, delimiter=";", header=None, names=['city_code', 'code', 'name'])

    def write_city_data_to_db(self):
        """
        Method for writing the City model data into the database.
        """

        for _, row in self.df.iterrows():
            City.objects.get_or_create(code=row['code'], name=row['name'])

    def write_hotel_data_to_db(self):
        """
        Method for writing the Hotel model data into the database.
        """

        for _, row in self.df.iterrows():
            matching_city = City.objects.get(code=row['city_code'])
            Hotel.objects.get_or_create(city_code=row['city_code'], code=row['code'], name=row['name'],
                                        city=matching_city, description=None)
