# Learning Document Template
## Instructions for the AI when creating a new exercise document

---

## Context

This folder contains a growing set of practical exercises built on top of a single standalone project:
**`ecommerce-exercises/`** — an e-commerce domain (products, orders, customers).

The project was set up in `python_architecture_exercises.md` (Part 0).
Every new exercise document assumes that setup is already done and the project already exists.

**Do not re-explain the setup. Do not re-create the project. Build on top of what exists.**

---

## Project State

The base project has:
- Python 3.12 + `uv`
- Docker + docker-compose (MySQL 8.0, app, test services)
- SQLAlchemy async (imperative mapping)
- Alembic migrations
- Strawberry GraphQL
- FastAPI
- pytest + pytest-asyncio + pytest-mock
- Hexagonal architecture: `domain/` → `infrastructure/` → `application/`
- `conftest.py` with `engine`, `dbsession` fixtures (session-scoped DB, per-test rollback)

Before creating a new document, ask:
- What entities/tables have been added by previous exercises?
- What use cases already exist?
- What QuerySpecs already exist?

If unsure, ask the user: *"Which exercises have you completed so far?"*

---

## Developer Profile

- SSr Python developer
- Comfortable with Python, intermediate level
- Light experience with async and Strawberry
- Wants to understand **why**, not just **how**
- Exercises must be done **without AI or LLMs**
- TDD is a priority — always strict red/green flow

---

## Document Structure

Every new exercise document must follow this structure:

```
# [Topic] Exercises
## [subtitle describing what's covered]

**Builds on:** [which previous document(s)]
**New concepts introduced:** [bullet list]

---

## Recap — What exists so far
[Brief summary of entities, use cases, queryspecs already built]
[Remind the developer what they can use/import]

---

## New Concepts — Read Before Exercising
[Explain the WHY of the new concepts being introduced]
[Keep it short — 1 paragraph per concept max]
[Always include: what problem it solves, what would go wrong without it]

---

## Exercise N — [Name]

### What to build
[Concrete, open-ended objective — "build X that does Y using Z"]

### Tasks
[Numbered list of specific steps]
[Each step should be actionable and verifiable]

### TDD flow
[Explicit red/green cycle for this exercise]
[Always: write test → RED → implement → GREEN]

### Key question
[One question to answer as a comment/docstring in the code]
[Should force the developer to reason about the design, not just implement]

### Documentation
[Links to official docs — one per relevant concept]

---
[Repeat for each exercise]
---

## Final Questions
[3-5 open-ended reflection questions]
[No single correct answer — goal is reasoning]
[At least one question should connect to a real-world scenario]
```

---

## Rules for writing exercises

1. **Always open-ended** — say *what* to build, not *how* to build it. No code samples in exercises.
2. **TDD is mandatory** — every exercise must have an explicit red/green flow.
3. **Key questions go in the code** — the developer writes the answer as a comment or docstring, not in the document.
4. **Build on the existing project** — new entities/use cases/queryspecs extend what was built before. Don't replace.
5. **No setup repetition** — assume the environment is already running.
6. **One new concept at a time** — don't introduce QuerySpecs and Strawberry unions in the same exercise.
7. **Documentation links are mandatory** — one link per concept introduced, always official docs.
8. **Keep the Conceptual Foundation short** — explain the WHY in plain language, not as a tutorial.

---

## What to ask the user before writing

Before generating a new document, always ask:

1. **Topic** — What concept or pattern do you want to practice?
2. **Completed exercises** — Which exercises from previous documents have you finished?
3. **Difficulty** — Do you want more guided tasks or more open-ended challenges?
4. **Any specific pain point** — Was there something from the last session you want to reinforce?

---

## Example prompt to trigger a new document

> "Crea un nuevo documento de ejercicios sobre [tema]. Ya completé los ejercicios 1 a 4 del documento anterior. Quiero practicar [aspecto específico]."

---

## File naming convention

```
[topic]_exercises.md
```

Examples:
- `python_architecture_exercises.md` — base setup + ORM + UoW + QuerySpecs + GQL
- `async_patterns_exercises.md` — async/await, concurrency, background tasks
- `testing_patterns_exercises.md` — mocking strategies, integration vs unit, fixtures
- `error_handling_exercises.md` — typed errors, GraphQL unions, exception boundaries
