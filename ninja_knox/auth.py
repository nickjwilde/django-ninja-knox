from django.contrib.auth import get_user_model
from django.utils import timezone
from ninja_knox.models import AuthToken, AnonymousUserWithIP
from ninja.security import HttpBasicAuth, HttpBearer


class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        user_model = get_user_model()
        user = user_model.objects\
            .filter(**{user_model.USERNAME_FIELD: username})\
            .first()
        if user:
            if user_model\
                    .check_password(user, password):
                return user
            else:
                return False
        return False


class TokenAuth(HttpBearer):
    def authenticate(self, request, token):
        token_obj = AuthToken.objects\
            .filter(token=token)\
            .prefetch_related('user')\
            .first()
        print(token_obj)
        if token_obj:
            # clean up expired tokens
            token_obj.user.auth_tokens\
                .exclude(token=token)\
                .filter(expiry__lt=timezone.now())\
                .delete()
            return token_obj
        return None


def anonymous_auth(request):
    ip = request.META["REMOTE_ADDR"]
    return AnonymousUserWithIP(ip)
