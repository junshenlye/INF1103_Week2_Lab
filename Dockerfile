FROM python:3.11-slim
WORKDIR /app
COPY src/ .
CMD ["python", "modular_auditor.py"]
