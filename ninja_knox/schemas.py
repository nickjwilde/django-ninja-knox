from ninja import ModelSchema
from ninja_knox.models import AuthToken


class AuthTokenShema(ModelSchema):
    class Meta:
        model = AuthToken
        fields = ['token', 'expiry']
