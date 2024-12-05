from django.urls import path
from . import views

app_name = 'hotelapp'

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path('hoteldetails/<uuid:uuid>/', views.HotelDetails.as_view(), name='hoteldetails'),
]
