def test_registration(client):
    response = client.post('/api/v1/auth/register',
                           json={
                               'username':  'test',
                               'password': '123456',
                               'email': 'test@gmail.com'
                           })

    response_data = response.get_json()
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['token']