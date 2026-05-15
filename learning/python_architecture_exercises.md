# Python Architecture Exercises
## Async SQLAlchemy · QuerySpecs · Strawberry GraphQL · TDD · Hexagonal Architecture

**Domain:** E-commerce (products, orders, customers)
**Target:** SSr Python developer, comfortable with Python, light on async and Strawberry
**Goal:** Understand *why* we build things the way we do — UoW, QuerySpecs, layered architecture — not just *how*

---

## Part 0 — Setup

This is a standalone repo. No existing codebase. You build it from scratch.
Everything runs inside Docker — no local MySQL installation needed.

### 0.1 Prerequisites

- Python 3.12
- `uv` installed (`pip install uv` or via [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/))
- Docker + Docker Compose

### 0.2 Create the project

```bash
mkdir ecommerce-exercises && cd ecommerce-exercises
uv init
uv python pin 3.12
```

### 0.3 Install dependencies

```bash
uv add sqlalchemy aiomysql alembic strawberry-graphql fastapi uvicorn pytest pytest-asyncio pytest-mock
```

Your `pyproject.toml` should now list all of these under `[project.dependencies]`.

### 0.4 Project structure

Create this folder layout manually:

```
ecommerce-exercises/
├── src/
│   └── ecommerce/
│       ├── domain/
│       │   ├── entities.py
│       │   ├── repository.py
│       │   ├── interfaces.py
│       │   └── use_cases/
│       │       └── __init__.py
│       ├── infrastructure/
│       │   ├── database.py
│       │   ├── entity_mappings.py
│       │   ├── uow.py
│       │   └── repos/
│       │       └── __init__.py
│       └── application/
│           └── gql/
│               ├── entities.py
│               └── query.py
├── tests/
│   ├── conftest.py
│   ├── domain/
│   └── infrastructure/
├── alembic/
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

### 0.5 Dockerfile

Create `Dockerfile` in the project root:

```dockerfile
FROM python:3.12-slim

# Install uv
RUN pip install uv

WORKDIR /app

# Copy dependency files first (layer caching)
COPY pyproject.toml .
COPY uv.lock* .

# Install dependencies
RUN uv sync

# Copy source code
COPY src/ src/
COPY tests/ tests/
COPY alembic/ alembic/
COPY alembic.ini .

ENV PYTHONPATH=/app/src

