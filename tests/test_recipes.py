import pytest


def create_recipe(client, auth_headers, ingredient_model):
    payload = {
        "name": "Pasta",
        "instructions": "Cook pasta and mix.",
        "ingredients": [
            {
                "name": ingredient_model.name,
                "amount": 200
            }
        ]
    }
    response = client.post(
        "/api/v1/recipes",
        json=payload,
        headers=auth_headers
    )
    return response


def test_create_recipe_with_ingredients(client, auth_headers, ingredient_model):
    response = create_recipe(client, auth_headers, ingredient_model)

    assert response.status_code == 201

    response_json = response.get_json()
    assert response_json['success'] is True

    data = response_json["data"]

    assert "id" in data
    assert isinstance(data["id"], int)
    assert data["name"] == "Pasta"


def test_create_recipe_missing_token(client, ingredient_model):
    response = client.post(
        "/api/v1/recipes",
        json={
            "name": "Pasta",
            "instructions": "Cook",
            "ingredients": [{"name": ingredient_model.name, "amount": 100}]
        }
    )
    assert response.status_code == 401


@pytest.mark.parametrize(
    "data, missing_field",
    [
        ({"instructions": "Cook"}, "name"),
        ({"name": "Pasta"}, "instructions"),
        ({"name": "Pasta", "instructions": "Cook"}, "ingredients"),
    ]
)
def test_create_recipe_invalid_data(client, auth_headers, data, missing_field):
    response = client.post(
        "/api/v1/recipes",
        json=data,
        headers=auth_headers
    )
    response_data = response.get_json()

    assert response.status_code == 400
    assert response_data["success"] is False
    assert missing_field in response_data["message"]
    assert "data" not in response_data

