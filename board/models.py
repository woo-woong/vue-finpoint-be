# FinPoint/board/models.py

from django.db import models
from accounts.models import User

class BoardType(models.TextChoices):
    DEPOSIT = 'DEPOSIT', '예금'
    SAVINGS = 'SAVINGS', '적금'
    ANNUITY_SAVINGS = 'ANNUITY_SAVINGS', '연금저축'
    MORTGAGE_LOAN = 'MORTGAGE_LOAN', '주택담보대출'
    CREDIT_LOAN = 'CREDIT_LOAN', '신용대출'
    RENT_HOUSE_LOAN = 'RENT_HOUSE_LOAN', '전세자금대출'

class Board(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    product_code = models.CharField(max_length=100)
    type = models.CharField(
        max_length=20,
        choices=BoardType.choices,
        default=BoardType.DEPOSIT
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def type_lower(self):
        return self.type.lower()