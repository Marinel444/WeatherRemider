from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    name = models.CharField(max_length=256, blank=False)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    period = models.PositiveIntegerField(choices=[(1, '1 hour'), (3, '3 hours'), (6, '6 hours'), (12, '12 hours')])
    webhook_url = models.URLField(null=True, blank=True)
    email_notification = models.BooleanField(default=False)
    last_notification = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-{self.city}'


class WeatherData(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.temperature}°C"
