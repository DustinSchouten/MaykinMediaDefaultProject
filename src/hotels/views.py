from datetime import datetime

from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, FormView
from django.urls import reverse

from .models import City, Hotel, Reservation
from .forms import CityForm, ReservationForm1, ReservationForm2


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


class ReservationStep1(FormView):
    form_class = ReservationForm1
    template_name = 'hotels/reservation/step_1.html'

    def get_success_url(self):
        uuid = self.kwargs['uuid']
        return reverse('hotels:reservation_step_2', kwargs={'uuid': uuid})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the hotel object and pass it to the context
        hotel_uuid = self.kwargs.get('uuid')
        hotel_object = Hotel.objects.get(uuid=hotel_uuid)
        context["hotel_object"] = hotel_object

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        # Get all room choices that belongs to the selected hotel object
        hotel_uuid = self.kwargs.get('uuid')
        hotel_object = Hotel.objects.get(uuid=hotel_uuid)
        room_choices = [(obj.id, obj.name) for obj in hotel_object.rooms.all()]

        # Pass the room choices to kwargs so that it can be accessed into the forms.py
        kwargs['room_choices'] = room_choices
        return kwargs

    def form_valid(self, form):
        form_data = form.cleaned_data
        # Get the right room object, calculate some fields and store them in a session
        hotel_uuid = self.kwargs.get('uuid')
        hotel_object = Hotel.objects.get(uuid=hotel_uuid)
        room_object = hotel_object.rooms.get(id=form_data['hotel_room'])
        room_nights = (form_data['end_date'] - form_data['start_date']).days
        room_total_costs = room_nights * room_object.price

        self.request.session.update({
            'hotel_name': str(hotel_object.name),
            'room_name': str(room_object.name),
            'room_total_costs': str(room_total_costs),
            'start_date': form_data['start_date'].strftime("%d-%m-%Y"),
            'end_date': form_data['end_date'].strftime("%d-%m-%Y")
        })
        return super().form_valid(form)


class ReservationStep2(FormView):
    form_class = ReservationForm2
    template_name = 'hotels/reservation/step_2.html'
    success_url = '/reservation_successful'

    def form_valid(self, form):
        # Collect the data of the first reservation page which is stored in a session
        session_data = dict(self.request.session)
        # Collect the formdata of the second reservation page
        form_data = form.cleaned_data
        # Create a new Reservation object with all collected data and store it into the database
        Reservation.objects.create(hotel_room=session_data['room_name'],
                                   start_date=datetime.strptime(session_data['start_date'], '%d-%m-%Y').date(),
                                   end_date=datetime.strptime(session_data['end_date'], '%d-%m-%Y').date(),
                                   first_name=form_data['first_name'], last_name=form_data['last_name'],
                                   email_address= form_data['email_address'], address=form_data['address'],
                                   postal_code=form_data['postal_code'], country=form_data['country'])
        # Clear the session after storing the data
        self.request.session.clear()

        return super().form_valid(form)


class ReservationSuccessful(View):
    def get(self, request):
        return render(request, "hotels/reservation_successful.html")
