# Documentation Index

This documentation separates the canonical portfolio application, stable
Arcade routes, deterministic local tooling, generated ChatHub output, and the
archived legacy site.

## Repository

- [Public overview and local commands](../README.md)
- [Architecture](ARCHITECTURE.md)
- [Contributing](../CONTRIBUTING.md)
- [Security policy](../SECURITY.md)
- [Visual identity](visual-identity.md)

## Application Surfaces

- [Arcade wing](ARCADE.md)
- [Tooling](TOOLING.md)
- [Development lanes for small models](DEVELOPMENT_FOR_SMALL_MODELS.md)
- [ChatHub Harness](../ChatHub-Harness/README.md)

## Operating State

The root `memory.md` records durable repository decisions. `.agent/` provides a
bounded operational workspace for goals, workflow state, feedback, and change
history. Generated application builds, run packets, browser profiles, and local
automation state remain outside the documentation source of truth.
