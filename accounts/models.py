#FinPoint/accounts/models

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    detail_address = models.CharField(max_length=255, null=True, blank=True)
    annual_salary = models.DecimalField(
        max_digits=12,  # 최대 12자리
        decimal_places=2,  # 소수점 2자리
        null=True,
        blank=True,
        help_text='연간 급여(원)'
    )
    asset = models.DecimalField(
        max_digits=15,  # 최대 15자리
        decimal_places=2,  # 소수점 2자리
        null=True,
        blank=True,
        help_text='총 자산(원)'
    )

    # email 대신 username을 기본 로그인 필드로 사용
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # email을 required field로 변경