FROM python:3.11-slim

WORKDIR /app
COPY inventory_manager.py .

ENV INVENTORY_FILE=/data/inventory.json
RUN mkdir -p /data
VOLUME ["/data"]

CMD ["python", "-u", "inventory_manager.py"]
