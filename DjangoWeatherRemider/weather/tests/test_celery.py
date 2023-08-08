from django.core import mail
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from freezegun import freeze_time
from ..models import City, Subscription, User, WeatherData
from ..tasks import check_notification


class CeleryMailTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')
        self.city = City.objects.create(name='Kiev')
        self.weather = WeatherData.objects.create(city=self.city, temperature=25, description='Test Weather')
        self.subscription = Subscription.objects.create(user=self.user, city=self.city, period=1)

    @freeze_time('2023-07-28 12:00:00')
    def test_check_notification_task(self):
        self.subscription.last_notification = timezone.now() - timedelta(hours=2)
        self.subscription.save()

        check_notification()

        self.subscription.refresh_from_db()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(self.subscription.last_notification.date(), timezone.now().date())

