from rest_framework import serializers
from .models import Like
from board.serializers import BoardSerializer


class LikeSerializer(serializers.ModelSerializer):
    board = BoardSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'board', 'created_at']
        read_only_fields = ['user']