FROM python:3.11-slim
WORKDIR /app
COPY *.py ./
COPY inventory.json ./
COPY products.csv ./
COPY tests ./tests
CMD ["python", "-u", "inventory_manager.py"]
