FROM python:3.11-alpine

# Set build directory
WORKDIR /tmp

# Perform build and cleanup artifacts
RUN apk add --no-cache \
    git curl \
    && apk add --no-cache --virtual .build gcc musl-dev make\
    && apk del .build gcc musl-dev \
    && rm -rf /tmp/*

# Install uv
RUN pip install --user uv

ENV PATH=$PATH:/root/.local/bin

# Set working directory
RUN mkdir /app
WORKDIR /app
COPY ./ ./

# Install dependencies using uv
RUN uv sync

# Expose FastAPI development server port
EXPOSE 5000

# Start development server by default
ENTRYPOINT ["uv", "run", "python", "run.py"]
CMD ["uv", "run", "python", "run.py"]