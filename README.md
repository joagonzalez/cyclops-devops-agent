# Cyclops-DevOps-Agent
![Python](https://img.shields.io/badge/python-v3.12.x-orange)
![Python](https://img.shields.io/badge/platform-linux-blue)
[![Build Status](https://github.com/joagonzalez/python-seed-v2/actions/workflows/pipeline.yml/badge.svg)](https://github.com/joagonzalez/python-seed-v2/actions/workflows/pipeline.yml)
[![Documentation](https://readthedocs.org/projects/python-seed-v2/badge/?)](https://python-seed-v2.readthedocs.io/en/latest/)
[![Coverage Status](https://coveralls.io/repos/github/joagonzalez/python-seed-v2/badge.svg?branch=master)](https://coveralls.io/github/joagonzalez/python-seed-v2?branch=master)

Natural Language to PromQL Agent for infrastructure monitoring prototype

---
**Content**
- [Getting started](#getting-started)
- [Branch strategy](#branch-strategy)
- [Documentation](#documentation)
- [CICD Pipeline ](#cicd-pipeline)
- [Build](#build)
- [Run](#run)
    - [Local development](#local-development)
    - [Production](#production)
- [References](#references)
---

## Getting started

**Cyclops** is a prototype framework that leverages large language models (LLMs) for converting natural language queries into PromQL, simplifying infrastructure monitoring and metrics analysis. The current implementation focuses on few-shot learning and semantic search to extract user intent and generate accurate PromQL queries. While the prototype does not yet utilize a knowledge graph, future iterations may explore its integration to enhance context understanding and query generation. **Cyclops** is designed with flexibility in mind, making it adaptable to other monitoring systems beyond Prometheus with minimal adjustments and easily extensible to support new systems through the use of the MCP protocol.

![Prototype Diagram](docs/project/prototypes.png)

![Few Show Learning](docs/project/fewshot.png)

## Branch strategy
The following diagram describes the branch strategy used in the context of this template repository. The ideas was to simplify git flow due to it is oriented to single developer or very small teams with only one production stage.

The workflow consists of release candidate branches (rc-\*) that will be branched from master. Master branch will always have a tag with a tested and approved version which will be the result of a rc-\* branch merge. Developers will create feature branches (feature-<issue_number>-\*) from rc-\* branches.

Events:
- commit on feature branch: Trigger code quality checks and unit tests
- commit on release candidate branch: Trigger code quality checks, unit tests, docker image building, image push tor registry and deploy on VPS
- commit on master: Trigger code quality checks and unit tests, create release at Github to create version package

<img src="docs/pipelines/branch_strategy_python.png" />

## Documentation
Mkdocs with [readthedocs](https://readthedocs.org/) service is being used to automatically publish service documentation. This approach was prefered over local Mkdocs service due serverless simplicity.

Static documentation is generated at *docs/* folder and is deployed when a release candidate branch is merged with master.

Docs URL is published in badge in this README.

Once configured via the Read the Docs UI, a webhook is automatically added to the repository. This webhook listens for new merge commits to the `master` branch and triggers the documentation rebuild process by sending an HTTPS request to Read the Docs.

## CICD Pipeline
The pipeline leverages GitHub Actions, installing all required dependencies directly on the GitHub-hosted runner. Conditional steps are used to control workflow execution based on branch naming, allowing a single pipeline to handle different scenarios. Notifications on success and failure are sent to a specific Telegram bot using callbacks.

<img src="docs/pipelines/pipeline.png" />

## Build
```bash
build-images # build api image and documentation image, only for development
```

## Run
How to execute code and services for local development and prod environments.

### Local development
Use the Makefile
```bash
make install # install dependencies
make code-quality
make test
make doc # run mkdocs development server
make run # run api using local uvicorn
```

To deploy the application locally on a Minikube Kubernetes cluster, use the provided Makefile command:

```bash
# Not implemented yet
make deploy-minikube # deploys the application to your local Minikube cluster
```

### Production
Merge your feature branch to release candidate branch to execute deploy pipeline. Public URLs for documentation and api are defined on docker-compose. Take into consideration that public DNS must be created before the deployment because an automatic process will create a Let's Encrypt certificate right after the container is up and running in the server.

## References
- PromAssistant: Leveraging Large Language Models for
Text-to-PromQL
- Xpert: Empowering Incident Management
with Query Recommendations via Large Language Models