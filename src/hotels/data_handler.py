import random

import requests
import pandas as pd
from io import StringIO
from decouple import config

from .models import City, Hotel, Room, Highlight


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
                City.objects.create(code=row['code'], name=row['name'])

        if self.db_model_name == 'Highlight':
            images = ['https://cdn-icons-png.flaticon.com/512/93/93158.png',  # Free wifi icon
                        'https://cdn.iconscout.com/icon/free/png-256/free-parking-icon-download-in-svg-png-gif-file-formats--p-sign-symbol-1214003.png',  # Free parking icon
                        'https://www.shutterstock.com/image-vector/luggage-storage-icon-260nw-631948439.jpg',  # Luggage storage icon
                        'https://static.vecteezy.com/system/resources/previews/000/552/683/non_2x/geo-location-pin-vector-icon.jpg']  # Central location icon
            Highlight.objects.create(icon_url=images[0], name='Free wifi')
            Highlight.objects.create(icon_url=images[1], name='Free parking')
            Highlight.objects.create(icon_url=images[2], name='Luggage storage')
            Highlight.objects.create(icon_url=images[3], name='Central location')

        if self.db_model_name == 'Hotel':
            images = [
                'https://static.vecteezy.com/system/resources/previews/015/694/764/non_2x/skyscraper-hotel-building-flat-cartoon-hand-drawn-illustration-template-with-view-on-city-space-of-street-panorama-design-vector.jpg',
                'https://i.pinimg.com/736x/ba/1b/92/ba1b92fd2141aef3075da367ea805eb4.jpg']
            price = 12.34
            all_highlights = Highlight.objects.all()
            for idx, row in self.df.iterrows():
                matching_city = City.objects.get(code=row['city_code'])
                description = f'This hotel named {row['name']} is the best hotel of {matching_city}'
                is_available = random.choice([True, False])
                image_url = images[idx%2]
                hotel = Hotel(city_code=row['city_code'], code=row['code'], name=row['name'], city=matching_city,
                              description=description, is_available=is_available, price=price, image_url=image_url)
                hotel.save()
                for highlight in all_highlights:
                    if random.random() < 0.5:
                        hotel.highlights.add(highlight)

        if self.db_model_name == 'Room':
            images = ['https://img.freepik.com/free-vector/hotel-double-room-cartoon-illustration_33099-2026.jpg',
                      'https://thumbs.dreamstime.com/b/coastal-hotel-bedroom-sea-view-interior-cartoon-game-background-beachfront-accommodation-scenic-ocean-resort-room-adventure-326426288.jpg',
                      'https://img.freepik.com/premium-vector/cartoon-depiction-contemporary-hotel-bedroom-interior-illuminated-by-nighttime-city-lights_1263357-10258.jpg']
            descriptions = ['Standard hotel room for two persons with all facilities you need',
                            'The room with more comfort',
                            'The best and most luxurious room of the entire hotel!']
            for hotel in Hotel.objects.all():
                Room.objects.create(hotel=hotel, name='Room classic', image_url=images[0], price=12.34,
                                    description=descriptions[0])
                Room.objects.create(hotel=hotel, name='Room comfort', image_url=images[1], price=12.34,
                                    description=descriptions[1])
                Room.objects.create(hotel=hotel, name='Room deluxe', image_url=images[2], price=12.34,
                                    description=descriptions[2])
