FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Install all dependencies (no torch needed - grader uses keyword matching)
RUN pip install --no-cache-dir --timeout=300 --retries=5 \
    -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["python", "-m", "uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
