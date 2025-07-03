from .auth import BasicAuth
from .models import AuthToken
from .schemas import AuthTokenShema
from .router import router


def login(request):
    user = request.auth
    token = AuthToken.objects.create(user=user)
    return token


router.post("/login", auth=BasicAuth(), response=AuthTokenShema)(login)


def logout(request):
    token = request.auth
    token.delete()
    return 204, None


router.post("/logout", response={204: None})(logout)


def logoutall(request):
    user = request.auth.user
    user.auth_tokens.all().delete()
    return 204, None


router.post("/logoutall", response={204: None})(logoutall)
