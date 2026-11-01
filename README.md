# INF1103 Week 9: Inheritance, Overriding and Abstraction

Inventory management with physical, digital and subscription products. Requires Python 3.9+; no additional Python packages.

## Run

```sh
python3 inventory_manager.py
python3 -m unittest discover -s tests -v
```

## Docker

```sh
docker build -t inf1103-week9 .
docker run --rm -it -v "${PWD}:/app" -w /app inf1103-week9
docker run --rm -v "${PWD}:/app" -w /app inf1103-week9 python -m unittest discover -s tests -v
```

The menu supports displaying, adding, searching, updating stock, saving and exiting. Adding a product asks for its type and the relevant weight (kg), download size (MB) or subscription duration (whole months). Physical shipping costs $5/kg. Inventory is saved to `inventory.json`; `INVENTORY_FILE` can select another path. JSON records retain product types and their additional fields.

`uml.svg` contains the class diagram; `uml.mmd` is its editable Mermaid source.

## Optional reflection

SubscriptionProduct required a new module and a registry entry in `product_catalog.py`. Product, Inventory, the menu and file-handling algorithms did not need to change for the new type. The registry provides a shared factory for input and persistence. Plugin discovery could remove the central registration edit in a larger system.
