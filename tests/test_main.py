import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# --- GET / ---

def test_root_returns_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_root_contains_calculator_title():
    response = client.get("/")
    assert "Calculator" in response.text


# --- POST /add ---

def test_add_endpoint_basic():
    response = client.post("/add", json={"a": 3, "b": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["result"] == 8
    assert data["operation"] == "add"

def test_add_endpoint_floats():
    response = client.post("/add", json={"a": 1.5, "b": 2.5})
    assert response.status_code == 200
    assert response.json()["result"] == pytest.approx(4.0)

def test_add_endpoint_negative():
    response = client.post("/add", json={"a": -3, "b": -4})
    assert response.status_code == 200
    assert response.json()["result"] == -7

def test_add_endpoint_returns_operands():
    response = client.post("/add", json={"a": 10, "b": 20})
    data = response.json()
    assert data["a"] == 10
    assert data["b"] == 20


# --- POST /subtract ---

def test_subtract_endpoint_basic():
    response = client.post("/subtract", json={"a": 10, "b": 4})
    assert response.status_code == 200
    assert response.json()["result"] == 6

def test_subtract_endpoint_negative_result():
    response = client.post("/subtract", json={"a": 3, "b": 8})
    assert response.status_code == 200
    assert response.json()["result"] == -5

def test_subtract_endpoint_floats():
    response = client.post("/subtract", json={"a": 5.5, "b": 2.2})
    assert response.status_code == 200
    assert response.json()["result"] == pytest.approx(3.3)

def test_subtract_endpoint_operation_field():
    response = client.post("/subtract", json={"a": 1, "b": 1})
    assert response.json()["operation"] == "subtract"


# --- POST /multiply ---

def test_multiply_endpoint_basic():
    response = client.post("/multiply", json={"a": 4, "b": 5})
    assert response.status_code == 200
    assert response.json()["result"] == 20

def test_multiply_endpoint_by_zero():
    response = client.post("/multiply", json={"a": 9, "b": 0})
    assert response.status_code == 200
    assert response.json()["result"] == 0

def test_multiply_endpoint_negative():
    response = client.post("/multiply", json={"a": -3, "b": 4})
    assert response.status_code == 200
    assert response.json()["result"] == -12

def test_multiply_endpoint_floats():
    response = client.post("/multiply", json={"a": 2.5, "b": 4.0})
    assert response.status_code == 200
    assert response.json()["result"] == pytest.approx(10.0)


# --- POST /divide ---

def test_divide_endpoint_basic():
    response = client.post("/divide", json={"a": 10, "b": 2})
    assert response.status_code == 200
    assert response.json()["result"] == 5.0

def test_divide_endpoint_float_result():
    response = client.post("/divide", json={"a": 7, "b": 2})
    assert response.status_code == 200
    assert response.json()["result"] == pytest.approx(3.5)

def test_divide_endpoint_negative():
    response = client.post("/divide", json={"a": -6, "b": 3})
    assert response.status_code == 200
    assert response.json()["result"] == pytest.approx(-2.0)

def test_divide_by_zero_returns_400():
    response = client.post("/divide", json={"a": 5, "b": 0})
    assert response.status_code == 400

def test_divide_by_zero_error_message():
    response = client.post("/divide", json={"a": 5, "b": 0})
    assert "divide by zero" in response.json()["detail"].lower()


# --- Validation errors ---

def test_missing_field_returns_422():
    response = client.post("/add", json={"a": 5})
    assert response.status_code == 422

def test_invalid_type_returns_422():
    response = client.post("/add", json={"a": "hello", "b": 2})
    assert response.status_code == 422
