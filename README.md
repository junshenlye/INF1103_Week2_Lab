# INF1103 Week 11 Lab 9

Inventory Management System with discount strategies, a product factory,
input validation and CSV loading.

## Run

```sh
python3 inventory_manager.py
python3 demo_lab9.py
python3 -m unittest discover -s tests -v
```

The menu includes CSV import as option 8. The demo shows the discount
calculations and error handling without changing the saved inventory.

## Docker

```sh
docker build -t inf1103-week11 .
docker run --rm inf1103-week11 python -m unittest discover -s tests -v
docker run --rm inf1103-week11 python demo_lab9.py
docker run --rm -it -v "${PWD}:/app" -w /app inf1103-week11
```

Python 3.9 or later is required. No extra Python packages are needed.

## Files

- Python files and `tests/`: program and automated tests.
- `products.csv`: sample file from the lab.
- `inventory.json`: saved inventory.
- `UML.pdf`: class diagram.
- `Predict_First_Notes.docx`: predictions, results and reflections.
- `evidence/`: test output and workflow screenshots.

The sample CSV has no weight or download-size fields. The factory uses
1 kg for physical products and 1 MB for digital products when these values
are omitted. The subscription default is 12 months. The menu still asks
for the actual value when adding a product.
