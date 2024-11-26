from django.db import models
from enum import Enum

class FinanceEndpoint(Enum):
    DEPOSIT_PRODUCTS = "/depositProductsSearch.json"
    SAVINGS_PRODUCTS = "/savingProductsSearch.json"
    ANNUITY_SAVINGS_PRODUCTS = "/annuitySavingProductsSearch.json"
    MORTGAGE_LOAN_PRODUCTS = "/mortgageLoanProductsSearch.json"
    CREDIT_LOAN_PRODUCTS = "/creditLoanProductsSearch.json"
    RENT_HOUSE_LOAN_PRODUCTS = "/rentHouseLoanProductsSearch.json"