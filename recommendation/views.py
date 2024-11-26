from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from recommendation.services.recommendation_service import BankingRecommendationService
from .serializers import RecommendationResponseSerializer


class DepositRecommendationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        service = BankingRecommendationService()
        recommendations = service.get_recommendations_for_user(request.user, "DEPOSIT")
        serializer = RecommendationResponseSerializer(data=recommendations)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SavingsRecommendationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        service = BankingRecommendationService()
        recommendations = service.get_recommendations_for_user(request.user, "SAVINGS")
        serializer = RecommendationResponseSerializer(data=recommendations)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)