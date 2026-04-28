from django.db import models
from django.conf import settings
from lakes.models import Lake



class QuizResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    score = models.IntegerField()
    total = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.score}/{self.total}"
        return f"Guest - {self.score}/{self.total}"
    

class QuizAnswer(models.Model):
    result = models.ForeignKey(QuizResult, on_delete=models.CASCADE, related_name="answers")

    question = models.ForeignKey(Lake, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)
    is_correct = models.BooleanField()
