import secrets
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from .settings import ninja_knox_settings


class TokenManager(models.Manager):

    def create(
            self, user=None,
            expiry=ninja_knox_settings.KNOX_TOKEN_TTL,
            **kwargs):
        assert user is not None
        if expiry is not None:
            expiry = timezone.now() + expiry
        token = secrets.token_hex(
                    int(ninja_knox_settings.KNOX_MAX_TOKEN_LENGTH / 2))
        return super().create(user=user, expiry=expiry, token=token, **kwargs)


class AbstractToken(models.Model):
    token = models.CharField(
            max_length=ninja_knox_settings.KNOX_MAX_TOKEN_LENGTH,
            db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=False,
                             blank=False,
                             on_delete=models.CASCADE,
                             related_name='auth_tokens')

    created_at = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.id:
            raise Exception(
                    "Cannot update Token Model, create or delete")
        return super().save(*args, **kwargs)

    objects = TokenManager()

    class Meta:
        abstract = True


class AuthToken(AbstractToken):
    class Meta:
        swappable = 'KNOX_TOKEN_MODEL'


class AnonymousUserWithIP(AnonymousUser):
    ip_address: str

    def __init__(self, ip_address):
        super().__init__()
        self.ip_address = ip_address

    def __str__(self):
        return self.ip_address
