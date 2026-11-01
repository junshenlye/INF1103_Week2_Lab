# Week 9 assignment checklist

- [x] Create Wk9 and clone the GitHub repository; use Wk8 OOP design as reference.
- [x] §1: PhysicalProduct extends Product; super constructor; weight in kg.
- [x] §1: DigitalProduct extends Product; super constructor; download size in MB.
- [x] §2: Both display overrides reuse super().display_information(); verify common and additional fields.
- [x] §3: Product inherits ABC; abstract get_fulfilment_info(); both concrete implementations; direct Product instantiation raises TypeError in tests.
- [x] §4: Independent CanBeShipped interface ABC; physical implementation; different-weight shipping tests; digital has no shipping behavior.
- [x] §5: Display, add with type choice, update stock, search, save/load and exit.
- [x] §5: Inventory manages objects and delegates product behavior.
- [x] §5: Typed JSON retains subclass fields; actual Docker save/restart verified.
- [x] §6: All six application classes in UML, abstract/interface labels, inheritance, realisation and Inventory aggregation; SVG and Mermaid source.
- [x] §7: Seven meaningful tests pass locally and in Docker; input validation and malformed JSON checks included.
- [x] §8 optional: SubscriptionProduct and written OCP reflection; registry extension without editing base/menu/persistence algorithms.
- [x] §9: .gitignore excludes caches, environments, secrets and IDE settings.
- [x] §9: Git status, staged diff, meaningful commit, history and remote push (see evidence/git-workflow.txt).
- [x] §9: Docker build, mounted execution and tests (see evidence/).
- [x] Submission: Python sources, UML, updated typed JSON and test data.
- [x] Submission: Browser screenshots of actual recorded Git and Docker workflow outputs; raw logs supplied. These are transcript views, not native Terminal screenshots (Terminal access denied by computer-use policy).
- [x] Submission: ZIP containing the required files and evidence.
- [ ] Upload ZIP to course submission portal (user action; portal not provided).

## Docker cleanup

Removed all old build cache and unused images. Preserved containers and data volumes. Kept the new inf1103-week9 image for this assignment and cleared its build cache after verification. Final disk summary: evidence/docker-cleanup.txt.
