import pytest
from ninja_knox.models import AuthToken

@pytest.mark.django_db
class TestTokenModel:
    def test_no_expiry(self, get_test_user):
        user = get_test_user(1)
        token = AuthToken.objects.create(user=user, expiry=None)
        assert token.expiry is None

    def test_raise_on_update(self):
        token= AuthToken.objects.get(pk=1)
        with pytest.raises(Exception) as ex_info:
            token.save()
        assert ex_info.value.args[0] == "Cannot update Token Model, only create and delete methods"

