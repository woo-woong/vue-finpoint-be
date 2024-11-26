from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WishListViewSet

app_name = 'wishlist'

router = DefaultRouter()
router.register(r'', WishListViewSet, basename='wishlist')

urlpatterns = [
    path('', include(router.urls)),
]