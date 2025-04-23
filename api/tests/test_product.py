import pytest
from django.urls import reverse
from apps.shop.models import Product

@pytest.mark.django_db
def test_create_product(api_client):
    url = reverse("product-create")
    payload = {
        "name": "Test Product",
        "price": "19.99",
        "stock": 50
    }
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201
    assert Product.objects.filter(name="Test Product").exists()


@pytest.mark.django_db
def test_create_product_invalid_price_payload(api_client):
    url = reverse("product-create")
    payload = {
        "name": "Another product",
        "price": "gdh", 
        "stock": 5
    }
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 400
    data = response.data
    assert data['validations']['price'] == "A valid number is required."


@pytest.mark.django_db
def test_update_product(api_client):
    # First, create a product
    product = Product.objects.create(name="Old Product", price="15.00", stock=10)
    
    url = reverse("product-retrieve-update-destroy", kwargs={"id": product.id})  # product-detail should be name in urls.py
    payload = {
        "name": "Updated Product",
        "price": "20.00",
        "stock": 30
    }
    response = api_client.put(url, payload, format="json")

    assert response.status_code == 200
    product.refresh_from_db()
    assert product.name == "Updated Product"
    assert product.price == 20.00
    assert product.stock == 30