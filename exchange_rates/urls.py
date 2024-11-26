# exchange_rates/urls.py

from django.urls import path
from . import views

app_name = 'exchange_rates'

urlpatterns = [
    path('rates/', views.get_exchange_rates, name='exchange-rates'),
    path('calculate/', views.calculate_exchange_rate, name='calculate-exchange'),
]
