from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('finance/', include('finance.urls')),
    path('board/', include('board.urls')),
    path('exchange/', include('exchange_rates.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('api/products/', include('recommendation.urls')),
    path('likes/', include('likes.urls')),
]
