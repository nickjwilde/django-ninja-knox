"""Default values for app settings. These can
be overriden in your project settings file"""

from datetime import timedelta
from django.conf import settings

DEFAULTS = {
    "KNOX_TOKEN_TTL": timedelta(hours=8),
    "KNOX_MAX_TOKEN_LENGTH": 64,
    "KNOX_TOKEN_MODEL": "ninja_knox.AuthToken",
}


class NinjaKnoxSettings(dict):
    _defaults = DEFAULTS

    def __getattr__(self, name):
        if name not in self._defaults:
            raise AttributeError("%s is not a valid setting" % name)
        # if not overriden, get default
        return getattr(settings, name, self._defaults[name])


ninja_knox_settings = NinjaKnoxSettings()
