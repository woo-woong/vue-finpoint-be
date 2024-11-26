from django.shortcuts import get_object_or_404
import requests  # 외부 라이브러리 requests를 가져옵니다.
# FinPoint/finance/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from wishlist.models import WishList
from .services import FinanceService
from board.models import BoardType, Board

finance_service = FinanceService()


@api_view(['GET'])
def get_deposit_products(request):
    top_fin_grp_no = request.GET.get('topFinGrpNo')
    page_no = int(request.GET.get('pageNo', 1))

    # Pass the current user to the service method
    products = finance_service.get_deposit_products(
        top_fin_grp_no,
        page_no,
        user=request.user
    )

    if products is not None:
        return Response(products)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_savings_products(request):
    top_fin_grp_no = request.GET.get('topFinGrpNo')
    page_no = int(request.GET.get('pageNo', 1))

    # Pass the current user to the service method
    products = finance_service.get_savings_products(
        top_fin_grp_no,
        page_no,
        user=request.user
    )

    if products is not None:
        return Response(products)
    return Response(status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def get_annuity_savings_products(request):
    top_fin_grp_no = request.GET.get('topFinGrpNo')
    page_no = int(request.GET.get('pageNo', 1))

    products = finance_service.get_annuity_savings_products(top_fin_grp_no, page_no)
    if products is not None:
        return Response(products)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_mortgage_loan_products(request):
    top_fin_grp_no = request.GET.get('topFinGrpNo')
    page_no = int(request.GET.get('pageNo', 1))

    products = finance_service.get_mortgage_loan_products(top_fin_grp_no, page_no)
    if products is not None:
        return Response(products)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_credit_loan_products(request):
    top_fin_grp_no = request.GET.get('topFinGrpNo')
    page_no = int(request.GET.get('pageNo', 1))

    products = finance_service.get_credit_loan_products(top_fin_grp_no, page_no)
    if products is not None:
        return Response(products)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_rent_house_loan_products(request):
    top_fin_grp_no = request.GET.get('topFinGrpNo')
    page_no = int(request.GET.get('pageNo', 1))

    products = finance_service.get_rent_house_loan_products(top_fin_grp_no, page_no)
    if products is not None:
        return Response(products)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_deposit_product_detail(request, fin_prdt_cd):
    product = finance_service.get_deposit_product_detail(fin_prdt_cd)
    print(product)

    if product is not None:
        # 인증된 사용자인 경우에만 is_subscribed 확인
        if request.user.is_authenticated:
            wishlist_item = WishList.objects.filter(
                user=request.user,
                fin_prdt_cd=fin_prdt_cd
            ).first()

            if wishlist_item:
                product['is_subscribed'] = True
                product['wishlist_id'] = wishlist_item.id
            else:
                product['is_subscribed'] = False
                product['wishlist_id'] = None
        else:
            product['is_subscribed'] = False
            product['wishlist_id'] = None

        return Response(product)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_savings_product_detail(request, fin_prdt_cd):
    product = finance_service.get_savings_product_detail(fin_prdt_cd)
    if product is not None:
        # 인증된 사용자인 경우에만 is_subscribed 확인
        if request.user.is_authenticated:
            wishlist_item = WishList.objects.filter(
                user=request.user,
                fin_prdt_cd=fin_prdt_cd
            ).first()

            if wishlist_item:
                product['is_subscribed'] = True
                product['wishlist_id'] = wishlist_item.id
            else:
                product['is_subscribed'] = False
                product['wishlist_id'] = None
        else:
            product['is_subscribed'] = False
            product['wishlist_id'] = None

        return Response(product)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_annuity_savings_product_detail(request, fin_prdt_cd):
    product = finance_service.get_annuity_savings_product_detail(fin_prdt_cd)
    if product is not None:
        return Response(product)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_mortgage_loan_product_detail(request, fin_prdt_cd):
    product = finance_service.get_mortgage_loan_product_detail(fin_prdt_cd)
    if product is not None:
        return Response(product)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_credit_loan_product_detail(request, fin_prdt_cd):
    product = finance_service.get_credit_loan_product_detail(fin_prdt_cd)
    if product is not None:
        return Response(product)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_rent_house_loan_product_detail(request, fin_prdt_cd):
    product = finance_service.get_rent_house_loan_product_detail(fin_prdt_cd)
    if product is not None:
        return Response(product)
    return Response(status=status.HTTP_404_NOT_FOUND)


