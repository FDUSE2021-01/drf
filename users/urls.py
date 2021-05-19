from django.urls import path
from users import views

urlpatterns = [
    # Creating users
    path('users/activation/', views.UserActivation.as_view()),
    path('users/registration/', views.UserRegister.as_view()),

    # Favorites
    path('users/fav-articles/', views.UserFavoriteArticlesListCreate.as_view()),
    path('users/fav-articles/<int:pk>/', views.UserFavoriteArticlesRetrieveDestroy.as_view()),

    # User details
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('users/password_change/', views.UserChangePassword.as_view()),
    # path('users/password_reset/', views.UserResetPassword.as_view()),

    # Verification code
    path('users/postverifycode/<int:pk>/', views.UserPostVerifycode.as_view()),
    path('users/dealverifycode/', views.UserDealVerifycode.as_view()),
]
