import pytest

@pytest.mark.django_db
class TestLogin:
    
    def test_login(self, client, get_basic_auth_header, get_test_user):
        user = get_test_user(1)
        response = client.post('/login', headers={'Authorization': get_basic_auth_header(user.username, 'test')})
        data = response.data
        assert response.status_code == 200
        assert isinstance(data['token'], str)
        assert len(data['token']) == 64

    def test_login_unauthorized(self, client, get_basic_auth_header, get_test_user):
        user = get_test_user(1)
        response = client.post('/login', headers={'Authorization': get_basic_auth_header(user.username, 'test_fail')})
        assert response.status_code == 401

@pytest.mark.django_db
class TestLogout:
    
    def test_logout(self, client):
        response = client.post('/logout', headers={'Authorization': 'Bearer test_user_token'})
        assert response.status_code == 204

    def test_logoutall(self, client):
        response = client.post('/logoutall', headers={'Authorization': 'Bearer test_user_token'})
        assert response.status_code == 204
