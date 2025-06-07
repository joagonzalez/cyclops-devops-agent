# mypy: ignore-file
# mypy: ignore-errors
import json
import uuid
import chromadb
from chromadb.api import ClientAPI
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer


class MetricVectorStore:
    def __init__(self, persist_directory: str = "./chroma_db") -> None:
        self.client: ClientAPI = chromadb.PersistentClient(path=persist_directory)
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
                    "labels": json.dumps(labels),        # SERIALIZADO
                    "templates": json.dumps(templates),  # SERIALIZADO
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
                    "labels": ", ".join(json.loads(metadata.get("labels", "[]"))),
                    "templates": "; ".join(json.loads(metadata.get("templates", "[]"))),
                    "distance": str(results["distances"][0][i]),
                }
            )
        return output

if __name__ == "__main__":
    pass
