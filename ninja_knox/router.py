from ninja import Router
from .auth import TokenAuth

router = Router(auth=TokenAuth())
