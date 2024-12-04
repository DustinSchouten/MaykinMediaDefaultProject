from django.core.management.base import BaseCommand
from hotelapp.data_handler import DataHandler
from hotelapp.models import City


class Command(BaseCommand):
    help = 'This command collects city and hotel data and writes it into the truncated database'

    def handle(self, *args, **kwargs):
        # Truncate the database model before collecting the new data from the API
        City.objects.all().delete()

        # Fetch the data from the specific city and hotel api and write it to the database
        model_names = ['City', 'Hotel']
        for model_name in model_names:
            handler = DataHandler(model_name)
            handler.fetch_data()
            if handler.get_status_code() == 404:
                self.stderr.write('The hotel data could not be retrieved.')
            handler.parse_data()
            handler.write_to_db()
        self.stdout.write('Done!')
