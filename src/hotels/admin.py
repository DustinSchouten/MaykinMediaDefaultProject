from django.contrib import admin

from .models import City, Hotel, Room, Highlight

# Register your models here.

admin.site.register(City)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Highlight)
