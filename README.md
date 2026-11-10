# INF1103 Week 10 Lab 8

This inventory management system demonstrates association, aggregation,
composition, type hints, Liskov substitution and polymorphism.

## Object relationships

- `Product` is associated with one independently created `Supplier`.
- `Inventory` aggregates independently created `Product` objects.
- `Order` creates and owns its `OrderLine` objects.
- `OrderLine` refers to a `Product` without owning that product.
- `PhysicalProduct`, `DigitalProduct` and `SubscriptionProduct` satisfy the
  common abstract `Product` contract.

The editable class diagram is in `uml.mmd`. `UML.pdf` and `uml.svg` are
rendered copies.

## Run and test locally

```sh
python3 inventory_manager.py
python3 -m unittest discover -s tests -v
```

The menu supports displaying, adding, updating, searching and removing
products. Products retain their supplier association when saved to JSON.
Products loaded with the same supplier ID share the same `Supplier` object.

## Run and test with Docker

```sh
docker build -t inf1103-week10 .
docker run --rm inf1103-week10 python -m unittest discover -s tests -v
docker run --rm -it -v "${PWD}:/app" -w /app inf1103-week10
```

The Docker image uses Python 3.11. The application itself also runs on the
course machine's Python 3.9 installation.
