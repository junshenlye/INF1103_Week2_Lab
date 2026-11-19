# INF1103 Week 11 Lab 9

Inventory Management System with discount strategies, a product factory,
validation and CSV loading.

## Files

- `src/main.py`: start the inventory menu.
- `src/inventory_examples.py`: examples of discounts, validation and CSV loading.
- `src/inventory_storage.py`: load and save inventory files.
- `src/product_records.py`: convert products to and from JSON records.
- `src/input_validation.py`: read a valid positive price.
- `src/tests/`: automated tests.
- `documents/predictions_and_reflection.docx`: prediction notes and reflections.
- `uml.pdf`: class diagram.
- `Screenshots/`: Docker terminal proof in the submission folder.
- `log.txt`: Git history in the submission folder.

The remaining Python files are named after their classes.

## Run locally

From the project folder:

```sh
cd src
python3 main.py
python3 inventory_examples.py
python3 -m unittest discover -s tests -v
```

Python 3.9 or later is required. No extra Python packages are needed.

## Docker

Run these from the project folder, where Dockerfile is located:

```sh
docker build -t inf1103-week11 .
docker run --rm inf1103-week11 python -m unittest discover -s tests
docker run --rm -it inf1103-week11
```

The sample CSV has no weight or download-size fields. The factory uses
1 kg for physical products and 1 MB for digital products when those values
are omitted. The subscription default is 12 months. The menu asks for the
actual value when adding a product.
