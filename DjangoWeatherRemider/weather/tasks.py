from DjangoWeatherRemider.celery import app
from django.core.mail import send_mail
from .models import Subscription, WeatherData
from DjangoWeatherRemider.settings import WEATHER_API
from django.utils import timezone
import requests


def send_mail_tack(weather, user):
    send_mail(
        f'Weather notification for {weather.city}',
        f"Температура: {weather.temperature}°C\n{weather.description}",
        'weather@gmail.com',
        [user.email],
        fail_silently=False
    )


def add_subscription_data(city, data):
    description = f"Минимальная температура: {data['main']['temp_min']}°C\n" \
                  f"Максимальная температура: {data['main']['temp_max']}°C"
    if not WeatherData.objects.filter(city=city).exists():
        WeatherData.objects.create(
            city=city,
            temperature=data['main']['temp'],
            description=description
        )
    else:
        weather = WeatherData.objects.filter(city=city).first()
        weather.temperature = data['main']['temp']
        weather.description = description
        weather.save()


@app.task()
def get_city_weather():
    subscribe = Subscription.objects.all()
    for item in subscribe:
        time = timezone.now() - item.last_notification
        hours = time.seconds // 3600
        if item.period <= hours:
            response = requests.get(
                f'http://api.openweathermap.org/data/2.5/weather?q={item.city}&appid={WEATHER_API}&units=metric')
            data = response.json()
            add_subscription_data(item.city, data)
            weather = WeatherData.objects.filter(city=item.city).first()
            send_mail_tack(weather, item.user)
