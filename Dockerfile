FROM python:3.11-slim
WORKDIR /app
COPY src/ .
CMD ["python", "persistent_auditor.py"]
