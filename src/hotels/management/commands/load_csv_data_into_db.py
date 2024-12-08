from django.core.management.base import BaseCommand

from ...data_handler import DataHandler


class Command(BaseCommand):
    help = 'This command collects city and hotel data and writes it into the database'

    def handle(self, *args, **kwargs):
        # Performing all steps for City data
        handler = DataHandler()
        handler.fetch_city_data()
        if handler.response is None:
            return
        if handler.get_status_code() == 404:
            self.stderr.write(f'The city data could not be retrieved.')
        df_city = handler.parse_city_data()
        handler.write_city_data_to_db(df_city)

        # Performing all steps for Hotel data
        handler = DataHandler()
        handler.fetch_hotel_data()
        if handler.response is None:
            return
        if handler.get_status_code() == 404:
            self.stderr.write(f'The hotel data could not be retrieved.')
        df_hotel = handler.parse_hotel_data()
        handler.write_hotel_data_to_db(df_hotel)

        self.stdout.write('Done!')
