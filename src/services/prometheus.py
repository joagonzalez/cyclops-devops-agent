import httpx
from typing import Any, Dict, Optional



class PrometheusClient:
    def __init__(self, base_url: str, timeout: int = 5):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def test_connection(self) -> Dict[str, Any]:
        """Checks Prometheus health by making a test query."""
        query_url = f"{self.base_url}/api/v1/query"
        params = {"query": "up"}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(query_url, params=params, timeout=self.timeout)
                if response.status_code == 200:
                    return {"status": "OK", "data": response.json()}
                else:
                    return {"status": f"Prometheus error: {response.status_code}"}
        except Exception as e:
            return {"status": f"Error: {str(e)}"}

    async def query(self, promql: str, time: Optional[float|None] = None) -> Dict[str, Any]:
        """Executes a generic PromQL query.

        Args:
            promql (str): The PromQL query string.
            time (Optional[float]): Evaluation timestamp (optional).

        Returns:
            Dict[str, Any]: The response from Prometheus.
        """
        query_url = f"{self.base_url}/api/v1/query"
        params = {"query": promql}
        if time is not None:
            params["time"] = str(time)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(query_url, params=params, timeout=self.timeout)
                if response.status_code == 200:
                    return {"status": "OK", "data": response.json()}
                else:
                    return {"status": f"Prometheus error: {response.status_code}"}
        except Exception as e:
            return {"status": f"Error: {str(e)}"}