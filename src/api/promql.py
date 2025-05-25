"""
API PromQL endpoints used to get data from Prometheus
from external tools and applications
"""
import httpx
from typing import Dict, Any
from fastapi import APIRouter, status
from src.config.settings import config


router = APIRouter()


@router.get("/query/", tags=["PromQL"], status_code=status.HTTP_200_OK)
async def get_promql_health() -> Dict[str, Any]:
    """Checks Prometheus health by making a test query

    Returns:
        Dict[str, str]: dict with status message
    """
    prometheus_url = config["PROMETHEUS_URL"]
    query_url = f"{prometheus_url}/api/v1/query"
    params = {"query": "up"}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(query_url, params=params, timeout=5)
            if response.status_code == 200:
                return {"status": "OK", "data": response.json()}
            else:
                return {"status": f"Prometheus error: {response.status_code}"}
    except Exception as e:
        return {"status": f"Error: {str(e)}"}
