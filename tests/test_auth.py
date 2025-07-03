import pytest
from django.http import HttpRequest
from ninja_knox.auth import BasicAuth, TokenAuth, anonymous_auth

@pytest.fixture
def basic_auth():
    return BasicAuth()

@pytest.fixture
def token_auth():
    return TokenAuth()

@pytest.mark.django_db
class TestBasicAuth:
    @pytest.mark.parametrize("uname,passwd,expected", [
        ('test', 'test', ("get_test_user", 2)),
        ('test', 'bad_pass', False),
        ('not_found_username', 'test', False),
        ])
    def test_basic_user(self, basic_auth, request, uname, passwd, expected):
        
        result = basic_auth.authenticate(None, uname, passwd)

        if isinstance(expected, bool):
            assert result == expected
        else:
            get_user, id = expected
            assert result == request.getfixturevalue(get_user)(id)

@pytest.mark.django_db
class TestTokenAuth:
    @pytest.mark.parametrize("token,expected", [
        ('test_user_token', 'test_user_token'),
        ('not_found_token', None)
    ])
    def test_token_auth(self, token_auth: TokenAuth, token: str, expected: str|None):
        result = token_auth.authenticate(None, token)
        if result:
            assert result.token == expected
        else:
            assert not result

class TestAnonymousAuth:
    def test_anon_auth(self):
        request = HttpRequest()
        request.META['REMOTE_ADDR'] = 'test'
        anon = anonymous_auth(request)
        assert anon.is_anonymous
        assert str(anon) == 'test'
