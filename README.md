# INF1103 Week 11 Lab 9

Inventory Management System extended from Week 10 Lab 8 with Strategy,
Factory, validation, specific exception handling and automated tests.

## Run

Requires Python 3.9 or later. No third-party Python packages are needed.

```sh
python3 inventory_manager.py
python3 demo_lab9.py
python3 -m unittest discover -s tests -v
```

The menu supports product CRUD, JSON saving and CSV import (option 8).
Price input is retried until it is finite and greater than zero. The demo
uses a separate in-memory inventory and never changes inventory.json.

## Docker

```sh
docker build -t inf1103-week11 .
docker run --rm inf1103-week11 python -m unittest discover -s tests -v
docker run --rm inf1103-week11 python demo_lab9.py
docker run --rm -it -v "${PWD}:/app" -w /app inf1103-week11
```

Tests and sample CSV are included in the image. The last command mounts
the current directory so interactive JSON changes persist on the host.
The image uses Python 3.11; local verification also covers Python 3.9.

## Design

- `Order` delegates its subtotal to a `DiscountStrategy`. Its default is
  `NoDiscount`; use `set_discount()` to switch an existing order.
- `PercentageDiscount`, `BulkDiscount` and the fourth strategy,
  `StudentDiscount` (5%), are interchangeable. Bulk discounts start at the
  inclusive threshold and never make the total negative.
- `ProductFactory.create()` is the only product creation decision. Menu,
  JSON loader, CSV loader, demo and tests call it. The registry supports
  physical, digital and subscription products. Unknown types raise ValueError.
- `Product` owns validation for finite positive prices and non-negative
  integer stock. `OrderLine` requires a positive integer quantity. Boolean
  values are rejected where they could be mistaken for numbers.
- `load_products()` uses try/except/else/finally, reports a missing file,
  catches ValueError per row, keeps valid rows, reports the successful count
  and always prints `Load attempt finished.`.

The supplied five-column `products.csv` omits subtype-specific attributes.
For this lab, the factory uses explicit demonstration defaults when `extra`
is omitted: physical weight 1 kg, digital download size 1 MB, subscription
duration 12 months. Pass `extra` to provide a real value; the menu and JSON
loader retain explicit values. These defaults are not inferred product data.

## Relationships

- Product -- Supplier: association; one supplier per product.
- Inventory aggregates products; products are independent and can be shared.
- Order owns and creates its OrderLine objects through composition.
- OrderLine -- Product: association.
- Order -- DiscountStrategy: association; one strategy per order, zero or
  more orders per strategy. Strategies can be shared.
- ProductFactory ..> Product: creation dependency, labelled `«creates»`.

`UML.pdf` contains two landscape sheets: the complete core model and the
pattern extensions. `uml.mmd` is the editable Mermaid diagram;
`uml-core.svg` and `uml-patterns.svg` are vector views of the PDF sheets.

## Notes and verification

`Predict_First_Predictions.md` was recorded before running the new Lab 9
verification. `Predict_First_Notes.docx` contains all eight predictions,
actual observations, comparisons, the initial diagnosis and optional
reflections. It identifies AI assistance and should be reviewed by the student.

The 36 automated tests cover the prior relationships and LSP contract,
discount switching and extension, boundaries and invalid values, factory
creation, price retries, missing and renamed CSV files, invalid and duplicate
rows, the finally message, menu imports and persistence. GitHub Actions is
configured to run the same tests on pushes and pull requests.

`evidence/` contains captured command output and screenshots of the local
evidence viewer. Those screenshots display actual saved output; they are
not screenshots of an interactive terminal. `COMPLETION_REPORT.md` maps
the lab requirements to files and checks.

Repository: https://github.com/junshenlye/INF1103_Week2_Lab
Branch: `week11-lab9`
