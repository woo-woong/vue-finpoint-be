from django.urls import path
from . import views

app_name = 'likes'

urlpatterns = [
    path('my-likes/', views.get_user_likes, name='my-likes'),
    path('check/<int:board_id>/', views.check_like_status, name='check-status'),
]