CMD ["uv", "run", "uvicorn", "ecommerce.application.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 0.6 docker-compose.yml

Create `docker-compose.yml` in the project root:

```yaml
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: ecommerce
    ports:
      - "3306:3306"
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-uroot", "-proot"]
      interval: 5s
      timeout: 5s
      retries: 10

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: mysql+aiomysql://root:root@db:3306/ecommerce
    depends_on:
      db:
        condition: service_healthy

  test:
    build: .
    environment:
      DATABASE_URL: mysql+aiomysql://root:root@db:3306/ecommerce
      DB_HOST: db
      DB_USER: root
      DB_PASS: root
    depends_on:
      db:
        condition: service_healthy
    command: ["uv", "run", "pytest", "tests/", "-v"]
```

### 0.7 Start the environment

To start MySQL and the app:
```bash
docker compose up db app
```

To run all tests inside Docker:
```bash
docker compose run --rm test
```

To run tests locally (against the Dockerized MySQL):
```bash
docker compose up db -d   # start only MySQL in background
uv run pytest tests/ -v
```

The second option (local tests, Docker MySQL) is recommended during development — faster feedback loop.

### 0.8 Configure Alembic

```bash
uv run alembic init alembic
```

Edit `alembic.ini`:
```ini
sqlalchemy.url = mysql+aiomysql://root:root@localhost:3306/ecommerce
```

Edit `alembic/env.py` to import your metadata before `run_migrations_offline()`:
```python
from ecommerce.infrastructure.entity_mappings import mapper_registry
target_metadata = mapper_registry.metadata
```

To run migrations inside Docker:
```bash
docker compose run --rm app uv run alembic upgrade head
```

Or locally with MySQL running in Docker:
```bash
uv run alembic upgrade head
```

### 0.9 Configure pytest

Add to `pyproject.toml`:
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

### 0.10 Base `conftest.py`

The conftest reads DB connection params from environment variables — same values work
whether you run tests locally or inside Docker via `docker compose run test`.

```python
# tests/conftest.py
import asyncio
import binascii
import os

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker

# Reads from env — works both locally (db on localhost) and inside Docker (db on "db" host)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "root")
DB_PORT = os.getenv("DB_PORT", "3306")

BASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def dbname():
    # Each test session gets a fresh isolated database
    return "test_{}".format(binascii.b2a_hex(os.urandom(6)).decode("ascii"))


@pytest.fixture(scope="session")
async def engine(event_loop, dbname):
    # Create the test database
    base_engine = create_async_engine(f"{BASE_URL}/?charset=utf8", isolation_level="AUTOCOMMIT")
    async with base_engine.connect() as conn:
        await conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {dbname}"))
    await base_engine.dispose()

    # Connect to the test database and create all tables from ORM metadata
    url = f"{BASE_URL}/{dbname}?charset=utf8"
    _engine = create_async_engine(url, echo=True)

    from ecommerce.infrastructure import entity_mappings  # noqa: F401 — triggers table registration
    from ecommerce.infrastructure.database import mapper_registry
    async with _engine.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)

    yield _engine

    # Teardown — drop the test database
    await _engine.dispose()
    base_engine2 = create_async_engine(f"{BASE_URL}/?charset=utf8", isolation_level="AUTOCOMMIT")
    async with base_engine2.connect() as conn:
        await conn.execute(text(f"DROP DATABASE IF EXISTS {dbname}"))
    await base_engine2.dispose()


@pytest.fixture()
async def dbsession(engine):
    """
    Each test gets a fresh session wrapped in a SAVEPOINT transaction
    that is rolled back after the test — no data leaks between tests.
    """
    from asyncio import current_task
    conn = await engine.connect()
    trans = await conn.begin()
    async_session = sessionmaker(conn, expire_on_commit=False, class_=AsyncSession)
    scoped = async_scoped_session(async_session, scopefunc=current_task)
    try:
        yield scoped
    finally:
        await scoped.close()
        await trans.rollback()
        await conn.close()
```

### 0.11 Base `database.py`

```python
# src/ecommerce/infrastructure/database.py
from sqlalchemy.orm import registry

mapper_registry = registry()
```

---

## Conceptual Foundation — Read Before Exercising

### Why layers?

The architecture has three layers:

```
application/   ← GraphQL resolvers. Knows about HTTP/GQL. Calls use cases.
domain/        ← Business logic. Knows nothing about DB or GQL.
infrastructure/← SQLAlchemy tables, repos, UoW. Implements domain interfaces.
```

**Rule:** inner layers never import from outer layers.
`domain/` never imports from `infrastructure/` or `application/`.

### Why Unit of Work (UoW)?

The UoW is a context manager that groups all DB operations into a single transaction.
It owns the session and all repos. When the block exits cleanly → commit. On exception → rollback.

```python
async with uow:
    uow.products.add(product)
    uow.orders.add(order)
    # both committed together or neither
```

Without UoW, you'd pass sessions around everywhere, making transactions hard to reason about.

### Why QuerySpec?

A QuerySpec is a **query object** — it encapsulates a specific database query as a class.

```python
class ProductsByCategoryQuery(SQLAlchemyQuerySpec[Product]):
    def __init__(self, category: str):
        self.category = category

    def build(self):
        return sa.orm.Query(Product).filter(Product.category == self.category)
```

**Why not just write the query in the repo?**
- Queries in repos are hard to test in isolation
- Queries in repos are bound to the session at construction time — you can't reuse them across different engines (read replica, write primary, test DB)
- QuerySpecs are plain objects — no session, no side effects, easy to instantiate and inspect in tests

**The runner executes the spec against a session:**
```python
runner = AsyncSQLAlchemyQuerySpecRunner(session)
products = await runner.get_all(ProductsByCategoryQuery("electronics"))
```

### Why two definitions of the same type?

You'll see `Product` defined twice:
- `domain/entities.py` — `@dataclass`. Pure Python. No GraphQL, no SQLAlchemy.
- `application/gql/entities.py` — `@strawberry.type`. Exposed via GraphQL schema.

This is intentional. The domain doesn't know GraphQL exists. If tomorrow you add a REST API, the domain works unchanged.

---

## Exercise 1 — ORM Entities + Migration

**Goal:** Understand how SQLAlchemy's imperative mapping works and how Alembic creates tables.

### What to build

Three domain entities and their ORM mappings:

**`Product`** — `id`, `name`, `category`, `price_cents` (int), `stock` (int), `created_at`
**`Customer`** — `id`, `email`, `name`, `created_at`
**`Order`** — `id`, `customer_id`, `status` (str: `pending`/`confirmed`/`shipped`), `created_at`

### Tasks

1. Define the three `@dataclass` entities in `domain/entities.py`
2. Define the three `Table()` objects and `map_imperatively()` calls in `infrastructure/entity_mappings.py`
3. Generate and run an Alembic migration:
   ```bash
   uv run alembic revision --autogenerate -m "initial_tables"
   uv run alembic upgrade head
   ```
4. Write a test in `tests/infrastructure/test_entities.py` that:
   - Inserts a `Product` via `dbsession`
   - Commits
   - Queries it back
   - Asserts `name`, `category`, `price_cents` match

### TDD flow

Write the test first → watch it fail (entity doesn't exist) → define entity → watch it fail (no table) → write migration → watch it pass.

### Rules

- No FK constraints at DB level (use plain integer columns for `customer_id` in `Order`)
- All integer IDs: `mysql.INTEGER(unsigned=True)`, autoincrement, primary key
- All timestamps: `sa.DateTime`, `server_default=text("CURRENT_TIMESTAMP")`

### Documentation

- SQLAlchemy imperative mapping: https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#imperative-mapping
- Alembic autogenerate: https://alembic.sqlalchemy.org/en/latest/autogenerate.html
- Python dataclasses: https://docs.python.org/3/library/dataclasses.html

---

## Exercise 2 — Unit of Work

**Goal:** Understand why the UoW pattern exists and how to implement it.

### What to build

A `SqlAlchemyUnitOfWork` that:
- Holds the async session
- Exposes `products`, `customers`, `orders` repos (simple repos with `add()` and `get(id)`)
- Commits on clean exit, rolls back on exception

### Tasks

1. Define abstract interfaces in `domain/interfaces.py`:
   - `AbstractRepo[T]` with `add(*entities)` and `get(id) -> T | None`
   - `AbstractUnitOfWork` with `products`, `customers`, `orders` attributes and `__aenter__`/`__aexit__`

2. Implement `SqlAlchemyProductRepo`, `SqlAlchemyCustomerRepo`, `SqlAlchemyOrderRepo` in `infrastructure/repos/`
   - Each has `add(*entities)` (calls `session.add_all`) and `get(id)` (calls `session.get`)

3. Implement `SqlAlchemyUnitOfWork` in `infrastructure/uow.py`

4. Write a test in `tests/infrastructure/test_uow.py` that:
   - Creates a product and customer inside a `async with uow:` block
   - Verifies both are in the DB after
   - Then creates another product inside a block that raises an exception mid-way
   - Verifies that product is NOT in the DB (rollback worked)

### TDD flow

Write both tests first (they'll fail) → implement repos → implement UoW → watch them pass.

### Key question to answer as you build this

*Why does the UoW own the session instead of each repo owning it?*
Write your answer as a comment at the top of `uow.py`.

### Documentation

- Unit of Work pattern: https://www.cosmicpython.com/book/chapter_06_uow.html
- SQLAlchemy async session: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- Python context managers (`__aenter__`/`__aexit__`): https://docs.python.org/3/reference/datamodel.html#async-context-managers

---

## Exercise 3 — QuerySpecs

**Goal:** Understand why QuerySpecs exist, how to build them, and how to test them independently from the session.

### What to build

Three QuerySpecs:

1. **`ProductsByCategory(category: str)`** — returns all `Product` rows where `category == self.category`
2. **`CustomerByEmail(email: str)`** — returns a single `Customer` by email (or None)
3. **`OrdersByCustomer(customer_id: int)`** — joins `Order` filtered by `customer_id`, returns list of `Order`

And an `AsyncSQLAlchemyQuerySpecRunner` that executes them.

### Tasks

1. Read the `SQLAlchemyQuerySpec` base class API — understand `build()`, `parse_result()`, `_result_type`
2. Create `domain/queries/products_by_category.py`, `customer_by_email.py`, `orders_by_customer.py`
3. Each QuerySpec must:
   - Subclass `SQLAlchemyQuerySpec[T]`
   - Accept params in `__init__`
   - Implement `build()` returning an `sa.orm.Query`
   - NOT import or reference any session
4. Write tests in `tests/infrastructure/test_queryspecs.py`:
   - Setup: insert test data via `dbsession`
   - Exercise: create runner, call `runner.get_all()` or `runner.get_one()`
   - Assert: correct results returned

### TDD flow for each QuerySpec

Write the test → RED (QuerySpec doesn't exist) → write QuerySpec → GREEN → next.

### Key questions to answer as comments in each QuerySpec file

- *Why doesn't the QuerySpec hold a reference to the session?*
- *What would break if you wrote this query directly in the repo method?*

### Documentation

- SQLAlchemy ORM queries (legacy Query API): https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html
- SQLAlchemy joins: https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join

---

## Exercise 4 — Use Cases

**Goal:** Understand how use cases orchestrate domain logic without knowing about DB or GQL.

### What to build

Two use cases:

1. **`CreateOrder(uow)`** — given a `customer_id` and a list of `(product_id, quantity)` pairs:
   - Validates the customer exists
   - Validates each product exists and has enough stock
   - Creates the order with status `pending`
   - Deducts stock from each product
   - Returns the created order

2. **`GetCustomerOrders(runner)`** — given a `customer_id`, returns all orders for that customer using `OrdersByCustomer` QuerySpec

### Tasks

1. Create `domain/use_cases/create_order.py` and `get_customer_orders.py`
2. Use cases receive `uow` or `runner` as constructor argument — they do NOT import from infrastructure
3. Write tests in `tests/domain/test_create_order.py` and `test_get_customer_orders.py`:
   - Use `mocker.AsyncMock()` for the UoW — mock all repo calls
   - Test the happy path
   - Test each error case (customer not found, product not found, insufficient stock)
   - Assert that `uow.orders.add()` was called with the right arguments
   - Assert that stock was deducted correctly

### TDD flow

Write all tests first → all RED → implement use case step by step → each test turns GREEN.

### Key question

*`CreateOrder` modifies both `Product` (stock) and `Order`. Why is it correct that both happen inside a single `async with uow:` block?*
Write the answer as a docstring on the `execute()` method.

### Documentation

- Cosmic Python — Use cases: https://www.cosmicpython.com/book/chapter_04_service_layer.html
- pytest-mock AsyncMock: https://pytest-mock.readthedocs.io/en/latest/usage.html

---

## Exercise 5 — Strawberry GraphQL

**Goal:** Understand the two-layer type system (domain dataclass vs strawberry type) and how to wire a use case to a GraphQL query.

### What to build

Two GraphQL queries:

1. **`products(category: String!): [Product!]!`** — calls `ProductsByCategory` QuerySpec via runner
2. **`customerOrders(customerId: Int!): [Order!]!`** — calls `GetCustomerOrders` use case

### Tasks

1. Define GQL types in `application/gql/entities.py`:
   - `@strawberry.type class Product` with fields: `id`, `name`, `category`, `priceCents`, `stock`
   - `@strawberry.type class Order` with fields: `id`, `customerId`, `status`
   - Note: these are DIFFERENT classes from the domain dataclasses — same data, different layer

2. Add resolvers to `application/gql/query.py`:
   - `products(category: str) -> list[Product]` — creates runner from `info.context["session"]`, executes QuerySpec, maps results to GQL types
   - `customer_orders(customer_id: int) -> list[Order]` — calls use case

3. Write tests in `tests/application/test_queries.py`:
   - Mock the QuerySpec runner / use case
   - Call `Query().products(info=mock_info, category="electronics")` directly
   - Assert the returned GQL types have correct field values

### TDD flow

Write tests first → RED → implement GQL types → still RED → implement resolvers → GREEN.

### Key questions

- *Why do we define `Product` twice — once in domain and once in GQL?*
- *What would happen if the domain `Product` used `@strawberry.type` directly?*

Write both answers as comments at the top of `application/gql/entities.py`.

### Documentation

- Strawberry types: https://strawberry.rocks/docs/types/object-types
- Strawberry enums: https://strawberry.rocks/docs/types/enums
- Strawberry queries: https://strawberry.rocks/docs/general/queries

---

## Exercise 6 — Full End-to-End TDD

**Goal:** Put everything together. Build a feature from test to working GraphQL query using strict TDD.

### Feature to build

**`placeOrder` mutation** — a GraphQL mutation that:
1. Takes `customerId: Int!` and `items: [OrderItemInput!]!` (each item: `productId`, `quantity`)
2. Calls `CreateOrder` use case
3. Returns the created order or a typed error

### Typed errors

Define a GraphQL union return type:
```graphql
union PlaceOrderResult = Order | CustomerNotFoundError | ProductNotFoundError | InsufficientStockError
```

### TDD sequence — follow this strictly

1. Write domain test for `CreateOrder` error cases → RED → implement error handling in use case → GREEN
2. Write GQL test for `placeOrderMutation` happy path → RED → implement mutation → GREEN
3. Write GQL test for each error case → RED → implement error mapping → GREEN

### Documentation

- Strawberry mutations: https://strawberry.rocks/docs/general/mutations
- Strawberry union types: https://strawberry.rocks/docs/types/union

---

## Final Questions

Answer these in writing before moving on. They have no single correct answer — the goal is to reason through them.

1. **QuerySpec vs repo method** — You could write `session.execute(select(Product).where(Product.category == category))` directly in the repo. Why is that worse than a QuerySpec? Give two concrete reasons.

2. **UoW transaction boundary** — `CreateOrder` deducts stock AND creates an order in one `async with uow:` block. What would happen in the real world (not in tests) if you committed the stock deduction first and the order creation failed? Why does the UoW prevent this?

3. **Two type definitions** — You defined `Product` as a `@dataclass` in domain and as a `@strawberry.type` in GQL. Name one concrete scenario where having them separate saves you from a problem.

4. **`lazy="raise"`** — In the exercises you may have encountered `lazy="raise"` on relationships. What does it mean? Why is it safer than `lazy="select"` in an async context?

5. **TDD discipline** — In Exercise 6 you had to write the test before the implementation. Describe one moment where writing the test first forced you to make a better design decision than you would have made otherwise.

---

*Good luck. No LLMs, no autocomplete. Read the docs, make mistakes, understand why.*
