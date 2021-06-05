from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from rest_framework.test import APIRequestFactory
from . import views

User = get_user_model()

class SampleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='tester@wanju.monster', password='top_secret')

    def test_articles(self):
        # middleware are not supported. 
        # Create an instance of a GET request.
        request = self.factory.get('/api/articles')

        request.user = self.user


        # Use this syntax for class-based views.
        response = views.ArticleList.as_view()(request)
        self.assertEqual(response.status_code, 200)