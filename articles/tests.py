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
        models.Article.objects.create(
            title= 'test title',
            content_html = '<span>html content</span>',
            content_md = '# md content',
            img_src = 'https://img01.vgtime.com/game/cover/2020/05/13/200513111436256_u59.jpg',
        )
    def test_articles(self):
        # middleware are not supported. 
        # Create an instance of a GET request.
        request = self.factory.get('/api/articles')

        request.user = self.user

        # Use this syntax for class-based views.
        response = views.ArticleList.as_view()(request)
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertEqual(len(response.data), 4, f'raw response: {response.content}')
        self.assertGreaterEqual(response.data['count'], 1)
        self.assertContains(response, 'results', 1)
        # article filter test
        request = self.factory.get('/api/articles', {'title': 'test title'})
        response = views.ArticleList.as_view()(request)
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertContains(response, 'results', 1)
