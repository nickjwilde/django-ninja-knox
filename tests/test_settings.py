import pytest
from datetime import timedelta
from django.test import override_settings
from ninja_knox.settings import ninja_knox_settings

class TestSettings:
    def test_token_ttl_change(self, settings):
        settings.KNOX_TOKEN_TTL = timedelta(hours=1)
        assert ninja_knox_settings.KNOX_TOKEN_TTL == timedelta(hours=1)

    def test_non_valid_setting_throws(self):
        with pytest.raises(AttributeError) as ex_info:
            ninja_knox_settings.NOT_A_SETTING
        assert ex_info.value.args == ("NOT_A_SETTING is not a valid setting",)

