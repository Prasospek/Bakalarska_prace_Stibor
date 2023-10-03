from django.db import models
from django.utils import timezone

class Email(models.Model):
    email = models.EmailField()
    message = models.TextField(default="Message empty")
    sent_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Email - {self.email}"


class Transaction(models.Model):
    ACTION_CHOICES = [
        ('Dividend', 'Dividend'),
        ('MarketSell', 'Market Sell'),
        ('InterestOnCash', 'Interest on Cash'),
        ('Withdrawal', 'Withdrawal'),
    ]
    
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    date = models.DateTimeField()
    isin = models.CharField(max_length=20)
    ticker = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    shares = models.DecimalField(max_digits=10, decimal_places=4)
    price_per_share = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    result = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    withholding_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    charge_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.action} - {self.ticker} - {self.date}"