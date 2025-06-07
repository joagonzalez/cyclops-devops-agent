"""
VectorDB service for RAG use case using sqlite-vec.
This service manages embeddings for metrics, labels, and templates
to enable similarity-based queries for monitoring and alerting.
"""
import sqlite3
import json
import random
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorDB:
    """
    VectorDB class for managing embeddings and similarity searches for RAG use case.
    
    This class manages three main tables:
    - metrics: Store metric information with embeddings
    - metric_labels: Store label information for metrics  
    - metric_templates: Store PromQL query templates
    """
    
    def __init__(self, db_path: str = "vectordb.sqlite", embedding_dimension: int = 512):
        """
        Initialize VectorDB with sqlite-vec extension.
        
        Args:
            db_path: Path to SQLite database file
            embedding_dimension: Dimension of embedding vectors (default 512)
        """
        self.db_path = db_path
        self.embedding_dimension = embedding_dimension
        self.conn = None
        self.use_vector_search = True  # Will be set to False if sqlite-vec is not available
        self._initialize_db()
    
    def _initialize_db(self):
        """Initialize database connection and create tables."""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            
            # Try to load sqlite-vec extension
            self.conn.enable_load_extension(True)
            vec_loaded = False
            
            # Try different methods to load sqlite-vec
            for extension_name in ["vec0", "sqlite_vec", "vector"]:
                try:
                    self.conn.load_extension(extension_name)
                    vec_loaded = True
                    logger.info(f"Successfully loaded sqlite-vec extension: {extension_name}")
                    break
                except sqlite3.OperationalError as e:
                    logger.debug(f"Failed to load extension {extension_name}: {e}")
                    continue
            
            # Try loading from sqlite_vec module if direct loading failed
            if not vec_loaded:
                try:
                    import sqlite_vec
                    sqlite_vec.load(self.conn)
                    vec_loaded = True
                    logger.info("Successfully loaded sqlite-vec using sqlite_vec.load()")
                except (ImportError, AttributeError) as e:
                    logger.debug(f"Failed to load using sqlite_vec module: {e}")
            
            self.conn.enable_load_extension(False)
            
            if not vec_loaded:
                logger.warning("sqlite-vec extension not available. Falling back to pure SQLite implementation.")
                self.use_vector_search = False
            else:
                self.use_vector_search = True
            
            # Create tables
            self._create_tables()
            logger.info(f"VectorDB initialized successfully at {self.db_path}")
            
        except Exception as e:
            logger.error(f"Failed to initialize VectorDB: {e}")
            raise
    
    def _create_tables(self):
        """Create the required tables for the RAG system."""
        cursor = self.conn.cursor()
        
        # Create metrics table with embedding vector
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL UNIQUE,
                description TEXT,
                example_query TEXT,
                embedding BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create metric_labels table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metric_labels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_id INTEGER NOT NULL,
                label_name TEXT NOT NULL,
                example_values TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (metric_id) REFERENCES metrics (id),
                UNIQUE(metric_id, label_name)
            )
        """)
        
        # Create metric_templates table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metric_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_id INTEGER NOT NULL,
                template TEXT NOT NULL,
                template_type TEXT DEFAULT 'promql',
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (metric_id) REFERENCES metrics (id)
            )
        """)
        
        # Create vector index for similarity search (only if sqlite-vec is available)
        if self.use_vector_search:
            try:
                cursor.execute("""
                    CREATE VIRTUAL TABLE IF NOT EXISTS metrics_vec USING vec0(
                        embedding float[{}]
                    )
                """.format(self.embedding_dimension))
                logger.info("Vector search table created successfully")
            except Exception as e:
                logger.warning(f"Failed to create vector table, disabling vector search: {e}")
                self.use_vector_search = False
        
        self.conn.commit()
        logger.info("Database tables created successfully")
    
    def add_metric(self, metric_name: str, description: str = None, 
                   example_query: str = None, embedding: List[float] = None) -> int:
        """
        Add a new metric with its embedding.
        
        Args:
            metric_name: Name of the metric
            description: Description of what the metric measures
            example_query: Example PromQL query for this metric
            embedding: Vector embedding for the metric
            
        Returns:
            int: ID of the inserted metric
        """
        cursor = self.conn.cursor()
        
        try:
            # Insert metric
            cursor.execute("""
                INSERT OR REPLACE INTO metrics (metric_name, description, example_query, embedding)
                VALUES (?, ?, ?, ?)
            """, (metric_name, description, example_query, 
                  json.dumps(embedding) if embedding else None))
            
            metric_id = cursor.lastrowid
            
            # Add to vector index if embedding provided and vector search is available
            if embedding and self.use_vector_search:
                try:
                    cursor.execute("""
                        INSERT OR REPLACE INTO metrics_vec (rowid, embedding) 
                        VALUES (?, ?)
                    """, (metric_id, json.dumps(embedding)))
                except Exception as e:
                    logger.warning(f"Failed to add to vector index: {e}")
                    # Continue without vector indexing
            
            self.conn.commit()
            logger.info(f"Added metric: {metric_name} with ID: {metric_id}")
            return metric_id
            
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to add metric {metric_name}: {e}")
            raise
    
    def add_metric_label(self, metric_id: int, label_name: str, 
                        example_values: str = None) -> int:
        """
        Add a label for a metric.
        
        Args:
            metric_id: ID of the metric
            label_name: Name of the label
            example_values: Example values for this label
            
        Returns:
            int: ID of the inserted label
        """
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO metric_labels (metric_id, label_name, example_values)
                VALUES (?, ?, ?)
            """, (metric_id, label_name, example_values))
            
            label_id = cursor.lastrowid
            self.conn.commit()
            logger.info(f"Added label {label_name} for metric ID {metric_id}")
            return label_id
            
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to add label {label_name}: {e}")
            raise
    
    def add_metric_template(self, metric_id: int, template: str, 
                           template_type: str = "promql", description: str = None) -> int:
        """
        Add a template for a metric.
        
        Args:
            metric_id: ID of the metric
            template: Template string (e.g., PromQL query template)
            template_type: Type of template (default: 'promql')
            description: Description of the template
            
        Returns:
            int: ID of the inserted template
        """
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO metric_templates (metric_id, template, template_type, description)
                VALUES (?, ?, ?, ?)
            """, (metric_id, template, template_type, description))
            
            template_id = cursor.lastrowid
            self.conn.commit()
            logger.info(f"Added template for metric ID {metric_id}")
            return template_id
            
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to add template: {e}")
            raise
    
    def similarity_search(self, query_embedding: List[float], 
                         top_k: int = 5, threshold: float = 0.7) -> List[Dict[str, Any]]:
        """
        Find similar metrics using cosine similarity.
        
        Args:
            query_embedding: Query vector embedding
            top_k: Number of top results to return
            threshold: Minimum similarity threshold (0-1)
            
        Returns:
            List of similar metrics with metadata
        """
        if not self.use_vector_search:
            logger.warning("Vector search not available, falling back to returning all metrics")
            return self.get_all_metrics()[:top_k]
        
        cursor = self.conn.cursor()
        
        try:
            # Use sqlite-vec's cosine distance function
            # Note: cosine distance = 1 - cosine similarity
            query = """
                SELECT 
                    m.id,
                    m.metric_name,
                    m.description,
                    m.example_query,
                    (1 - vec_distance_cosine(mv.embedding, ?)) as similarity_score
                FROM metrics m
                JOIN metrics_vec mv ON m.id = mv.rowid
                WHERE (1 - vec_distance_cosine(mv.embedding, ?)) >= ?
                ORDER BY similarity_score DESC
                LIMIT ?
            """
            
            query_vector_json = json.dumps(query_embedding)
            cursor.execute(query, (query_vector_json, query_vector_json, threshold, top_k))
            
            results = []
            for row in cursor.fetchall():
                metric_id, metric_name, description, example_query, similarity = row
                
                # Get labels for this metric
                labels = self.get_metric_labels(metric_id)
                
                # Get templates for this metric
                templates = self.get_metric_templates(metric_id)
                
                results.append({
                    'id': metric_id,
                    'metric_name': metric_name,
                    'description': description,
                    'example_query': example_query,
                    'similarity_score': similarity,
                    'labels': labels,
                    'templates': templates
                })
            
            logger.info(f"Found {len(results)} similar metrics")
            return results
            
        except Exception as e:
            logger.error(f"Similarity search failed: {e}")
            # Fall back to text search or return all metrics
            logger.info("Falling back to returning all metrics")
            return self.get_all_metrics()[:top_k]
    
    def get_metric_labels(self, metric_id: int) -> List[Dict[str, Any]]:
        """Get all labels for a specific metric."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, label_name, example_values 
            FROM metric_labels 
            WHERE metric_id = ?
        """, (metric_id,))
        
        return [
            {
                'id': row[0],
                'label_name': row[1],
                'example_values': row[2]
            }
            for row in cursor.fetchall()
        ]
    
    def get_metric_templates(self, metric_id: int) -> List[Dict[str, Any]]:
        """Get all templates for a specific metric."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, template, template_type, description 
            FROM metric_templates 
            WHERE metric_id = ?
        """, (metric_id,))
        
        return [
            {
                'id': row[0],
                'template': row[1],
                'template_type': row[2],
                'description': row[3]
            }
            for row in cursor.fetchall()
        ]
    
    def get_metric_by_name(self, metric_name: str) -> Optional[Dict[str, Any]]:
        """Get metric information by name."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, metric_name, description, example_query, embedding
            FROM metrics 
            WHERE metric_name = ?
        """, (metric_name,))
        
        row = cursor.fetchone()
        if row:
            metric_id, name, description, example_query, embedding_json = row
            embedding = json.loads(embedding_json) if embedding_json else None
            
            return {
                'id': metric_id,
                'metric_name': name,
                'description': description,
                'example_query': example_query,
                'embedding': embedding,
                'labels': self.get_metric_labels(metric_id),
                'templates': self.get_metric_templates(metric_id)
            }
        return None
    
    def search_by_text(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search metrics by text using simple text matching.
        This is a fallback method when embeddings are not available.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, metric_name, description, example_query
            FROM metrics 
            WHERE metric_name LIKE ? OR description LIKE ?
            ORDER BY 
                CASE 
                    WHEN metric_name LIKE ? THEN 1
                    WHEN description LIKE ? THEN 2
                    ELSE 3
                END
            LIMIT ?
        """, (f"%{query_text}%", f"%{query_text}%", f"%{query_text}%", f"%{query_text}%", top_k))
        
        results = []
        for row in cursor.fetchall():
            metric_id, metric_name, description, example_query = row
            results.append({
                'id': metric_id,
                'metric_name': metric_name,
                'description': description,
                'example_query': example_query,
                'labels': self.get_metric_labels(metric_id),
                'templates': self.get_metric_templates(metric_id)
            })
        
        return results
    
    def get_all_metrics(self) -> List[Dict[str, Any]]:
        """Get all metrics from the database."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, metric_name, description, example_query
            FROM metrics 
            ORDER BY metric_name
        """)
        
        results = []
        for row in cursor.fetchall():
            metric_id, metric_name, description, example_query = row
            results.append({
                'id': metric_id,
                'metric_name': metric_name,
                'description': description,
                'example_query': example_query,
                'labels': self.get_metric_labels(metric_id),
                'templates': self.get_metric_templates(metric_id)
            })
        
        return results
    
    def delete_metric(self, metric_id: int) -> bool:
        """Delete a metric and all its associated data."""
        cursor = self.conn.cursor()
        
        try:
            # Delete from vector index if available
            if self.use_vector_search:
                try:
                    cursor.execute("DELETE FROM metrics_vec WHERE rowid = ?", (metric_id,))
                except Exception as e:
                    logger.warning(f"Failed to delete from vector index: {e}")
            
            # Delete templates
            cursor.execute("DELETE FROM metric_templates WHERE metric_id = ?", (metric_id,))
            
            # Delete labels
            cursor.execute("DELETE FROM metric_labels WHERE metric_id = ?", (metric_id,))
            
            # Delete metric
            cursor.execute("DELETE FROM metrics WHERE id = ?", (metric_id,))
            
            self.conn.commit()
            logger.info(f"Deleted metric with ID {metric_id}")
            return True
            
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to delete metric {metric_id}: {e}")
            return False
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Example usage and helper functions
def create_sample_data(vector_db: VectorDB):
    """
    Create sample data for testing the VectorDB.
    In a real implementation, embeddings would be generated using
    a proper embedding model like OpenAI's text-embedding-ada-002.
    """
    import random
    
    # Sample metrics with mock embeddings
    sample_metrics = [
        {
            'name': 'cpu_usage_percent',
            'description': 'CPU usage percentage across all cores',
            'example_query': 'cpu_usage_percent{instance="server1"}',
            'labels': [
                {'name': 'instance', 'examples': 'server1, server2, web-01'},
                {'name': 'cpu_core', 'examples': '0, 1, 2, 3'}
            ],
            'templates': [
                'sum(rate(cpu_usage_percent{{instance="{instance}"}}[5m]))',
                'avg_over_time(cpu_usage_percent{{instance="{instance}"}}[1h])'
            ]
        },
        {
            'name': 'memory_usage_bytes',
            'description': 'Memory usage in bytes',
            'example_query': 'memory_usage_bytes{instance="server1"}',
            'labels': [
                {'name': 'instance', 'examples': 'server1, server2, db-01'},
                {'name': 'memory_type', 'examples': 'used, free, cached'}
            ],
            'templates': [
                'memory_usage_bytes{{instance="{instance}", memory_type="used"}}',
                'sum(memory_usage_bytes{{memory_type="used"}}) by (instance)'
            ]
        },
        {
            'name': 'disk_io_bytes_total',
            'description': 'Total disk I/O operations in bytes',
            'example_query': 'disk_io_bytes_total{device="/dev/sda"}',
            'labels': [
                {'name': 'device', 'examples': '/dev/sda, /dev/nvme0n1'},
                {'name': 'direction', 'examples': 'read, write'}
            ],
            'templates': [
                'rate(disk_io_bytes_total{{device="{device}"}}[5m])',
                'sum(rate(disk_io_bytes_total[5m])) by (device)'
            ]
        }
    ]
    
    for metric_data in sample_metrics:
        # Generate mock embedding (in real usage, use proper embedding model)
        mock_embedding = [random.random() for _ in range(vector_db.embedding_dimension)]
        
        # Add metric
        metric_id = vector_db.add_metric(
            metric_name=metric_data['name'],
            description=metric_data['description'],
            example_query=metric_data['example_query'],
            embedding=mock_embedding
        )
        
        # Add labels
        for label in metric_data['labels']:
            vector_db.add_metric_label(
                metric_id=metric_id,
                label_name=label['name'],
                example_values=label['examples']
            )
        
        # Add templates
        for template in metric_data['templates']:
            vector_db.add_metric_template(
                metric_id=metric_id,
                template=template,
                description=f"Template for {metric_data['name']}"
            )
    
    logger.info("Sample data created successfully")


if __name__ == "__main__":
    # Example usage
    with VectorDB("test_vectordb.sqlite") as vector_db:
        # Create sample data
        create_sample_data(vector_db)
        
        # Test similarity search
        query_embedding = [random.random() for _ in range(512)]
        results = vector_db.similarity_search(query_embedding, top_k=3, threshold=0.1)
        
        print("Similarity search results:")
        for result in results:
            print(f"- {result['metric_name']}: {result['similarity_score']:.3f}")
        
        # Test text search
        text_results = vector_db.search_by_text("cpu", top_k=2)
        print("\nText search results for 'cpu':")
        for result in text_results:
            print(f"- {result['metric_name']}: {result['description']}")