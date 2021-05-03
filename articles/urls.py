from django.urls import path, include
from articles import views
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'upload', views.FileViewSet)

urlpatterns = [
    path('gameinfo/', views.SteamGameDetail.as_view()),
    path('articles/', views.ArticleList.as_view()),
    path('articles/<int:pk>/', views.ArticleDetail.as_view()),
    path('upload/', views.FileModelList.as_view()),
    path('upload/<int:pk>/', views.FileModelDetail.as_view()),
    # path('', include(router.urls))
]