from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.user_profile, name='update_user_details'),
    path('logout/', views.logout_view, name='logout'),  # 추가

]
