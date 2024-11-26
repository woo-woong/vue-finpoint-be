from .gpt_service import GPTService
from wishlist.models import WishList
from django.db.models import Count
from django.contrib.auth import get_user_model
from collections import defaultdict

class BankingRecommendationService:
    def __init__(self):
        self.gpt_service = GPTService()

    def get_age_group(self, age):
        if age < 20: return "10대"
        elif age < 30: return "20대"
        elif age < 40: return "30대"
        elif age < 50: return "40대"
        elif age < 60:return "50대"
        else: return "60대 이상"

    def analyze_age_group_preferences(self, product_type, exclude_products=None):
        User = get_user_model()
        age_group_preferences = defaultdict(lambda: defaultdict(int))
        product_codes = {}

        wishlists_query = WishList.objects.filter(type=product_type).select_related('user')

        if exclude_products:
            wishlists_query = wishlists_query.exclude(fin_prdt_cd__in=exclude_products)

        for wishlist in wishlists_query:
            user = wishlist.user
            if user.birth_date:
                age = self.gpt_service.get_age_from_birth_date(user.birth_date)
                age_group = self.get_age_group(age)
                age_group_preferences[age_group][wishlist.fin_prdt_nm] += 1
                product_codes[wishlist.fin_prdt_nm] = wishlist.fin_prdt_cd

        return age_group_preferences, product_codes

    def get_top_items(self, preferences_dict, product_codes, n=3):
        sorted_items = sorted(preferences_dict.items(), key=lambda x: x[1], reverse=True)
        return [(name, count, product_codes.get(name)) for name, count in sorted_items[:n]]

    def get_recommendations_for_user(self, user, product_type):
        if user.birth_date:
            age = self.gpt_service.get_age_from_birth_date(user.birth_date)
            age_group = self.get_age_group(age)
        else:
            age_group = "30대"
            age = 35

        # 사용자 프로필 준비
        user_profile = {
            "age": age,
            "age_group": age_group,
            "product_type": product_type,
            "annual_salary": user.annual_salary,
            "asset": user.asset
        }

        # 사용자 인사이트 생성
        user_insights = self.gpt_service.generate_user_insights(user_profile)

        user_wishlist = WishList.objects.filter(user=user, type=product_type)
        user_wishlisted_products = list(user_wishlist.values_list('fin_prdt_cd', flat=True))

        age_group_preferences, product_codes = self.analyze_age_group_preferences(
            product_type,
            exclude_products=user_wishlisted_products
        )

        popular_products = dict(age_group_preferences.get(age_group, {}))

        if not popular_products:
            return {
                "recommendations": [{
                    "financial_advice": f"현재 {product_type} 상품 추천을 위한 데이터가 충분하지 않습니다."
                }],
                "age_group_statistics": {
                    "age_group": age_group,
                    "popular_products": []
                },
                "user_insights": user_insights
            }

        top_items = self.get_top_items(popular_products, product_codes)

        recommendations = []
        for name, count, code in top_items:
            product_info = {
                "fin_prdt_cd": code,
                "fin_prdt_nm": name,
                "count": count
            }

            insights = self.gpt_service.generate_product_insights(product_info, user_profile)

            recommendations.append({
                "fin_prdt_cd": code,
                "fin_prdt_nm": name,
                "count": count,
                "reason": insights['reason'],
                "key_features": insights['key_features']
            })

        return {
            "recommendations": recommendations,
            "age_group_statistics": {
                "age_group": age_group,
                "popular_products": [
                    {
                        "fin_prdt_nm": rec["fin_prdt_nm"],
                        "fin_prdt_cd": rec["fin_prdt_cd"],
                        "count": rec["count"]
                    } for rec in recommendations
                ]
            },
            "user_insights": user_insights
        }


