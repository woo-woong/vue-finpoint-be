from django.db import models
from accounts.models import User
from board.models import Board

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'board')  # 한 사용자가 같은 게시글에 좋아요를 두 번 누를 수 없도록

    def __str__(self):
        return f"{self.user.username} likes {self.board.title}"