from django.urls import path
from users import views

urlpatterns = [
    path('users/activation/', views.UserActivation.as_view()),
    path('users/registration/', views.UserRegister.as_view()),
    path('users/fav-articles/', views.UserFavoriteArticlesCreate.as_view()),
    path('users/fav-articles/<int:pk>/', views.UserFavoriteArticlesRetrieveDestroy.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('users/postverifycode/<int:pk>/', views.UserPostVerifycode.as_view()),
    path('users/dealverifycode/', views.UserDealVerifycode.as_view()),
]
