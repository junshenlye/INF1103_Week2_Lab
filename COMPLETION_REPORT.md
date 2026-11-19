# INF1103 Week 11 Lab 9 completion report

The Week 10 system has been extended in a separate Week 11 project. The
original Wk9 project and submission have not been changed.

## Requirements and evidence

| Lab requirement | Implementation or deliverable | Verification |
| --- | --- | --- |
| Section 1 diagnosis | Predict_First_Predictions.md and Predict_First_Notes.docx | Original creation sites, behaviour selection and failure points inspected |
| Abstract discount strategy | discount_strategy.py | Abstract base cannot be instantiated |
| NoDiscount, PercentageDiscount, BulkDiscount | discount_strategy.py | Totals and percentage/threshold boundaries tested |
| Default strategy and runtime switching | order.py | 250 without discount, 230 bulk, 225 percentage on the same order |
| Fourth strategy without editing Order | StudentDiscount in discount_strategy.py | 237.50 student total; independent FiveOff extension tested |
| No discount if/elif inside Order total | order.py | Delegation and absence of branching in calculate_total checked |
| Static ProductFactory.create returning Product | product_factory.py | Physical, digital and subscription products; explicit extra values and unknown types tested |
| Replace direct product construction | Menu, JSON, CSV, demo and tests use the factory | Named concrete constructors are no longer called outside the factory registry |
| Positive product prices | product.py | Zero, negative, boolean, non-number and non-finite values rejected |
| Non-negative stock and LSP | product.py and inherited subclasses | Construction/update checks across all product types |
| Positive OrderLine quantities | order_line.py | Invalid quantity leaves the order unchanged |
| Retry positive price input | input_helpers.py and menu | abc, -5, 12.50 exact messages plus full menu flow tested |
| CSV loader with try/except/else/finally | file_handling.load_products | Missing files, renamed copied file, invalid rows, duplicates, empty file and final message tested |
| Provided CSV data | products.csv | Three valid IDs loaded: P001, D001, P003 |
| Updated UML and multiplicities | UML.pdf, uml.mmd, two SVG views | Both PDF pages rendered and visually inspected against the code |
| All Predict First activities | Predict_First_Notes.docx | Eight predictions with observations/comparisons; Word pages rendered and inspected |
| Optional reflections | Final page of prediction notes | All reflection topics addressed without inventing group-project details |
| Automated tests folder | tests/test_inventory.py and tests/test_lab9.py | 36 tests pass locally on Python 3.9 and in Docker on Python 3.11 |
| Run in Docker | Dockerfile and evidence/docker-demo.txt | Self-contained image builds, tests and demonstration succeed |
| Git workflow | week11-lab9 branch and evidence/git-workflow.txt | Status, staging, commit, push and history captured |
| Workflow screenshots | evidence/*-workflow.png | Actual browser screenshots of saved workflow output, labelled as an evidence viewer |

## Design decisions

The existing project already centralised product creation. Lab 9 formalises
that responsibility as a factory rather than introducing another independent
creation mechanism. Type registration still changes when a subtype is added,
which is the deliberate small-system OCP tradeoff discussed in the lab.

The supplied CSV has no weight or download-size columns. The factory uses
documented demonstration defaults (1 kg and 1 MB) when these values are
omitted; an explicit extra argument overrides them. Subscription products,
retained from the existing system, default to 12 months when omitted.

The core UML now shows shared Inventory aggregation (0..* at both ends),
matching what the code permits. Order and DiscountStrategy are associated:
one strategy per order and zero or more orders per strategy. The factory has
a dashed «creates» dependency to Product and does not retain created objects.

## Reading the evidence

The prediction notes identify AI assistance. The predictions were recorded
before running the new Lab 9 checks; they are not a claim about the student's
unaided thought process. Review the notes and make sure you can explain the
design and outputs before submitting.

The screenshots show a local browser viewer of actual captured command
output. They are not interactive terminal screenshots. The raw Docker,
demonstration, test and Git output is also included for inspection.

GitHub Actions is configured to run tests after a push. Local and Docker
results are established independently of the remote workflow result.

No school submission portal has been used. The submission ZIP is prepared
locally for the student to review and upload.
