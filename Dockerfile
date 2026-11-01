FROM python:3.11-slim
WORKDIR /app
COPY *.py ./
COPY inventory.json ./
CMD ["python", "-u", "inventory_manager.py"]
