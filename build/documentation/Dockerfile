FROM python:3.11-alpine

# Set build directory
WORKDIR /tmp

# Copy files necessary for build
COPY requirements.txt requirements.txt

# COPY setup.py setup.py

# Perform build and cleanup artifacts
RUN apk add --no-cache \
    git curl \
    && apk add --no-cache --virtual .build gcc musl-dev \
    && pip install --user -r requirements.txt \
    && apk del .build gcc musl-dev \
    && rm -rf /tmp/*

ENV PATH=$PATH:/root/.local/bin
# Set working directory

RUN mkdir /app
WORKDIR /app
COPY ./ ./

# Expose MkDocs development server port
EXPOSE 8000

# Start development server by default
ENTRYPOINT ["mkdocs"]
CMD ["serve", "--dev-addr=0.0.0.0:8000"]