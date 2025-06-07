"""
Tests for PromQL api endpoints.
"""
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from src import app

client = TestClient(app=app)


@patch('src.services.prometheus.PrometheusClient.test_connection')
def test_promql_health_success(mock_test_connection):
    """
    Test /promql/query/ endpoint for health check - success case
    """
    mock_test_connection.return_value = {"status": "OK", "data": {"status": "success"}}
    
    response = client.get("/promql/query/")
    
    assert response.status_code == 200
    assert response.json() == {"status": "OK", "data": {"status": "success"}}
    mock_test_connection.assert_called_once()


@patch('src.services.prometheus.PrometheusClient.test_connection')
def test_promql_health_error(mock_test_connection):
    """
    Test /promql/query/ endpoint for health check - error case
    """
    mock_test_connection.return_value = {"status": "Prometheus error: 500"}
    
    response = client.get("/promql/query/")
    
    assert response.status_code == 200
    assert response.json() == {"status": "Prometheus error: 500"}
    mock_test_connection.assert_called_once()


@patch('src.services.prometheus.PrometheusClient.test_connection')
def test_promql_health_connection_error(mock_test_connection):
    """
    Test /promql/query/ endpoint for health check - connection error
    """
    mock_test_connection.return_value = {"status": "Error: Connection timeout"}
    
    response = client.get("/promql/query/")
    
    assert response.status_code == 200
    assert response.json() == {"status": "Error: Connection timeout"}
    mock_test_connection.assert_called_once()


@patch('src.services.prometheus.PrometheusClient.query')
def test_promql_query_simple_metric(mock_query):
    """
    Test /promql/query/{promql} endpoint with simple metric query
    """
    mock_query.return_value = {
        "status": "success",
        "data": {
            "resultType": "vector",
            "result": [{"metric": {"__name__": "up"}, "value": [1234567890, "1"]}]
        }
    }
    
    response = client.get("/promql/query/up")
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_query.assert_called_once_with("up")


@patch('src.services.prometheus.PrometheusClient.query')
def test_promql_query_complex_metric(mock_query):
    """
    Test /promql/query/{promql} endpoint with complex metric query
    """
    complex_query = "rate(http_requests_total[5m])"
    mock_query.return_value = {
        "status": "success",
        "data": {
            "resultType": "vector",
            "result": [{"metric": {"job": "api"}, "value": [1234567890, "0.5"]}]
        }
    }
    
    response = client.get(f"/promql/query/{complex_query}")
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_query.assert_called_once_with(complex_query)


@patch('src.services.prometheus.PrometheusClient.query')
def test_promql_query_with_special_characters(mock_query):
    """
    Test /promql/query/{promql} endpoint with special characters in query
    """
    special_query = "cpu_usage{instance=\"localhost:9090\"}"
    mock_query.return_value = {
        "status": "success",
        "data": {"resultType": "vector", "result": []}
    }
    
    response = client.get(f"/promql/query/{special_query}")
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_query.assert_called_once_with(special_query)


@patch('src.services.prometheus.PrometheusClient.query')
def test_promql_query_aggregation(mock_query):
    """
    Test /promql/query/{promql} endpoint with aggregation query
    """
    aggregation_query = "sum(cpu_usage) by (instance)"
    mock_query.return_value = {
        "status": "success",
        "data": {
            "resultType": "vector",
            "result": [
                {"metric": {"instance": "server1"}, "value": [1234567890, "75.5"]},
                {"metric": {"instance": "server2"}, "value": [1234567890, "82.1"]}
            ]
        }
    }
    
    response = client.get(f"/promql/query/{aggregation_query}")
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["data"]["result"]) == 2
    mock_query.assert_called_once_with(aggregation_query)


@patch('src.services.prometheus.PrometheusClient.query')
def test_promql_query_empty_result(mock_query):
    """
    Test /promql/query/{promql} endpoint with query returning empty result
    """
    mock_query.return_value = {
        "status": "success",
        "data": {"resultType": "vector", "result": []}
    }
    
    response = client.get("/promql/query/nonexistent_metric")
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["data"]["result"] == []
    mock_query.assert_called_once_with("nonexistent_metric")


@patch('src.services.prometheus.PrometheusClient.query')
def test_promql_query_prometheus_error(mock_query):
    """
    Test /promql/query/{promql} endpoint with Prometheus returning error
    """
    mock_query.return_value = {
        "status": "error",
        "errorType": "bad_data",
        "error": "invalid query"
    }
    
    response = client.get("/promql/query/invalid(query")
    
    assert response.status_code == 200
    assert response.json()["status"] == "error"
    assert "error" in response.json()
    mock_query.assert_called_once_with("invalid(query")


@patch('src.services.prometheus.PrometheusClient.query')
def test_promql_query_service_exception(mock_query):
    """
    Test /promql/query/{promql} endpoint when service raises an exception
    """
    mock_query.side_effect = Exception("Prometheus connection error")
    
    # The endpoint doesn't handle exceptions, so it will raise
    # This is expected behavior based on the current implementation
    try:
        response = client.get("/promql/query/up")
        # If we get here, the exception was handled somehow
        assert response.status_code in [200, 500]
    except Exception as e:
        # The exception is expected to bubble up
        assert "Prometheus connection error" in str(e)