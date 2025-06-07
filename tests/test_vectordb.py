#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import random

print("Starting Enhanced VectorDB test...")

try:
    print("Step 1: Importing VectorDB...")
    from src.services.vectordb import VectorDB
    print("✓ Import successful")
    
    print("Step 2: Creating VectorDB instance...")
    db = VectorDB(db_path=':memory:', embedding_dimension=128)
    print(f"✓ VectorDB created (vector search: {db.use_vector_search})")
    
    print("Step 3: Adding 10 comprehensive metrics with embeddings...")
    
    # Define 10 different metrics with varied characteristics
    metrics_data = [
        {
            "name": "cpu_usage_percent",
            "description": "CPU usage percentage across all cores",
            "query": "cpu_usage_percent{instance=\"server1\"}"
        },
        {
            "name": "memory_usage_bytes",
            "description": "Memory usage in bytes",
            "query": "memory_usage_bytes{instance=\"server1\"}"
        },
        {
            "name": "disk_io_operations_total",
            "description": "Total disk I/O operations",
            "query": "rate(disk_io_operations_total[5m])"
        },
        {
            "name": "network_bytes_transmitted",
            "description": "Network bytes transmitted",
            "query": "rate(network_bytes_transmitted[1m])"
        },
        {
            "name": "http_requests_total",
            "description": "Total HTTP requests received",
            "query": "rate(http_requests_total[5m])"
        },
        {
            "name": "database_connections_active",
            "description": "Number of active database connections",
            "query": "database_connections_active{database=\"postgres\"}"
        },
        {
            "name": "response_time_seconds",
            "description": "HTTP response time in seconds",
            "query": "histogram_quantile(0.95, response_time_seconds_bucket)"
        },
        {
            "name": "error_rate_percent",
            "description": "Error rate percentage",
            "query": "rate(http_errors_total[5m]) / rate(http_requests_total[5m]) * 100"
        },
        {
            "name": "queue_length",
            "description": "Message queue length",
            "query": "queue_length{queue=\"processing\"}"
        },
        {
            "name": "cache_hit_ratio",
            "description": "Cache hit ratio percentage",
            "query": "cache_hits / (cache_hits + cache_misses) * 100"
        }
    ]
    
    metric_ids = []
    
    for i, metric_data in enumerate(metrics_data):
        # Generate random embedding for each metric
        embedding = [random.random() for _ in range(128)]
        
        metric_id = db.add_metric(
            metric_name=metric_data["name"],
            description=metric_data["description"],
            example_query=metric_data["query"],
            embedding=embedding
        )
        metric_ids.append(metric_id)
        print(f"  ✓ Added metric {i+1}/10: {metric_data['name']} (ID: {metric_id})")
    
    print("Step 4: Adding labels for each metric...")
    
    # Define labels for each metric
    labels_data = [
        # CPU labels
        [
            {"name": "instance", "examples": "server1, server2, web-01, db-01"},
            {"name": "cpu_core", "examples": "0, 1, 2, 3, 4, 5, 6, 7"},
            {"name": "mode", "examples": "user, system, idle, iowait"}
        ],
        # Memory labels
        [
            {"name": "instance", "examples": "server1, server2, web-01, db-01"},
            {"name": "memory_type", "examples": "used, free, cached, buffers"}
        ],
        # Disk I/O labels
        [
            {"name": "device", "examples": "/dev/sda, /dev/nvme0n1, /dev/xvda"},
            {"name": "operation", "examples": "read, write"},
            {"name": "instance", "examples": "server1, server2, storage-01"}
        ],
        # Network labels
        [
            {"name": "interface", "examples": "eth0, eth1, lo"},
            {"name": "instance", "examples": "server1, server2, web-01"},
            {"name": "direction", "examples": "tx, rx"}
        ],
        # HTTP requests labels
        [
            {"name": "method", "examples": "GET, POST, PUT, DELETE"},
            {"name": "status", "examples": "200, 404, 500, 503"},
            {"name": "endpoint", "examples": "/api/users, /api/orders, /health"}
        ],
        # Database labels
        [
            {"name": "database", "examples": "postgres, mysql, redis"},
            {"name": "instance", "examples": "db-01, db-02, cache-01"},
            {"name": "pool", "examples": "primary, replica, analytics"}
        ],
        # Response time labels
        [
            {"name": "service", "examples": "api, web, auth"},
            {"name": "endpoint", "examples": "/api/users, /api/orders, /login"},
            {"name": "method", "examples": "GET, POST, PUT, DELETE"}
        ],
        # Error rate labels
        [
            {"name": "service", "examples": "api, web, auth"},
            {"name": "error_type", "examples": "4xx, 5xx, timeout"},
            {"name": "severity", "examples": "critical, warning, info"}
        ],
        # Queue labels
        [
            {"name": "queue", "examples": "processing, notifications, emails"},
            {"name": "priority", "examples": "high, medium, low"},
            {"name": "worker", "examples": "worker-01, worker-02, worker-03"}
        ],
        # Cache labels
        [
            {"name": "cache_type", "examples": "redis, memcached, local"},
            {"name": "instance", "examples": "cache-01, cache-02"},
            {"name": "namespace", "examples": "user_data, session, api_cache"}
        ]
    ]
    
    total_labels_added = 0
    for metric_idx, metric_id in enumerate(metric_ids):
        for label_data in labels_data[metric_idx]:
            label_id = db.add_metric_label(
                metric_id=metric_id,
                label_name=label_data["name"],
                example_values=label_data["examples"]
            )
            total_labels_added += 1
    
    print(f"  ✓ Added {total_labels_added} labels across all metrics")
    
    print("Step 5: Adding templates for each metric...")
    
    # Define templates for each metric
    templates_data = [
        # CPU templates
        [
            'sum(rate(cpu_usage_percent{{instance="{instance}"}}[5m]))',
            'avg_over_time(cpu_usage_percent{{instance="{instance}"}}[1h])',
            'cpu_usage_percent{{instance="{instance}", cpu_core="{cpu_core}"}}'
        ],
        # Memory templates
        [
            'memory_usage_bytes{{instance="{instance}", memory_type="used"}}',
            'sum(memory_usage_bytes{{memory_type="used"}}) by (instance)',
            '(memory_usage_bytes{{memory_type="used"}} / memory_usage_bytes{{memory_type="total"}}) * 100'
        ],
        # Disk I/O templates
        [
            'rate(disk_io_operations_total{{device="{device}"}}[5m])',
            'sum(rate(disk_io_operations_total[5m])) by (device)',
            'disk_io_operations_total{{device="{device}", operation="read"}}'
        ],
        # Network templates
        [
            'rate(network_bytes_transmitted{{interface="{interface}"}}[5m])',
            'sum(rate(network_bytes_transmitted[5m])) by (instance)',
            'network_bytes_transmitted{{interface="{interface}", direction="tx"}}'
        ],
        # HTTP requests templates
        [
            'rate(http_requests_total{{method="{method}"}}[5m])',
            'sum(rate(http_requests_total[5m])) by (endpoint)',
            'http_requests_total{{status=~"2..", endpoint="{endpoint}"}}'
        ],
        # Database templates
        [
            'database_connections_active{{database="{database}"}}',
            'sum(database_connections_active) by (database)',
            'database_connections_active{{database="{database}", pool="primary"}}'
        ],
        # Response time templates
        [
            'histogram_quantile(0.95, response_time_seconds_bucket{{service="{service}"}})',
            'histogram_quantile(0.50, response_time_seconds_bucket{{endpoint="{endpoint}"}})',
            'avg_over_time(response_time_seconds{{service="{service}"}}[5m])'
        ],
        # Error rate templates
        [
            'rate(http_errors_total{{service="{service}"}}[5m]) / rate(http_requests_total{{service="{service}"}}[5m]) * 100',
            'sum(rate(http_errors_total[5m])) by (error_type)',
            'http_errors_total{{severity="critical", service="{service}"}}'
        ],
        # Queue templates
        [
            'queue_length{{queue="{queue}"}}',
            'sum(queue_length) by (queue)',
            'queue_length{{queue="{queue}", priority="high"}}'
        ],
        # Cache templates
        [
            'cache_hits{{cache_type="{cache_type}"}} / (cache_hits{{cache_type="{cache_type}"}} + cache_misses{{cache_type="{cache_type}"}}) * 100',
            'sum(cache_hits) by (cache_type)',
            'rate(cache_misses{{namespace="{namespace}"}}[5m])'
        ]
    ]
    
    total_templates_added = 0
    for metric_idx, metric_id in enumerate(metric_ids):
        for template_idx, template in enumerate(templates_data[metric_idx]):
            template_id = db.add_metric_template(
                metric_id=metric_id,
                template=template,
                template_type="promql",
                description=f"Template {template_idx+1} for {metrics_data[metric_idx]['name']}"
            )
            total_templates_added += 1
    
    print(f"  ✓ Added {total_templates_added} templates across all metrics")
    
    print("Step 6: Getting all metrics...")
    metrics = db.get_all_metrics()
    print(f"✓ Found {len(metrics)} metrics with labels and templates")
    
    for metric in metrics:
        print(f"  - {metric['metric_name']}: {len(metric['labels'])} labels, {len(metric['templates'])} templates")
    
    print("Step 7: Testing similarity search with random embeddings...")
    
    # Generate a random query embedding
    query_embedding = [random.random() for _ in range(128)]
    
    # Perform similarity search
    similar_metrics = db.similarity_search(
        query_embedding=query_embedding,
        top_k=5,
        threshold=0.0  # Low threshold to get results
    )
    
    print(f"✓ Found {len(similar_metrics)} similar metrics")
    
    if similar_metrics:
        print("  Top similar metrics:")
        for i, metric in enumerate(similar_metrics, 1):
            similarity = metric.get('similarity_score', 'N/A')
            print(f"    {i}. {metric['metric_name']}: {similarity}")
            print(f"       Description: {metric['description']}")
            print(f"       Labels: {len(metric['labels'])}, Templates: {len(metric['templates'])}")
    
    print("Step 8: Testing text search...")
    
    # Test text search for different terms
    search_terms = ["cpu", "memory", "http", "database", "error"]
    
    for term in search_terms:
        results = db.search_by_text(term, top_k=3)
        print(f"  Text search for '{term}': {len(results)} results")
        for result in results:
            print(f"    - {result['metric_name']}")
    
    print("Step 9: Testing individual metric retrieval...")
    
    # Test getting specific metrics by name
    test_metric = db.get_metric_by_name("cpu_usage_percent")
    if test_metric:
        print(f"✓ Retrieved metric: {test_metric['metric_name']}")
        print(f"  Labels: {[label['label_name'] for label in test_metric['labels']]}")
        print(f"  Templates count: {len(test_metric['templates'])}")
    
    print("Step 10: Closing database...")
    db.close()
    print("✓ Database closed")
    
    print("\n🎉 Enhanced VectorDB test completed successfully!")
    print(f"📊 Summary:")
    print(f"  - Added 10 metrics with embeddings")
    print(f"  - Added {total_labels_added} labels")
    print(f"  - Added {total_templates_added} templates")
    print(f"  - Performed similarity search with random embeddings")
    print(f"  - Tested text search for multiple terms")
    print(f"  - Verified individual metric retrieval")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
