from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Subscription, City, WeatherData


class ModelCreationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', email='test@gmail.com')
        self.city = City.objects.create(name='Kiev')
        self.subscription = Subscription.objects.create(user=self.user, city=self.city, period=1)
        self.weather = WeatherData.objects.create(city=self.city, temperature='30', description='text')

    def test_add_in_bd(self):
        self.assertEqual(len(City.objects.all()), 1)
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(len(Subscription.objects.all()), 1)
        self.assertEqual(len(WeatherData.objects.all()), 1)

    def test_delete_bd(self):
        weather = WeatherData.objects.first()
        weather.delete()
        self.assertFalse(WeatherData.objects.exists())
        subscription = Subscription.objects.first()
        subscription.delete()
        self.assertFalse(Subscription.objects.exists())
        city = City.objects.first()
        city.delete()
        self.assertFalse(City.objects.exists())
        user = User.objects.first()
        user.delete()
        self.assertFalse(User.objects.exists())
