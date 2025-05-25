"""
API PromQL endpoints used to get data from Prometheus
from external tools and applications
"""
from typing import Dict, Any
from fastapi import APIRouter, status
from src.config.settings import config
from src.services.prometheus import PrometheusClient


router = APIRouter()
prometheusClient = PrometheusClient(config["PROMETHEUS_URL"])

@router.get("/query/", tags=["PromQL"], status_code=status.HTTP_200_OK)
async def get_promql_health() -> Dict[str, Any]:
    """
    Checks Prometheus health by making a test query

    Returns:
        Dict[str, str]: dict with status message
    """
    return prometheusClient.test_connection()


@router.get("/query/{promql}", tags=["PromQL"], status_code=status.HTTP_200_OK)
async def get_promql_query(promql: str) -> Dict[str, Any]:
    """
    Executes a generic PromQL query

    Args:
        promql (str): The PromQL query string.

    Returns:
        Dict[str, Any]: The response from Prometheus.
    """
    return prometheusClient.query(promql)