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
