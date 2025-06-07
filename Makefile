run:
	API_VERSION=$$(cat VERSION) uv run python run.py

install:
	uv sync

typehint:
	uv run mypy src/ tests/

test-local:
	uv run pytest tests/ -v --cov

test:
	uv run pytest tests/ -v --cov --cov-report=xml:coverage.xml

test-vectordb:
	uv run python tests/test_vectordb.py

lint:
	uv run ruff check src/ tests/ 

format:
	uv run ruff check src/ tests/ --fix

doc:
	uv run mkdocs serve

build-images:
	@echo "Implement build images"

deploy-local:
	@echo "Implement deploy within local environment"

deploy:
	@echo "Implement deploy within k8s cluster"

clean:
	rm -rf .*_cache coverage.xml .*coverage site report

checklist: typehint lint test clean

code-quality: typehint lint clean

coverage-publish:
	uv run coveralls

KUBE_PROM_VALUES := build/k8s/monitoring/kube-prometheus-values.yaml
TRAEFIK_FILES := build/k8s/monitoring/middleware-https-grafana.yaml build/k8s/monitoring/ingressroute-http-grafana.yaml build/k8s/monitoring/ingressroute-https-grafana.yaml

deploy-monitoring:
	@echo "🛰️  Deploying monitoring stack..."
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts || true
	helm repo update
	helm upgrade --install monitoring prometheus-community/kube-prometheus-stack \
		--namespace monitoring --create-namespace \
		--values $(KUBE_PROM_VALUES)
	kubectl apply -f build/k8s/monitoring/ingressroute-https-grafana.yaml
	kubectl apply -f build/k8s/monitoring/middleware-https-grafana.yaml
	kubectl apply -f build/k8s/monitoring/ingressroute-http-grafana.yaml
	@echo "✅ Monitoring stack deployed. Grafana at https://analytics.qwerty.com.ar"


.PHONY: checklist