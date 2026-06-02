from django.urls import path
from . import views

app_name = 'detector'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/recommend-songs/', views.recommend_songs_api, name='recommend_songs'),
    path('api/save-detection/', views.save_detection_api, name='save_detection'),
    path('api/get-history/', views.get_history_api, name='get_history'),
]
