from django.urls import path
from .views import DepositRecommendationView, SavingsRecommendationView

urlpatterns = [
    path('recommendations/deposit/', DepositRecommendationView.as_view(), name='deposit-recommendations'),
    path('recommendations/savings/', SavingsRecommendationView.as_view(), name='savings-recommendations'),
]
