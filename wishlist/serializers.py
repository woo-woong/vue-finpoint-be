from rest_framework import serializers

from finance.views import finance_service
from .models import WishList

class WishListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    product_detail = serializers.SerializerMethodField()  # 새로 추가

    class Meta:
        model = WishList
        fields = [
            'id',
            'user_name',
            'fin_prdt_cd',
            'kor_co_nm',
            'fin_prdt_nm',
            'mtrt_int',
            'type',
            'created_at',
            'is_subscribed',
            'product_detail'  # 새로 추가
        ]
        read_only_fields = ['created_at', 'user_name', 'is_subscribed', 'product_detail']

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return WishList.objects.filter(
                user=request.user,
                fin_prdt_cd=obj.fin_prdt_cd
            ).exists()
        return False

    def get_product_detail(self, obj):
        try:
            # 상품 유형에 따라 적절한 상세 API 호출
            if obj.type == 'SAVINGS':
                product_detail = finance_service.get_savings_product_detail(obj.fin_prdt_cd)
            elif obj.type == 'DEPOSIT':
                product_detail = finance_service.get_deposit_product_detail(obj.fin_prdt_cd)
            else:
                return None

            # 만약 product_detail이 None이면 빈 딕셔너리 반환
            return product_detail if product_detail is not None else {}
        except Exception as e:
            # 로깅 또는 에러 처리
            print(f"Error fetching product detail: {e}")
            return {}