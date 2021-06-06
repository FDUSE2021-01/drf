from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from django.test.utils import get_runner
from django.conf import settings
from . import views, models
import sys
# Create your tests here.

User = get_user_model()

class SampleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='tester@wanju.monster', password='top_secret')
    def test_password_change(self):
        request = self.factory.put('/api/users/password_change', {
                'old_password': 'wrongpass',
                'new_password': 'nyNewPassword'
            })
        request.user = self.user
        response = views.UserChangePassword.as_view()(request)
        self.assertEqual(response.status_code, 401)
        response.render()