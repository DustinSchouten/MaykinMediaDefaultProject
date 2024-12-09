from django.test import TestCase
from django.test import Client
from django.urls import reverse

from bs4 import BeautifulSoup
import pandas as pd

from ..models import City, Hotel, Room
from ..data_handler import DataHandler


class Tests(TestCase):
    def setUp(self):
        self.handler = DataHandler()

    def perform_request(self, method, form_data=None):
        """
        Helper method to perform GET or POST request and return a BeautifulSoup object.
        :param method: 'GET' or 'POST'
        :param form_data: request body with data when method is 'POST'
        :return: A beautifulsoup object
        """

        client = Client()
        url = reverse('hotels:index')
        if method == 'GET':
            response = client.get(url)
        if method == 'POST':
            response = client.post(url, data=form_data)
        html_content = response.content.decode("utf-8")
        return BeautifulSoup(html_content, "html.parser")

    def test_api_connection(self):
        """
        Test if the API requests from both the City and the Hotel data returns status code 200
        """

        self.handler.fetch_city_data()
        self.assertEqual(self.handler.get_status_code(), 200)
        self.handler.fetch_hotel_data()
        self.assertEqual(self.handler.get_status_code(), 200)

    def test_write_to_db(self):
        """
        Test if the number of hotel model objects that will be written into the database equals the number of
        objects that is collected from that database.
        """

        city_data = {'code': ['AMS'], 'name': ['Amsterdam']}
        hotel_data = {'code': ['AMS01', 'AMS02'], 'name': ['Hotel1', 'Hotel2'], 'city_code': ['AMS', 'AMS']}

        df_city = pd.DataFrame(city_data)
        df_hotel = pd.DataFrame(hotel_data)

        self.handler.write_city_data_to_db(df_city)
        self.handler.write_hotel_data_to_db(df_hotel)

        model_objects = Hotel.objects.all()
        self.assertEqual(len(model_objects), 2)

    def test_index_view_get(self):
        """
        Test if the hotel data is correctly rendered in the html template. In this test, a GET request is performed.
        The response HTML template should have all three <li> tags and it should NOT have a 'No hotels found' message.
        """

        # self.write_test_data_to_test_db()
        city_amsterdam = City.objects.create(code="AMS", name="Amsterdam")
        Hotel.objects.create(code="AMS01", name="Hotel1", city=city_amsterdam)
        Hotel.objects.create(code="AMS02", name="Hotel2", city=city_amsterdam)
        city_antwerpen = City.objects.create(code="ANT", name="Antwerpen")
        Hotel.objects.create(code="ANT01", name="Hotel1", city=city_antwerpen)

        # Simulate a GET request and use BeautifulSoup to collect the html content of the response
        soup = self.perform_request('GET')

        # Check if the number of rendered list items (hotel objects) is 3.
        ul_tag = soup.find('ul')
        li_tags = ul_tag.find_all('li')
        self.assertEqual(len(li_tags), 3)

        # Check if the 'No hotels found' message is None.
        p_tag_no_hotels_found_message = soup.find('p', class_='no_hotels_found_message')
        self.assertIsNone(p_tag_no_hotels_found_message)

    def test_index_view_post_valid_city(self):
        """
        Test if the hotel data is correctly rendered in the html template. In this test, a POST request is performed
        with 'Antwerpen' as the city filter in the request body. This city occurs once in the test database.
        The response HTML template should have only one <li> tag and it should NOT have a 'No hotels found' message.
        """

        # self.write_test_data_to_test_db()
        city_amsterdam = City.objects.create(code="AMS", name="Amsterdam")
        Hotel.objects.create(code="AMS01", name="Hotel1", city=city_amsterdam)
        Hotel.objects.create(code="AMS02", name="Hotel2", city=city_amsterdam)
        city_antwerpen = City.objects.create(code="ANT", name="Antwerpen")
        Hotel.objects.create(code="ANT01", name="Hotel1", city=city_antwerpen)

        # Simulate a POST request and use BeautifulSoup to collect the html content of the response
        form_data = {'city': 'Antwerpen'}
        soup = self.perform_request('POST', form_data)

        # Check if the number of rendered list items (hotel objects) is equal to 1.
        ul_tag = soup.find('ul')
        li_tags = ul_tag.find_all('li')
        self.assertEqual(len(li_tags), 1)

        # Check if the 'No hotels found' message is None.
        p_tag_no_hotels_found_message = soup.find('p', class_='no_hotels_found_message')
        self.assertIsNone(p_tag_no_hotels_found_message)

    def test_index_view_post_empty_string(self):
        """
        Test if the hotel data is correctly rendered in the html template. In this test, a POST request is performed
        with an empty string as the city filter in the request body. In case of an invalid form, the response HTML
        template should have all three <li> tags and it should NOT have a 'No hotels found' message.
        """

        # self.write_test_data_to_test_db()
        city_amsterdam = City.objects.create(code="AMS", name="Amsterdam")
        Hotel.objects.create(code="AMS01", name="Hotel1", city=city_amsterdam)
        Hotel.objects.create(code="AMS02", name="Hotel2", city=city_amsterdam)
        city_antwerpen = City.objects.create(code="ANT", name="Antwerpen")
        Hotel.objects.create(code="ANT01", name="Hotel1", city=city_antwerpen)

        # Simulate a POST request and use BeautifulSoup to collect the html content of the response
        form_data = {'city': ''}
        soup = self.perform_request('POST', form_data)

        # Check if the number of rendered list items (hotel objects) is equal to 3.
        ul_tag = soup.find('ul')
        li_tags = ul_tag.find_all('li')
        self.assertEqual(len(li_tags), 3)

        # Check if the 'No hotels found' message is None.
        p_tag_no_hotels_found_message = soup.find('p', class_='no_hotels_found_message')
        self.assertIsNone(p_tag_no_hotels_found_message)

    def test_index_view_post_city_not_found(self):
        """
        Test if the hotel data is correctly rendered in the html template. In this test, a POST request is performed
        with 'Barcelona' as the city filter in the request body. This city does not exist in the test database.
        The response HTML template should have a 'No hotels found' message.
        """

        # self.write_test_data_to_test_db()
        city_amsterdam = City.objects.create(code="AMS", name="Amsterdam")
        Hotel.objects.create(code="AMS01", name="Hotel1", city=city_amsterdam)
        Hotel.objects.create(code="AMS02", name="Hotel2", city=city_amsterdam)
        city_antwerpen = City.objects.create(code="ANT", name="Antwerpen")
        Hotel.objects.create(code="ANT01", name="Hotel1", city=city_antwerpen)

        # Simulate a POST request and use BeautifulSoup to collect the html content of the response
        form_data = {'city': 'Barcelona'}
        soup = self.perform_request('POST', form_data)

        # Check if the 'No hotels found' message is present (not from django.urls import path
        p_tag_no_hotels_found_message = soup.find('p', class_='no_hotels_found_message')
        self.assertIsNotNone(p_tag_no_hotels_found_message)

    def test_smallest_price(self):
        """
        Test if the 'price' property of the Hotel model actually returns the smallest value of all hotel room prices.
        :return:
        """
        city_amsterdam = City.objects.create(code="AMS", name="Amsterdam")
        hotel = Hotel.objects.create(code="AMS01", name="Hotel1", city=city_amsterdam)
        Room.objects.create(hotel=hotel, name='Room1', price=100)
        Room.objects.create(hotel=hotel, name='Room2', price=50)  # <-- This is the smallest value for 'price'
        Room.objects.create(hotel=hotel, name='Room2', price=150)
        self.assertEqual(hotel.price, 50)


    def tearDown(self):
        pass
