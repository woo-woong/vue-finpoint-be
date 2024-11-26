from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('deposit/', views.get_deposit_products, name='deposit'),
    path('savings/', views.get_savings_products, name='savings'),
    path('annuity-savings/', views.get_annuity_savings_products, name='annuity-savings'),
    path('mortgage-loan/', views.get_mortgage_loan_products, name='mortgage-loan'),
    path('credit-loan/', views.get_credit_loan_products, name='credit-loan'),
    path('rent-house-loan/', views.get_rent_house_loan_products, name='rent-house-loan'),
    path('deposit/<str:fin_prdt_cd>/', views.get_deposit_product_detail, name='deposit-detail'),
    path('savings/<str:fin_prdt_cd>/', views.get_savings_product_detail, name='savings-detail'),
    path('annuity-savings/<str:fin_prdt_cd>/', views.get_annuity_savings_product_detail, name='annuity-savings-detail'),
    path('mortgage-loan/<str:fin_prdt_cd>/', views.get_mortgage_loan_product_detail, name='mortgage-loan-detail'),
    path('credit-loan/<str:fin_prdt_cd>/', views.get_credit_loan_product_detail, name='credit-loan-detail'),
    path('rent-house-loan/<str:fin_prdt_cd>/', views.get_rent_house_loan_product_detail, name='rent-house-loan-detail'),
    # path('board-product/<int:board_id>/', views.get_board_product_detail, name='board-product-detail'),


]
