# FinPoint/finanace/services.py

import requests
import json
from django.conf import settings
from django.shortcuts import get_object_or_404

from board.models import BoardType, Board
from wishlist.models import WishList
from .models import FinanceEndpoint


class FinanceService:
    BASE_URL = "https://finlife.fss.or.kr/finlifeapi"
    API_KEY = settings.FINLIFE_API_KEY

    def get_product_detail(self, endpoint, fin_prdt_cd):
        try:
            # Fetch all products first
            url = f"{self.BASE_URL}{endpoint}?auth={self.API_KEY}&topFinGrpNo=020000&pageNo=1&fin_prdt_cd={fin_prdt_cd}"
            print(url)
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                result = data.get('result', {})
                base_list = result.get('baseList', [])
                option_list = result.get('optionList', [])

                # Find the specific product
                product = None
                for base in base_list:
                    if base.get('fin_prdt_cd') == fin_prdt_cd:
                        product = base
                        break

                if product:
                    # Find matching options for this product
                    product_options = [
                        option for option in option_list
                        if option.get('fin_prdt_cd') == fin_prdt_cd
                    ]
                    product['options'] = product_options
                    return product

            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def process_response(self, response_data, user=None):
        result = response_data.get('result', {})
        base_list = result.get('baseList', [])
        option_list = result.get('optionList', [])

        # If a user is provided, get their wishlist product codes
        wishlist_product_codes = set()
        if user and user.is_authenticated:
            wishlist_product_codes = set(
                WishList.objects.filter(user=user)
                .values_list('fin_prdt_cd', flat=True)
            )

        # Map options to products
        options_map = {}
        for option in option_list:
            product_code = option.get('fin_prdt_cd')
            if product_code not in options_map:
                options_map[product_code] = []
            options_map[product_code].append(option)

        # Add options and is_wished flag to products
        products = []
        for base in base_list:
            product_code = base.get('fin_prdt_cd')
            base['options'] = options_map.get(product_code, [])

            # Add is_wished flag
            base['is_wished'] = product_code in wishlist_product_codes

            products.append(base)

        return products

    def get_finance_products(self, endpoint, top_fin_grp_no, page_no, user=None):
        try:
            url = f"{self.BASE_URL}{endpoint}?auth={self.API_KEY}&topFinGrpNo={top_fin_grp_no}&pageNo={page_no}"
            response = requests.get(url)

            if response.status_code == 200:
                return self.process_response(response.json(), user)
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def get_deposit_products(self, top_fin_grp_no, page_no, user=None):
        return self.get_finance_products(
            FinanceEndpoint.DEPOSIT_PRODUCTS.value,
            top_fin_grp_no,
            page_no,
            user
        )

    def get_savings_products(self, top_fin_grp_no, page_no, user=None):
        return self.get_finance_products(
            FinanceEndpoint.SAVINGS_PRODUCTS.value,
            top_fin_grp_no,
            page_no,
            user
        )
    def get_annuity_savings_products(self, top_fin_grp_no, page_no):
        return self.get_finance_products(FinanceEndpoint.ANNUITY_SAVINGS_PRODUCTS.value, top_fin_grp_no, page_no)

    def get_mortgage_loan_products(self, top_fin_grp_no, page_no):
        return self.get_finance_products(FinanceEndpoint.MORTGAGE_LOAN_PRODUCTS.value, top_fin_grp_no, page_no)

    def get_credit_loan_products(self, top_fin_grp_no, page_no):
        return self.get_finance_products(FinanceEndpoint.CREDIT_LOAN_PRODUCTS.value, top_fin_grp_no, page_no)

    def get_rent_house_loan_products(self, top_fin_grp_no, page_no):
        return self.get_finance_products(FinanceEndpoint.RENT_HOUSE_LOAN_PRODUCTS.value, top_fin_grp_no, page_no)

    def get_board_product_detail(request, board_id):
        # 게시글 정보 가져오기
        board = get_object_or_404(Board, id=board_id)
        finance_service = FinanceService()

        # board.type에 따른 상품 상세 조회 함수 매핑
        product_detail_functions = {
            BoardType.DEPOSIT: finance_service.get_deposit_product_detail,
            BoardType.SAVINGS: finance_service.get_savings_product_detail,
            BoardType.ANNUITY_SAVINGS: finance_service.get_annuity_savings_product_detail,
            BoardType.MORTGAGE_LOAN: finance_service.get_mortgage_loan_product_detail,
            BoardType.CREDIT_LOAN: finance_service.get_credit_loan_product_detail,
            BoardType.RENT_HOUSE_LOAN: finance_service.get_rent_house_loan_product_detail,
        }

        # board.type에 해당하는 상품 상세 조회 함수 가져오기
        get_product_detail = product_detail_functions.get(board.type)

        if get_product_detail:
            # 금융상품 상세 정보 조회
            product_detail = get_product_detail(board.product_code)

            if product_detail:
                return {
                    'board': {
                        'id': board.id,
                        'title': board.title,
                        'content': board.content,
                        'created_at': board.created_at,
                        'user': board.user.username,
                    },
                    'product': product_detail
                }

        return None

    def get_deposit_product_detail(self, fin_prdt_cd):
        return self.get_product_detail(FinanceEndpoint.DEPOSIT_PRODUCTS.value, fin_prdt_cd)

    def get_savings_product_detail(self, fin_prdt_cd):
        return self.get_product_detail(FinanceEndpoint.SAVINGS_PRODUCTS.value, fin_prdt_cd)

    def get_annuity_savings_product_detail(self, fin_prdt_cd):
        return self.get_product_detail(FinanceEndpoint.ANNUITY_SAVINGS_PRODUCTS.value, fin_prdt_cd)

    def get_mortgage_loan_product_detail(self, fin_prdt_cd):
        return self.get_product_detail(FinanceEndpoint.MORTGAGE_LOAN_PRODUCTS.value, fin_prdt_cd)

    def get_credit_loan_product_detail(self, fin_prdt_cd):
        return self.get_product_detail(FinanceEndpoint.CREDIT_LOAN_PRODUCTS.value, fin_prdt_cd)

    def get_rent_house_loan_product_detail(self, fin_prdt_cd):
        return self.get_product_detail(FinanceEndpoint.RENT_HOUSE_LOAN_PRODUCTS.value, fin_prdt_cd)