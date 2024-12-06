from django.core.management.base import BaseCommand

from ...data_handler import DataHandler
from ...models import City, Room, Highlight


class Command(BaseCommand):
    help = 'This command collects city and hotel data and writes it into the truncated database'

    def perform_model_steps(self, model_name):
        """
        Helper method for performing all steps that are in the data handler like fetching, parsing data and writing
        data to a database.
        :param model_name: string name of model
        """
        handler = DataHandler(model_name)
        # Only for these two models, data is fetched from authenticated server
        if model_name in ['City', 'Hotel']:
            handler.fetch_data()
            if handler.get_status_code() == 404:
                self.stderr.write(f'The {model_name} data could not be retrieved.')
            handler.parse_data()
        handler.write_to_db()

    def handle(self, *args, **kwargs):
        # Truncate the database model before loading new data into the database.
        City.objects.all().delete()
        Room.objects.all().delete()
        Highlight.objects.all().delete()

        # The order of modelnames is very important for loading the tables correctly and it's the same order as the
        # order in models.py
        for model_name in ['City', 'Highlight', 'Hotel', 'Room']:
            self.perform_model_steps(model_name)
        self.stdout.write('Done!')
