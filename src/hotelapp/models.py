from django.db import models
import uuid


class City(models.Model):
    code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Highlight(models.Model):
    icon_url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Hotel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    highlights = models.ManyToManyField(Highlight)
    city_code = models.CharField(max_length=3)
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.CharField(max_length=1000)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.city.name}, {self.code})"


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.name} ({self.hotel.name})"
