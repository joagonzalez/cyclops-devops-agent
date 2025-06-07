from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import uuid
import random


class MetricVectorStore:
    def __init__(self, persist_directory: str = "./chroma_db") -> None:
        self.client = chromadb.Client(
            Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_directory)
        )
        self.collection = self.client.get_or_create_collection("metrics")
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def add_metric(
        self,
        metric_name: str,
        description: str,
        example_query: str,
        labels: List[str],
        templates: List[str],
    ) -> None:
        doc_id = str(uuid.uuid4())
        embedding = self.model.encode(f"{metric_name} {description} {example_query}").tolist()

        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[metric_name],
            metadatas=[
                {
                    "description": description,
                    "example_query": example_query,
                    "labels": labels,
                    "templates": templates,
                }
            ],
        )

    def query_similar_metrics(self, query: str, k: int = 5) -> List[Dict[str, Optional[str]]]:
        query_embedding = self.model.encode(query).tolist()

        results = self.collection.query(query_embeddings=[query_embedding], n_results=k)

        output = []
        for i in range(len(results["ids"][0])):
            metadata = results["metadatas"][0][i]
            output.append(
                {
                    "metric_name": results["documents"][0][i],
                    "description": metadata.get("description"),
                    "example_query": metadata.get("example_query"),
                    "labels": ", ".join(metadata.get("labels", [])),
                    "templates": "; ".join(metadata.get("templates", [])),
                    "distance": str(results["distances"][0][i]),
                }
            )
        return output


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
