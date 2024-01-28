from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    verify_code = models.CharField(max_length=12, verbose_name='Код верификации', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активный')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            ('set_is_active', 'Может блокировать пользователя')
        ]
