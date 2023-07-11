from django.db import models

class Email(models.Model):
    email = models.EmailField()
    message = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Email - {self.email}"
