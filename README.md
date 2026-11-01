# Week 9 — Lab 7 Inventory Management

Extends the Week 8 OOP design in a fresh clone of https://github.com/junshenlye/INF1103_Week2_Lab.git. The remote baseline was Week 5; the Product/Inventory separation was carried forward from the local Wk8 implementation. Previous week folders are unchanged.

## Run

Python 3.9+ (Docker uses 3.11); no third-party Python packages.

```sh
python3 inventory_manager.py
python3 -m unittest discover -s tests -v
docker build -t inf1103-week9 .
docker run --rm -it -v "${PWD}:/app" -w /app inf1103-week9
docker run --rm -v "${PWD}:/app" -w /app inf1103-week9 python -m unittest discover -s tests -v
```

Menu: 1 display, 2 add, 3 set stock, 4 search, 5 save, 6 save and exit. Adding asks for type, common fields, then weight (kg), download size (MB), or subscription duration (whole months). Shipping costs $5/kg. Price and stock cannot be negative; weight/size/duration must be positive. IDs are case-insensitive and unique. `INVENTORY_FILE` overrides the default `inventory.json`. Missing files start empty; invalid files are reported without overwriting them. Saving uses an atomic replacement. Legacy Week 8 JSON lacks types and must be explicitly classified before loading; this submission includes typed sample data.

## Design and reflection (including optional task)

Product encapsulates common state and stock validation. Its abstract fulfilment method prevents generic instances. Subclasses call `super()` in constructors and display overrides. PhysicalProduct implements CanBeShipped with `class PhysicalProduct(Product, CanBeShipped)`: Python spells interface implementation as multiple bases, but there is only one product implementation superclass. CanBeShipped contains no product state or shipping algorithm. DigitalProduct and SubscriptionProduct have no shipping capability.

Inventory only manages Product objects and delegates display. Menu functions own input; file functions own JSON I/O. `product_catalog.py` owns the type registry and object/record conversion. Functions are not UML classes.

Adding SubscriptionProduct required its own module and one registry entry/import. Product, Inventory, menu and persistence algorithms did not change for that extension. The registry is a factory approach rather than another inheritance layer. A larger system could discover registered plugins to eliminate even the central registry edit. OCP still has a configuration boundary: extension requires registering the constructor, field and prompt. See `uml.svg` (viewable diagram) and `uml.mmd` (editable detailed UML).

## Verification and submission

See CHECKLIST.md and evidence/ for actual test outputs, Docker build/menu/restart logs and Git workflow. Screenshots, where supplied, are explicitly labeled with their capture context. All required source, diagram, JSON, tests and evidence are packaged in INF1103_Week9_Submission.zip. Upload that ZIP through your course submission system.
