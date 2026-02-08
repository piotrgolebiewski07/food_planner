import pytest


def test_create_recipe_with_ingredients(client, auth_headers, ingredient_model):
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

    assert response.status_code == 201

    response_json = response.get_json()
    assert response_json['success'] is True

    data = response_json["data"]

    assert "id" in data
    assert isinstance(data["id"], int)
    assert data["name"] == "Pasta"

