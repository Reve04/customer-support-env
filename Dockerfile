FROM python:3.11.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --timeout=120 \
    torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir --timeout=120 -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["python", "-m", "uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]