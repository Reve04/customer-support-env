FROM python:3.11-slim-bookworm

WORKDIR /app

COPY requirements.txt .

# Install torch CPU-only first (smaller, avoids CUDA 2GB+ download)
RUN pip install --no-cache-dir --timeout=300 --retries=5 \
    torch==2.2.2+cpu --index-url https://download.pytorch.org/whl/cpu

# Install remaining dependencies
RUN pip install --no-cache-dir --timeout=300 --retries=5 \
    -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["python", "-m", "uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]