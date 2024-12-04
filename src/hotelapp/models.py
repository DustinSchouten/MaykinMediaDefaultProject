from django.db import models

class City(models.Model):
    code = models.CharField(max_length=3, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Hotel(models.Model):
    city = models.ForeignKey(City, max_length=3, on_delete=models.CASCADE)
    city_code = models.CharField(max_length=3, null=True)
    code = models.CharField(max_length=5, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.city.name}, {self.code})"
