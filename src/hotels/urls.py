from django.urls import path

from . import views

app_name = 'hotels'

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path('hoteldetails/<uuid:uuid>/', views.HotelDetail.as_view(), name='hoteldetails'),
    path('hoteldetails/<uuid:uuid>/reservation/step1/', views.ReservationStep1.as_view(), name='reservation_step_1'),
    path('hoteldetails/<uuid:uuid>/reservation/step2/', views.ReservationStep2.as_view(), name='reservation_step_2'),
    path('reservation_successful/', views.ReservationSuccessful.as_view(), name='reservation_successful'),
]
