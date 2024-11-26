# FinPoint/wishlist/views.py
from sqlite3 import IntegrityError

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from finance.views import finance_service
from . import serializers
from .models import WishList
from .serializers import WishListSerializer


class WishListViewSet(viewsets.ModelViewSet):
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WishList.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise serializers.ValidationError({"detail": "이미 찜한 상품입니다."})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {"detail": "삭제 권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        return Response(
            {"detail": "성공적으로 삭제되었습니다."},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['delete'])
    def remove_by_product(self, request):
        fin_prdt_cd = request.query_params.get('fin_prdt_cd')
        if not fin_prdt_cd:
            return Response(
                {"detail": "상품 코드가 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        wishlist_item = get_object_or_404(
            WishList,
            user=request.user,
            product_code=fin_prdt_cd
        )
        wishlist_item.delete()

        return Response(
            {"detail": "성공적으로 삭제되었습니다."},
            status=status.HTTP_204_NO_CONTENT
        )