from rest_framework import serializers

class RecommendationSerializer(serializers.Serializer):
    fin_prdt_cd = serializers.CharField()
    fin_prdt_nm = serializers.CharField()
    count = serializers.IntegerField()
    reason = serializers.CharField()
    key_features = serializers.ListField(child=serializers.CharField())

class PopularProductSerializer(serializers.Serializer):
    fin_prdt_nm = serializers.CharField()
    fin_prdt_cd = serializers.CharField()
    count = serializers.IntegerField()

class AgeGroupStatisticsSerializer(serializers.Serializer):
    age_group = serializers.CharField()
    popular_products = PopularProductSerializer(many=True)

class UserInsightsSerializer(serializers.Serializer):
    age_based_insight = serializers.CharField()
    general_advice = serializers.CharField()

class RecommendationResponseSerializer(serializers.Serializer):
    recommendations = RecommendationSerializer(many=True)
    age_group_statistics = AgeGroupStatisticsSerializer()
    user_insights = UserInsightsSerializer()