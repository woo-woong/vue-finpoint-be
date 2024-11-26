import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import urllib3

# SSL 경고 메시지 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_exchange_data_for_date(search_date):
    """특정 날짜의 환율 정보를 조회하는 함수"""
    url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
    params = {
        'authkey': settings.EXCHANGE_API_KEY,
        'searchdate': search_date.strftime('%Y%m%d'),
        'data': 'AP01'
    }

    try:
        response = requests.get(url, params=params, verify=False, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data:  # 데이터가 존재하면 반환
                return data
    except Exception as e:
        print(f"환율 정보 조회 중 오류 발생: {e}")
    return None


def get_latest_exchange_data(start_date):
    """최근 10일 이내의 유효한 환율 정보를 찾는 함수"""
    current_date = start_date
    for _ in range(10):  # 최대 10일 전까지 확인
        data = get_exchange_data_for_date(current_date)
        if data:
            return data, current_date
        current_date -= timedelta(days=1)
    return None, None


@api_view(['GET'])
def get_exchange_rates(request):
    try:
        # 캐시 키 생성
        today = datetime.now()
        cache_key = f"exchange_rates_{today.strftime('%Y%m%d')}"

        # 캐시된 데이터 확인
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        # 오늘 날짜부터 시작하여 최근 유효한 환율 정보 조회
        data, valid_date = get_latest_exchange_data(today)

        if data:
            # 캐시에 저장 (24시간)
            cache.set(cache_key, data, 60 * 60 * 24)
            return Response(data)

        return Response(
            {"message": "최근 10일 이내의 환율 정보를 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND
        )

    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return Response(
            {"message": f"네트워크 오류: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return Response(
            {"message": f"오류가 발생했습니다: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def get_exchange_rates_data():
    """환율 정보를 가져오는 함수"""
    today = datetime.now()
    cache_key = f"exchange_rates_{today.strftime('%Y%m%d')}"
    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data

    data, valid_date = get_latest_exchange_data(today)
    if data:
        cache.set(cache_key, data, 60 * 60 * 24)  # 24시간 캐시
        return data
    return []


@api_view(['GET'])
def calculate_exchange_rate(request):
    """
    from_currency: 시작 통화 (예: AUD)
    to_currency: 목표 통화 (예: AED)
    amount: 환전할 금액 (예: 100)
    """
    try:
        from_currency = request.GET.get('from', '').upper()
        to_currency = request.GET.get('to', '').upper()
        amount = float(request.GET.get('amount', 0))

        if not all([from_currency, to_currency, amount]):
            return Response(
                {"message": "필수 파라미터가 누락되었습니다. (from, to, amount)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 환율 정보 가져오기
        rates_data = get_exchange_rates_data()

        if not rates_data:
            return Response(
                {"message": "환율 정보를 가져오는데 실패했습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 통화별 환율 정보 찾기
        from_rate = next((rate for rate in rates_data if rate['cur_unit'] == from_currency), None)
        to_rate = next((rate for rate in rates_data if rate['cur_unit'] == to_currency), None)

        if not from_rate or not to_rate:
            return Response(
                {"message": "유효하지 않은 통화 코드입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 기준 환율 추출 (쉼표 제거 후 float로 변환)
        from_rate_value = float(from_rate['deal_bas_r'].replace(',', ''))
        to_rate_value = float(to_rate['deal_bas_r'].replace(',', ''))

        # 크로스 환율 계산
        krw_amount = amount * from_rate_value
        target_amount = krw_amount / to_rate_value

        result = {
            'from_currency': from_currency,
            'to_currency': to_currency,
            'amount': amount,
            'result': round(target_amount, 2),
            'rate': round(from_rate_value / to_rate_value, 4),
            'date': datetime.now().strftime('%Y-%m-%d')
        }

        return Response(result)

    except Exception as e:
        return Response(
            {"message": f"오류가 발생했습니다: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )