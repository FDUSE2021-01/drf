from django.urls import path
from users import views

urlpatterns = [
    # path('users/registration/activate/token', views.TokenRegister.as_view()),
    path('users/registration/', views.UserRegister.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]
