"""
Tests for calculator api endpoints.
"""
from fastapi.testclient import TestClient

from src import app

client = TestClient(app=app)


def test_calculator_addition_1():
    """
    Test /calculator/addition/ endpoint
    """
    response: TestClient = client.get("/calculator/addition/?a=5&b=4")
    assert response.status_code == 200
    assert response.json() == {"result": 9.0}


def test_calculator_addition_2():
    """
    Test /calculator/addition/ endpoint
    """
    response: TestClient = client.get("/calculator/addition/?a=5&b=-5")
    assert response.status_code == 200
    assert response.json() == {"result": 0.0}


def test_calculator_addition_3():
    """
    Test /calculator/addition/ endpoint
    """
    response: TestClient = client.get("/calculator/addition/?a=-5&b=4")
    assert response.status_code == 200
    assert response.json() == {"result": -1.0}


def test_calculator_divide_1():
    """
    Test /calculator/divide/ endpoint
    """
    response: TestClient = client.get("/calculator/divide/?a=4&b=2")
    assert response.status_code == 200
    assert response.json() == {"result": 2.0}


def test_calculator_divide_2():
    """
    Test /calculator/divide/ endpoint
    """
    response: TestClient = client.get("/calculator/divide/?a=4&b=4")
    assert response.status_code == 200
    assert response.json() == {"result": 1.0}


def test_calculator_divide_3():
    """
    Test /calculator/divide/ endpoint
    """
    response: TestClient = client.get("/calculator/divide/?a=-4&b=2")
    assert response.status_code == 200
    assert response.json() == {"result": -2.0}


def test_calculator_multiply_1():
    """
    Test /calculator/multiply/ endpoint
    """
    response: TestClient = client.get("/calculator/multiply/?a=2&b=2")
    assert response.status_code == 200
    assert response.json() == {"result": 4.0}


def test_calculator_multiply_2():
    """
    Test /calculator/multiply/ endpoint
    """
    response: TestClient = client.get("/calculator/multiply/?a=2&b=-2")
    assert response.status_code == 200
    assert response.json() == {"result": -4.0}


def test_calculator_multiply_3():
    """
    Test /calculator/multiply/ endpoint
    """
    response: TestClient = client.get("/calculator/multiply/?a=1&b=2")
    assert response.status_code == 200
    assert response.json() == {"result": 2.0}


def test_calculator_substract_1():
    """
    Test /calculator/substract/ endpoint
    """
    response: TestClient = client.get("/calculator/substract/?a=4&b=2")
    assert response.status_code == 200
    assert response.json() == {"result": 2.0}


def test_calculator_substract_2():
    """
    Test /calculator/substract/ endpoint
    """
    response: TestClient = client.get("/calculator/substract/?a=2&b=4")
    assert response.status_code == 200
    assert response.json() == {"result": -2.0}


def test_calculator_substract_3():
    """
    Test /calculator/substract/ endpoint
    """
    response: TestClient = client.get("/calculator/substract/?a=2&b=2")
    assert response.status_code == 200
    assert response.json() == {"result": 0.0}
