FROM debian:12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 python3-pip python3.11-dev ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/bin/python3.11 /usr/bin/python

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout=300 --retries=5 \
    "torch==2.2.2+cpu" --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir --timeout=300 --retries=5 -r requirements.txt
COPY . .
EXPOSE 7860
CMD ["python", "-m", "uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
