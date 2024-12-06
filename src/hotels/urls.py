from django.urls import path

from . import views

app_name = 'hotels'

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path('hoteldetails/<uuid:uuid>/', views.HotelDetail.as_view(), name='hoteldetails'),
]
