FROM python:3.12-slim

# Set build directory
WORKDIR /tmp

# Perform build and cleanup artifacts
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --user uv

ENV PATH=$PATH:/root/.local/bin

# Set working directory
RUN mkdir /app
WORKDIR /app
COPY ./ ./

# Install torch==cpu to avoid issues with onnxruntime
RUN python -m pip install --no-cache-dir torch==2.3.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

# Install dependencies using uv
RUN uv sync

# Expose FastAPI development server port
EXPOSE 5000

# Start development server by default
ENTRYPOINT ["uv", "run", "python", "run.py"]
CMD ["uv", "run", "python", "run.py"]