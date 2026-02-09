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


def test_get_recipes_empty(client):
    response = client.get("/api/v1/recipes")
    data = response.get_json()

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert data["success"] is True
    assert data["data"] == []
    assert data["records_on_page"] == 0


def test_get_recipes(client, auth_headers, ingredient_model):
    response = create_recipe(client, auth_headers, ingredient_model)
    recipe_id = response.get_json()["data"]["id"]

    response = client.get("/api/v1/recipes")
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert len(data["data"]) == 1

    recipe = data["data"][0]
    assert recipe["id"] == recipe_id
    assert recipe["name"] == "Pasta"
    assert isinstance(recipe["ingredients"], list)
    assert recipe["ingredients"][0]["name"] == ingredient_model.name


def test_get_single_recipe(client, auth_headers, ingredient_model):
    response = create_recipe(client, auth_headers, ingredient_model)
    recipe_id = response.get_json()["data"]["id"]

    response = client.get(f"/api/v1/recipes/{recipe_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert data["data"]["id"] == recipe_id
    assert data["data"]["name"] == "Pasta"
    assert data["data"]["ingredients"][0]["name"] == ingredient_model.name




