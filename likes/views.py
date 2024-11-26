from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from board.models import Board
from .models import Like
from .serializers import LikeSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_likes(request):
    likes = Like.objects.filter(user=request.user)
    serializer = LikeSerializer(likes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_like_status(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    is_liked = Like.objects.filter(user=request.user, board=board).exists()
    return Response({
        "is_liked": is_liked,
        "like_count": board.likes.count()
    })
