from datetime import date
import json
import openai
from django.conf import settings
import re

class GPTService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    def get_age_from_birth_date(self, birth_date):
        today = date.today()
        age = today.year - birth_date.year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        return age

    def _clean_and_parse_json(self, content):
        """
        GPT 응답을 정제하고 JSON으로 파싱하는 헬퍼 메서드
        """
        try:
            # 코바꿈 문자를 공백으로 대체
            content = ' '.join(content.split())
            
            # 코드 블록 마커 제거
            content = re.sub(r'```json\s*', '', content)
            content = re.sub(r'```\s*', '', content)
            
            # JSON 객체 추출 (마지막 완전한 JSON 객체 사용)
            json_matches = list(re.finditer(r'\{[^{]*?\}', content))
            if not json_matches:
                raise ValueError("JSON 객체를 찾을 수 없습니다")
            
            # 마지막으로 발견된 완전한 JSON 사용
            last_json = json_matches[-1].group()
            
            # 작은따옴표를 큰따옴표로 변경
            last_json = last_json.replace("'", '"')
            
            # 후행 쉼표 제거
            last_json = re.sub(r',(\s*[}\]])', r'\1', last_json)
            
            # JSON 파싱
            parsed_data = json.loads(last_json)
            
            return parsed_data

        except Exception as e:
            print(f"JSON 파싱 오류: {str(e)}")
            print(f"문제의 콘텐츠: {content}")
            return None

    def generate_user_insights(self, user_profile):
        prompt = f"""
        다음 사용자의 연령대별 금융 인사이트와 조언을 생성해주세요.
        각 응답은 200자 이내로 작성해주세요:

        사용자 정보:
        - 나이: {user_profile['age']}
        - 연령대: {user_profile['age_group']}
        - 연간 소득: {user_profile.get('annual_salary', '정보 없음')}
        - 총 자산: {user_profile.get('asset', '정보 없음')}

        다음 형식으로만 답변하세요:
        {{
            "age_based_insight": "200자 이내의 연령대별 금융 특성 인사이트",
            "general_advice": "200자 이내의 맞춤형 재무 조언"
        }}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 금융 상품 추천 전문가입니다. 50자 이내의 간단명료한 JSON 형식으로만 답변하세요."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )

            content = response.choices[0].message.content.strip()
            parsed_response = self._clean_and_parse_json(content)
            
            if parsed_response:
                return parsed_response
            
            # 파싱 실패시 기본 응답 반환
            return {
                "age_based_insight": f"{user_profile['age_group']}의 일반적인 금융 특성에 대한 인사이트입니다.",
                "general_advice": "장기적인 재무 계획을 세우는 것이 중요합니다."
            }

        except Exception as e:
            print(f"GPT API 오류: {str(e)}")
            return {
                "age_based_insight": f"{user_profile['age_group']}의 일반적인 금융 특성에 대한 인사이트입니다.",
                "general_advice": "장기적인 재무 계획을 세우는 것이 중요합니다."
            }

    def generate_product_insights(self, product_info, user_profile):
        product_type_kr = "예금" if user_profile['product_type'] == "DEPOSIT" else "적금"
        
        prompt = f"""
        다음 {product_type_kr} 상품에 대한 추천 이유를 150자 이내로 생성해주세요:

        사용자 정보:
        - 나이: {user_profile['age']}
        - 연령대: {user_profile['age_group']}
        - 연간 소득: {user_profile.get('annual_salary', '정보 없음')}
        - 총 자산: {user_profile.get('asset', '정보 없음')}

        상품명: {product_info['fin_prdt_nm']}
        선호도: {product_info['count']}명의 유사한 프로필을 가진 사용자가 관심

        다음 형식으로만 답변하세요:
        {{
            "reason": "150자 이내의 추천 이유",
            "key_features": ["20자 이내의 특징1", "20자 이내의 특징2", "20자 이내의 특징3"]
        }}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 금융 상품 추천 전문가입니다. 매우 간단명료하게 답변하세요."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )



            content = response.choices[0].message.content.strip()
            parsed_response = self._clean_and_parse_json(content)
            
            if parsed_response:
                return parsed_response

            # 파싱 실패시 기본 응답 반환
            return {
                "reason": f"이 상품은 {user_profile['age_group']} 연령대에 적합한 {product_type_kr} 상품입니다.",
                "key_features": ["안정적인 수익률", "편리한 거래 방식"]
            }

        except Exception as e:
            print(f"GPT API 오류: {str(e)}")
            return {
                "reason": f"이 상품은 {user_profile['age_group']} 연령대에 적합한 {product_type_kr} 상품입니다.",
                "key_features": ["안정적인 수익률", "편리한 거래 방식"]
            }
            
    

