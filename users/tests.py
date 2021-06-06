from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from django.test.utils import get_runner
from django.conf import settings
from . import views, models
import sys
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.views import TokenRefreshView
# Create your tests here.

User = get_user_model()

class SampleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()
        self.user = models.MyUser.objects.create_user(
            username='testuser', email='tester@wanju.monster', password='top_secret')
        self.token = models.ActivationToken.objects.create(user=self.user, activationToken="ABCDE")
    
    def test_api_token(self):    
        request = self.factory.post('/api/token/', {
                'username': 'testuser',
                'password': 'top_secret'
            })
        request.user = self.user
        force_authenticate(request, user=self.user, token=self.token)
        response = views.MyTokenObtainPairView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertEqual(len(response.data), 4, f'raw response: {response.content}')
    
    def test_api_token_fresh(self):    
        request1 = self.factory.post('/api/token/', {
                'username': 'testuser',
                'password': 'top_secret'
            })
        request1.user = self.user
        force_authenticate(request1, user=self.user, token=self.token)
        response1 = views.MyTokenObtainPairView.as_view()(request1)
        self.assertEqual(response1.status_code, 200)
        response1.render()
        refresh = response1.data['refresh']

        request = self.factory.post('/api/token/refresh/', {
                "refresh": refresh})
        request.user = self.user
        force_authenticate(request, user=self.user, token=self.token)
        response = TokenRefreshView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        response.render()
    
    def test_api_token_fresh_fail(self):    
        request = self.factory.post('/api/token/refresh/', {
                "refresh": "ABCDE"})
        request.user = self.user
        force_authenticate(request, user=self.user, token=self.token)
        response = TokenRefreshView.as_view()(request)
        self.assertEqual(response.status_code, 401)
        response.render()

    def test_password_change_fail(self):
        request = self.factory.put('/api/users/password_change', {
                'old_password': 'wrongpass',
                'new_password': 'nyNewPassword'
            })
        request.user = self.user
        force_authenticate(request, user=self.user, token=self.token)
        response = views.UserChangePassword.as_view()(request)
        self.assertEqual(response.status_code, 400)
        response.render()

    def test_password_change_success(self):
        request = self.factory.put('/api/users/password_change', {
                'old_password': 'top_secret',
                'new_password': 'top_secret2'
            })
        request.user = self.user
        force_authenticate(request, user=self.user, token=self.token)
        response = views.UserChangePassword.as_view()(request)
        self.assertEqual(response.status_code, 200)
        response.render()

    def test_registration(self):
        request = self.factory.post('/api/users/registration', {
                'username': 'testuser2',
                'password': 'top_secret',
                'email': 'a@b.com'
            })
        request.user = self.user
        response = views.UserRegister.as_view()(request)
        self.assertEqual(response.status_code, 201)
        response.render()
        self.assertEqual(len(response.data), 15, f'raw response: {response.content}')
        self.assertEqual(response.data['username'], 'testuser2')

    def test_registration_fail(self):    
        request = self.factory.post('/api/users/registration', {
                'username': 'testuser',
                'password': 'top_secret',
                'email': 'a@b.com'
            })
        request.user = self.user
        response = views.UserRegister.as_view()(request)
        self.assertEqual(response.status_code, 400)
        response.render()

    

    def test_api_user_int_get(self):
        request = self.factory.get('/api/users/', kwargs={'pk' :1})
        force_authenticate(request, user=self.user, token=self.token)
        response = views.UserDetail.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertEqual(len(response.data), 15, f'raw response: {response.content}')
        self.assertEqual(response.data['username'], 'testuser')

    def test_api_user_int_put(self):
        request = self.factory.put('/api/users/', {
                'username': 'testuser',
                'password': 'top_secret',
                'email': 'c@d.com'
                })
        force_authenticate(request, user=self.user, token=self.token)
        response = views.UserDetail.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertEqual(len(response.data), 15, f'raw response: {response.content}')
        self.assertEqual(response.data['email'], 'c@d.com')
    
    def test_api_user_int_put(self):
        request = self.factory.put('/api/users/', {
                'username': 'testuser',
                'password': 'top_secret',
                'email': 'c@d.com'
                })
        force_authenticate(request, user=self.user, token=self.token)
        response = views.UserDetail.as_view()(request, pk=5)
        self.assertEqual(response.status_code, 404)

    def test_favorite_articles(self):
        models.Article.objects.create(
            title= 'test title',
            content_html = '<span>html content</span>',
            content_md = '# md content',
            img_src = 'https://img01.vgtime.com/game/cover/2020/05/13/200513111436256_u59.jpg',
        )
        request = self.factory.post('/api/users/fav-articles/', {
                "article_id": "1" 
            })
        force_authenticate(request, user=self.user, token=self.token)
        response = views.UserFavoriteArticlesListCreate.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_favorite_articles(self):
        request = self.factory.post('/api/users/fav-articles/', {
                "article_id": "1" 
            })
        force_authenticate(request, user=self.user, token=self.token)
        response = views.UserFavoriteArticlesListCreate.as_view()(request)
        self.assertEqual(response.status_code, 404)