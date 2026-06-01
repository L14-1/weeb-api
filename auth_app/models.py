from django.db import models
from django.contrib.auth.models import User

class Role(models.TextChoices):
    MEMBER = 'member', 'Member'
    ADMIN = 'admin', 'Admin'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)

    def __str__(self):
        return f"{self.user.email} — {self.role}"