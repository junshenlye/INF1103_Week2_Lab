# Lab 9 predictions recorded before verification

These predictions were prepared with AI assistance from the lab brief and
inspection of the Week 10 code, before running the new Lab 9 demonstration
and tests. They are not a claim about the student's unaided predictions.
Actual observations and explanations are recorded in Predict_First_Notes.docx.

## Initial diagnosis from Section 1.5

- The menu has if/elif branches selecting actions. The original Order has no
  discount branch: it only sums line subtotals. Product serialization selects
  a registered concrete type; that is a persistence concern.
- Five direct PhysicalProduct/DigitalProduct constructor calls occur in
  tests/test_inventory.py, at original lines 32, 35, 53, 54 and 93. Production
  construction is already centralised in product_catalog.create_product,
  which selects a class through PRODUCT_TYPES. It has no scattered named
  constructors to replace. Lab 9 will formalise this as ProductFactory.create.
- float(input("Price: ")) can raise ValueError. The existing outer handler
  avoids a crash but returns to the menu, rather than retrying the same price.
  Missing JSON files are already handled. Bad JSON or invalid records stop
  loading; the new CSV loader should skip invalid rows and keep valid ones.

## 1 Adding a student discount

In the lab's hypothetical if/elif version, Order.calculate_total must change.
With strategies, a StudentDiscount class and its selection at the call site
are enough; Order should remain unchanged. In this implementation, the
existing configurable PercentageDiscount(5) could already express 5 percent,
but a named fourth strategy is included to meet Section 2.4.

## 2 Switching strategies

For an order subtotal of 250, BulkDiscount(200, 20) returns 230.
Replacing it with PercentageDiscount(10) returns 225. StudentDiscount returns
237.50. The percentage applies to the original subtotal, not the previous
discounted result.

## 3 Order and DiscountStrategy relationship

Association: an order uses a strategy without owning its lifecycle.
Each Order has exactly one DiscountStrategy (including a default NoDiscount).
One strategy may be used by zero or more Orders. Therefore Order 0..* -- 1
DiscountStrategy. Two orders can share one PercentageDiscount instance.

## 4 Unknown product type

ProductFactory.create("service", ...) raises ValueError at the explicit
unknown-type guard in ProductFactory.create. If uncaught, execution stops
with a traceback and a nonzero exit code. A caller can catch ValueError and
continue. The sample CSV should report this row and continue.

## 5 Adding BundleProduct

For this project's actual Week 10 baseline, registration was already
centralised: one product_catalog module needed updating, plus adding the
new class module. After the change, one product_factory module needs
updating, plus adding the class module. Normal menu/JSON algorithms need
no edits for a subtype that fits the existing one-extra-field convention.
New tests and UML still need updating in either version. Do not claim this
refactor reduces many scattered production constructors to one: they were
already centralised. Five direct constructor expressions in the old tests
test specific concrete products; adding a new subtype need not edit them.
The registry/factory still changes when a type is added, so the creation
mechanism is not closed to modification. This localised change is an
acceptable small-system tradeoff; a plugin framework would add complexity.
Additional fields or new business rules could require further changes.

## 6 LSP and stock validation

DigitalProduct must preserve Product's non-negative stock invariant. It
must accept valid updates and reject negative counts just like the other
subclasses. Skipping or weakening that rule violates the parent contract.

## 7 Input abc then -5 then 12.50

After abc: Please enter a valid number, e.g. 12.50
After -5: Please enter a number greater than zero.
After 12.50: no error message; return float 12.5.
The prompt is repeated three times. The automated demo supplies inputs
using a mock, so typed input and prompts are not echoed in its transcript.

## 8 CSV loading and the missing-file case

Three products load: P001, D001 and P003. Row numbers include the header.
Expected messages, in order:

    Row 4 skipped: Unknown product type: service
    Row 5 skipped: could not convert string to float: 'abc'
    3 products loaded.
    Load attempt finished.

With the file absent, the outer except FileNotFoundError and finally run;
the outer else does not. Expected messages:

    Products file not found: <requested path>
    Load attempt finished.

The demo uses a guaranteed absent temporary path, equivalent to renaming
the CSV without changing the supplied file. A separate test temporarily
renames a copied CSV to verify the exact lab scenario.
