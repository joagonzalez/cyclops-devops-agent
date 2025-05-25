"""
In this module all configuration required for the application
is collected within a single dictionary named 'config'. In the future
it will be used to config loggers as well
"""

import os
from typing import Any, Dict

from dotenv import load_dotenv

dotenv_path = os.getenv(
    "API_DOTENV_SHARED", os.path.join(os.path.dirname(__file__), ".env.shared")
)

dotenv_path_secrets = os.getenv(
    "API_DOTENV_SECRETS",
    os.path.join(os.path.dirname(__file__), ".env.secrets"),
)

# priorizes env vars (not .env file)
load_dotenv(dotenv_path, override=True)
# priorizes env vars (not .env file)
load_dotenv(dotenv_path_secrets, override=True)

config: Dict[str, Any] = {
    "OPENAI": {
        "API_KEY": os.getenv("OPENAI_API_KEY", ""),
        "MODEL": os.getenv("OPENAI_MODEL", "gpt-4o"),
        "TEMPERATURE": float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
        "SYSTEM_PROMPT": os.getenv(
            "OPENAI_SYSTEM_PROMPT",
            """
                You are a highly experienced DevOps and Site Reliability Engineer specialized in observability and monitoring. 
                Your task is to translate natural language monitoring queries into accurate and efficient PromQL (Prometheus Query Language) expressions.

                You are a PromQL expert. Respond only with a valid JSON object in the format:
                {
                    "status": "success|error",
                    "promql": ["<your_query_here>", "<your_query_here>"]
                }
                
                Also, you understand the following:
                Time series data modeling and Prometheus metrics exposition.

                Common metric patterns such as rate(), avg_over_time(), sum by (), histogram quantiles, and alerting conditions.

                How to interpret user intent from vague or underspecified queries and fill in missing technical details reasonably.

                Kubernetes, Linux systems, HTTP services, infrastructure metrics (CPU, memory, disk, network), and custom application metrics.

                You must:

                Only output PromQL code in a valid format unless explicitly asked to explain.

                Ask clarifying questions only if the query is too ambiguous or missing key details.

                Avoid hallucinating non-existent metric names; only use placeholders like <<metric_name>> if you're unsure.

                Follow best practices for performance and readability in PromQL queries.

                Optimize queries to work well with Grafana or alerting rules.

                If given context (e.g., existing metrics or schema), prefer using it to craft more precise queries.

                Examples of natural language queries you can handle:

                “CPU usage across all nodes over the past 5 minutes”

                “Latency P95 for service X”

                “Memory usage percentage by pod in namespace foo”

                “Total HTTP requests per second, grouped by response code”

                Respond with PromQL like a battle-tested SRE who automates Grafana dashboards and alert rules in their sleep.""",
        ),
    },
    "PROMETHEUS_URL": os.getenv("PROMETHEUS_URL", "http://prometheus-operated.monitoring.svc.cluster.local:9090"),  # noqa: E501
    "SERVER": {
        "HOSTNAME": os.getenv("SERVER_HOSTNAME", "0.0.0.0"),
        "PORT": int(os.getenv("SERVER_PORT", "5000")),
        "DEBUG": os.getenv("SERVER_DEBUG", "True").lower()
        in ("true", "1", "t"),  # noqa: E501
        "RELOAD": os.getenv("SERVER_RELOAD", "False").lower()
        in ("true", "1", "t"),  # noqa: E501
        "RELOAD_DIRS": [
            os.getenv("SERVER_RELOAD_DIRS", "src"),
        ],
        "LOG_LEVEL": os.getenv("SERVER_LOG_LEVEL", "debug"),
        "WORKERS": int(os.getenv("SERVER_WORKERS", "5")),
    },
    "API": {
        "ENVIRONMENT": os.getenv("API_ENVIRONMENT", "local"),
        "TITLE": os.getenv("API_TITLE", "Foundations-Networking Core API"),
        "DESCRIPTION": os.getenv(
            "API_DESCRIPTION",
            "REST interface that expose interactions with network elements",
        ),
        "VERSION": os.getenv("API_VERSION", "0.1.0"),
        "USERNAME": os.getenv("API_USERNAME", ""),
        "PASSWORD": os.getenv("API_PASSWORD", ""),
    },
    "SWAGGER": {
        "DOCS_URL": os.getenv("SWAGGER_DOCS_URL", "/docs"),
        "REDOC_URL": os.getenv("SWAGGER_REDOC_URL", "/redoc_docs"),
    },
    "JWT": {
        "SECRET_KEY": os.getenv("JWT_SECRET_KEY", ""),
        "ALGORITHM": os.getenv("JWT_ALGORITHM", ""),
        "ACCESS_TOKEN_EXPIRE_MINUTES": int(
            os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
        ),
    },
    "DATABASE": {
        "SQLALCHEMY": {
            "PREFIX": os.getenv("SQLALCHEMY_DATABASE_PREFIX", "DB."),
            "CONFIG": {
                "DB.URL": os.getenv("SQLALCHEMY_DATABASE_URL", None),
                "DB.ECHO": os.getenv(
                    "SQLALCHEMY_DATABASE_ECHO", "True"
                ).lower()  # noqa: E501
                in ("true", "1", "t"),
            },
        },
    },
}

# fmt: off
PROMPT = """
     ___      .______    __          _______. _______  _______  _______  
    /   \\     |   _  \\  |  |        /       ||   ____||   ____||       \\  
   /  ^  \\    |  |_)  | |  |       |   (----`|  |__   |  |__   |  .--.  | 
  /  /_\\  \\   |   ___/  |  |        \\   \\    |   __|  |   __|  |  |  |  |
 /  _____  \\  |  |      |  |    .----)   |   |  |____ |  |____ |  '--'  |
/__/     \\__\\ | _|      |__|    |_______/    |_______||_______||_______/ 
""" # noqa: W605, E261, W291, W1401
# fmt: on
