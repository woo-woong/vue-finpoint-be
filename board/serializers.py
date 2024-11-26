from rest_framework import serializers
from .models import Board
from accounts.models import User
from likes.models import Like

class BoardUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name']

class BoardSerializer(serializers.ModelSerializer):
    user = BoardUserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'user', 'title', 'content', 'created_at', 'product_code', 'type', 'like_count', 'is_liked']
        read_only_fields = ['created_at']

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, board=obj).exists()
        return False