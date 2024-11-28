from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout

from wishlist.serializers import WishListSerializer
from .serializers import UserSerializer, UserDetailSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        response_serializer = UserDetailSerializer(user)
        return Response({
            "message": "회원가입이 완료되었습니다.",
            "user": response_serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        serializer = UserDetailSerializer(user)
        response = Response({
            "message": "로그인 성공",
            "user": serializer.data
        })
        
        # 쿠키 설정 추가
        response.set_cookie(
            'sessionid',
            request.session.session_key,
            domain='finpoint-woo-woong.vercel.app',
            secure=True,
            httponly=True,
            samesite='None',
            max_age=60*60*24*14  # 14일
        )
        
        return response
    else:
        return Response({
            "message": "아이디 또는 비밀번호가 잘못되었습니다."
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user

    if request.method == 'GET':
        user_serializer = UserDetailSerializer(user)
        wishlist_serializer = WishListSerializer(user.wishlists.all(), many=True)
        return Response({
            "message": "사용자 정보 조회 성공",
            "user": user_serializer.data,
            "wishlist": wishlist_serializer.data
        })

    elif request.method == 'PUT':
        serializer = UserDetailSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "사용자 정보가 성공적으로 업데이트되었습니다.",
                "user": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({
        "message": "로그아웃되었습니다."
    }, status=status.HTTP_200_OK)