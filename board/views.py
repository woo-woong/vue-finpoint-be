from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from finance.views import finance_service
from likes.serializers import LikeSerializer
from .serializers import BoardSerializer

from board.models import BoardType, Board
from likes.models import Like  # Like 모델 import 추가

@api_view(['GET'])
@permission_classes([AllowAny])
def board_list(request):
    boards = Board.objects.all()
    serializer = BoardSerializer(boards, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def board_list_create(request):
    if request.method == 'GET':
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def board_product_list(request, product_code):
    boards = Board.objects.filter(product_code=product_code)
    serializer = BoardSerializer(boards, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def board_create(request):
    serializer = BoardSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def board_detail(request, board_id):
    if request.method == 'GET':
        return get_board_detail(request, board_id)
    else:
        return modify_board_detail(request, board_id)


@permission_classes([AllowAny])
def get_board_detail(request, board_id):
    try:
        board = get_object_or_404(Board, id=board_id)

        # 좋아요 관련 정보 추가
        like_count = board.likes.count()  # 전체 좋아요 수
        is_liked = False
        if request.user.is_authenticated:  # 로그인한 사용자인 경우만 체크
            is_liked = Like.objects.filter(user=request.user, board=board).exists()

        type_to_method = {
            BoardType.DEPOSIT: finance_service.get_deposit_product_detail,
            BoardType.SAVINGS: finance_service.get_savings_product_detail,
            BoardType.ANNUITY_SAVINGS: finance_service.get_annuity_savings_product_detail,
            BoardType.MORTGAGE_LOAN: finance_service.get_mortgage_loan_product_detail,
            BoardType.CREDIT_LOAN: finance_service.get_credit_loan_product_detail,
            BoardType.RENT_HOUSE_LOAN: finance_service.get_rent_house_loan_product_detail,
        }

        if board.type not in type_to_method:
            return Response(
                {'error': '유효하지 않은 상품 타입입니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        method = type_to_method[board.type]
        product = method(board.product_code)

        if not product:
            return Response(
                {'error': '상품을 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )

        response_data = {
            'board': {
                'id': board.id,
                'title': board.title,
                'content': board.content,
                'created_at': board.created_at,
                'user': board.user.username,
                'name': board.user.name,
                'type': board.type,
                'product_code': board.product_code,
                'like_count': like_count,  # 좋아요 수 추가
                'is_liked': is_liked,  # 현재 사용자의 좋아요 여부 추가
            },
            'product': product
        }

        return Response(response_data)
    except Board.DoesNotExist:
        return Response(
            {'error': '게시글을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@permission_classes([IsAuthenticated])
def modify_board_detail(request, board_id):
    try:
        board = get_object_or_404(Board, id=board_id)

        # 작성자만 수정/삭제 가능
        if board.user != request.user:
            return Response(
                {"message": "자신이 작성한 게시글만 수정/삭제할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        if request.method == 'PUT':
            serializer = BoardSerializer(board, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            board.delete()
            return Response(
                {"message": "게시글이 성공적으로 삭제되었습니다."},
                status=status.HTTP_204_NO_CONTENT
            )

    except Board.DoesNotExist:
        return Response(
            {'error': '게시글을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def toggle_like(request):
    # POST 요청의 body에서 board_id를 받음
    print("여기로 들어옴")
    if request.method == 'POST':
        board_id = request.data.get('board_id')
        if not board_id:
            return Response({
                "message": "board_id는 필수 항목입니다."
            }, status=status.HTTP_400_BAD_REQUEST)

        board = get_object_or_404(Board, id=board_id)

        try:
            like = Like.objects.get(user=request.user, board=board)
            # 이미 좋아요가 있으면 오류 반환
            return Response({
                "message": "이미 좋아요가 되어있습니다.",
                "like_count": board.likes.count(),
                "is_liked": True
            }, status=status.HTTP_400_BAD_REQUEST)

        except Like.DoesNotExist:
            # 좋아요가 없으면 생성
            like = Like.objects.create(user=request.user, board=board)
            serializer = LikeSerializer(like)
            return Response({
                "message": "좋아요가 추가되었습니다.",
                "like_count": board.likes.count(),
                "is_liked": True,
            }, status=status.HTTP_201_CREATED)

    # DELETE 요청일 경우
    elif request.method == 'DELETE':
        board_id = request.data.get('board_id')
        if not board_id:
            return Response({
                "message": "board_id는 필수 항목입니다."
            }, status=status.HTTP_400_BAD_REQUEST)

        board = get_object_or_404(Board, id=board_id)
        like = Like.objects.filter(user=request.user, board=board).first()

        if like:
            like.delete()
            return Response({
                "message": "좋아요가 취소되었습니다.",
                "like_count": board.likes.count(),
                "is_liked": False
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "취소할 좋아요가 없습니다.",
                "like_count": board.likes.count(),
                "is_liked": False
            }, status=status.HTTP_404_NOT_FOUND)

