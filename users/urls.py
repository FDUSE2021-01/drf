from django.urls import path
from users import views

urlpatterns = [
    path('users/register/', views.UserRegister.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]
