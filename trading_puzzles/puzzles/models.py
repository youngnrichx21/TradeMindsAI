from django.db import models

class Puzzle(models.Model):
    symbol = models.CharField(max_length=10)
    trend_type = models.CharField(max_length=10)
    pre_trend = models.JSONField()
    trend = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.trend_type} - {self.created_at}"
