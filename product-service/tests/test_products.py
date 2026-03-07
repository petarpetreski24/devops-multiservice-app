def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["service"] == "product-service"


def test_create_product(client):
    response = client.post("/products/", json={
        "name": "Laptop",
        "description": "A powerful laptop",
        "price": 999.99,
        "in_stock": True
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 999.99
    assert data["in_stock"] is True
    assert "id" in data


def test_create_product_invalid_price(client):
    response = client.post("/products/", json={
        "name": "Bad Product",
        "price": -10.0
    })
    assert response.status_code == 422


def test_list_products(client):
    client.post("/products/", json={
        "name": "Product 1",
        "price": 10.0
    })
    client.post("/products/", json={
        "name": "Product 2",
        "price": 20.0
    })

    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_product(client):
    create_resp = client.post("/products/", json={
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 1500.0
    })
    product_id = create_resp.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"


def test_get_product_not_found(client):
    response = client.get("/products/999")
    assert response.status_code == 404


def test_update_product(client):
    create_resp = client.post("/products/", json={
        "name": "Laptop",
        "price": 999.99
    })
    product_id = create_resp.json()["id"]

    response = client.put(f"/products/{product_id}", json={
        "name": "Updated Laptop",
        "price": 899.99
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Laptop"
    assert response.json()["price"] == 899.99


def test_update_product_not_found(client):
    response = client.put("/products/999", json={"name": "Ghost"})
    assert response.status_code == 404


def test_delete_product(client):
    create_resp = client.post("/products/", json={
        "name": "To Delete",
        "price": 5.0
    })
    product_id = create_resp.json()["id"]

    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 204

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404


def test_delete_product_not_found(client):
    response = client.delete("/products/999")
    assert response.status_code == 404
