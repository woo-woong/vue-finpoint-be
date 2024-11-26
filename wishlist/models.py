
# FinPoint/wishlist/models.py
from django.db import models
from django.conf import settings

class ProductType(models.TextChoices):
    DEPOSIT = 'DEPOSIT', '예금'
    SAVINGS = 'SAVINGS', '적금'
    ANNUITY_SAVINGS = 'ANNUITY_SAVINGS', '연금저축'
    MORTGAGE_LOAN = 'MORTGAGE_LOAN', '주택담보대출'
    CREDIT_LOAN = 'CREDIT_LOAN', '신용대출'
    RENT_HOUSE_LOAN = 'RENT_HOUSE_LOAN', '전세자금대출'

class WishList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wishlists',
        verbose_name='사용자'
    )
    fin_prdt_cd = models.CharField(max_length=100, verbose_name='상품코드')
    kor_co_nm = models.CharField(max_length=100, verbose_name='은행명')
    fin_prdt_nm = models.CharField(max_length=200, verbose_name='상품명')
    mtrt_int = models.CharField(
        max_length=500,
        verbose_name='만기기간',
        null=True,
        blank=True
    )
    type = models.CharField(
        max_length=20,
        choices=ProductType.choices,
        verbose_name='상품종류'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='찜한 날짜')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '찜 목록'
        verbose_name_plural = '찜 목록'
        unique_together = ['user', 'fin_prdt_cd']  # 사용자별 상품 중복 찜 방지

    def __str__(self):
        return f"{self.user.username} - {self.fin_prdt_nm}"