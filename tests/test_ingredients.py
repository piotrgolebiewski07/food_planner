import pytest


def test_get_ingredients_no_records(client):
    response = client.get('/api/v1/ingredients')
    expected_result = {
        'success': True,
        'data': [],
        'records_on_page': 0,
        'pagination': {
            'total_pages': 0,
            'total_records': 0,
            'current_page': '/api/v1/ingredients?page=1'
        }
    }
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.get_json() == expected_result


def test_get_ingredients(client, sample_data):
    response = client.get('/api/v1/ingredients')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['records_on_page'] == 5
    assert response_data['pagination'] == {
        'total_pages': 2,
        'total_records': 7,
        'current_page': '/api/v1/ingredients?page=1',
        'next_page': '/api/v1/ingredients?page=2'
    }


def test_get_ingredients_with_params(client, sample_data):
    response = client.get('/api/v1/ingredients?fields=first_name&sort=-id&page=2&limit=2')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['records_on_page'] == 2

    pagination = response_data['pagination']

    assert pagination['total_pages'] == 4
    assert pagination['total_records'] == 7

    assert pagination['current_page'].startswith('/api/v1/ingredients?page=2')

    assert pagination['next_page'].startswith('/api/v1/ingredients?page=3')
    assert 'fields=first_name' in pagination['next_page']

    assert pagination['previous_page'].startswith('/api/v1/ingredients?page=1')


def test_get_single_ingredient(client, sample_data):
    response = client.get('/api/v1/ingredients/2')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data']['name'] == 'milk'
    assert response_data['data']['calories'] == '42.00'
    assert response_data['data']['unit'] == 'ml'


def test_get_single_ingredient_not_found(client, sample_data):
    response = client.get('/api/v1/ingredients/1000')
    response_data = response.get_json()
    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


def test_create_ingredient(client, token, ingredient):
    response = client.post('/api/v1/ingredients',
                           json=ingredient,
                           headers={
                               'Authorization': f'Bearer {token}'
                           })
    response_data = response.get_json()

    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True

    created = response_data['data']

    assert created['name'] == ingredient['name']
    assert created['unit'] == ingredient['unit']
    assert created['calories'] == '40.00'
    assert 'id' in created

    ingredient_id = created['id']

    response = client.get(f'/api/v1/ingredients/{ingredient_id}')
    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data['success'] is True
    assert response_data['data']['name'] == ingredient['name']


@pytest.mark.parametrize(
    'data, missing_field',
    [
        ({'name': 'milk', 'calories': 40}, 'unit'),
        ({'calories': 40, 'unit': 'ml'}, 'name'),
        ({'name': 'milk', 'unit': 'ml'}, 'calories')
    ]
)
def test_create_ingredient_invalid_data(client, token, data, missing_field):
    response = client.post('/api/v1/ingredients',
                           json=data,
                           headers={
                               'Authorization': f'Bearer {token}'
                           })
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data
    assert missing_field in response_data['message']
    assert 'Missing data for required field.' in response_data['message'][missing_field]
    assert isinstance(response_data['message'][missing_field], list)


def test_create_ingredient_invalid_content_type(client, token, ingredient):
    response = client.post('/api/v1/ingredients',
                           data=ingredient,
                           headers={
                               'Authorization': f'Bearer {token}'
                           })
    response_data = response.get_json()
    assert response.status_code == 415
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


def test_create_ingredient_missing_token(client, ingredient):
    response = client.post('/api/v1/ingredients',
                           json=ingredient)
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data' not in response_data


def test_create_ingredient_duplicate_name(client, token, ingredient):
    response = client.post('/api/v1/ingredients',
                           json=ingredient,
                           headers={
                               'Authorization': f'Bearer {token}'
                           })
    assert response.status_code == 201

    response = client.post('/api/v1/ingredients',
                           json=ingredient,
                           headers={
                               'Authorization': f'Bearer {token}'
                           })

    assert response.status_code == 409


def test_delete_ingredient_success(client, token, ingredient):
    response = client.post('/api/v1/ingredients',
                           json=ingredient,
                           headers={
                               'Authorization': f'Bearer {token}'
                           })
    assert response.status_code == 201
    ingredient_id = response.get_json()['data']['id']

    response = client.delete(
        f'/api/v1/ingredients/{ingredient_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200

    response = client.get(f'/api/v1/ingredients/{ingredient_id}')
    assert response.status_code == 404


def test_delete_ingredient_missing_token(client, ingredient, token):
    response = client.post('/api/v1/ingredients',
                           json=ingredient,
                           headers={
                               'Authorization': f'Bearer {token}'
                           })
    assert response.status_code == 201
    ingredient_id = response.get_json()['data']['id']

    response = client.delete(
        f'/api/v1/ingredients/{ingredient_id}')
    assert response.status_code == 401


def test_delete_ingredient_not_found(client, token):
    response = client.delete('/api/v1/ingredients/1000',
                          headers={
                              'Authorization': f'Bearer {token}'
                          })
    assert response.status_code == 404

