from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from .models import City, Hotel
from .forms import CityForm


class Index(View):
    def get(self, request):
        """
        View-method to call when the user lands on the index page.
        :return: The index page
        """

        # Get all hotel objects with all related city objects into it.
        hotel_objects = Hotel.objects.all()

        # Get list with all available city names
        city_names = [c.name for c in City.objects.all()]

        return render(request, "hotels/index.html", {"hotel_objects": hotel_objects, "city_names": city_names})

    def post(self, request):
        """
        View-method to call when the user fetches the data using a city filter. Before the page will be rendered, the
        stored data inside the model will be filtered with the city value.
        :return: The index page or an error page
        """
        city_form = CityForm(request.POST)

        # Get list with all available city names
        city_names = [c.name for c in City.objects.all()]

        if city_form.is_valid():
            city_filter = request.POST['city']

            # Use the city filter to get all hotel objects from that specific city
            hotel_objects = Hotel.objects.filter(city__name=city_filter)

            return render(request, "hotels/index.html", {"hotel_objects": hotel_objects, "city_names": city_names})

        hotel_objects = Hotel.objects.all()

        return render(request, "hotels/index.html", {"hotel_objects": hotel_objects, "city_names": city_names})


class HotelDetail(DetailView):
    model = Hotel
    template_name = 'hotels/hoteldetails.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    context_object_name = 'hotel_object'
