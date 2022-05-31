from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN_ROLE_NAME = 'admin'
MODERATOR_ROLE_NAME = 'moderator'
USER_ROLE_NAME = 'user'

USER_ROLE = (
    (ADMIN_ROLE_NAME, 'admin'),
    (MODERATOR_ROLE_NAME, 'moderator'),
    (USER_ROLE_NAME, 'user'),
)


class User(AbstractUser):
    """Кастомизируем модель User."""
    password = models.CharField(
        help_text='password',
        null=True,
        max_length=128,
        blank=True,
        verbose_name='Пароль'
    )
    role = models.CharField(
        help_text='role',
        choices=USER_ROLE,
        max_length=20,
        verbose_name='Роль',
        default='user'
    )
    bio = models.TextField(
        help_text='bio',
        blank=True,
        verbose_name='Биография'
    )

    @property
    def is_moderator(self):
        return self.role == MODERATOR_ROLE_NAME

    class Meta:
        ordering = ('-date_joined',)
        verbose_name = 'User'
        verbose_name_plural = 'User'

    def save(self, *args, **kwargs):
        if self.role == ADMIN_ROLE_NAME:
            self.is_staff = True
        super().save(*args, **kwargs)
