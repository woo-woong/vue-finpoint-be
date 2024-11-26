from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.board_list_create, name='board-list-create'),
    path('<int:board_id>/', views.board_detail, name='board-detail'),
    path('likes/', views.toggle_like, name='toggle'),

]
