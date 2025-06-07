# mypy: ignore-file
import sys
sys.path.append(".")
import random
from src.services.vectordb import MetricVectorStore


def test_metric_vector_store() -> None:
    store = MetricVectorStore()

    # Cargar 15 métricas de ejemplo
    for i in range(15):
        metric_name = f"metric_{i}"
        description = f"Description of metric {i}"
        example_query = f"sum(rate(metric_{i}{{label='value'}}[5m]))"
        labels = [f"label_{j}" for j in range(random.randint(1, 3))]
        templates = [
            f"sum(rate({metric_name}{{{{label_filters}}}}[5m]))",
            f"avg({metric_name}{{{{label_filters}}}})",
        ]

        store.add_metric(
            metric_name=metric_name,
            description=description,
            example_query=example_query,
            labels=labels,
            templates=templates,
        )

    # Ejecutar búsqueda de similitud
    print("== Similarity search example ==")
    query_text = "CPU usage over time"
    similar_metrics = store.query_similar_metrics(query=query_text, k=5)

    for metric in similar_metrics:
        print(metric)


if __name__ == "__main__":
    test_metric_vector_store()