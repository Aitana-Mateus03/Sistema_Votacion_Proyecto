# ADR-001: Adoption of Hexagonal Architecture

**Status:** Accepted  
**Date:** November 9, 2026  
**Project:** Student Voting System

## 1. Context

The Student Voting System requires a maintainable architecture that separates business logic from external technologies, databases, and user interfaces.

The project integrates external services, including Colombian open data APIs, uses DuckDB for analytical queries, and provides API endpoints for application functionality.

The main bounded contexts identified in the system are:

- **Student and Academic Management:** Handles student information and academic relationships.
- **Candidate Management:** Handles the registration and consultation of election candidates.
- **Voting Management:** Represents the election and voting processes.
- **External Data and Analytics:** Integrates external data sources, processes information, and generates analytical results.

Without clear separation between these responsibilities, changes in infrastructure could directly affect the business logic.

## 2. Decision

We decided to adopt **Hexagonal Architecture (Ports and Adapters)**.

The project is organized into four main layers:

- **Domain:** Contains the core business models and rules.
- **Application:** Coordinates application services and use cases.
- **Infrastructure:** Implements external integrations, database access, and technical services.
- **API:** Exposes application functionality through HTTP endpoints.

Dependencies are organized so that the core business logic does not depend directly on external technologies.

Dependency Injection is used to provide required components to application services and facilitate testing.

External API integrations are handled through infrastructure components, including retry mechanisms and Circuit Breaker patterns.

DuckDB is used to process data and execute analytical queries independently of the main application logic.

## 3. Consequences

### Positive consequences

- Business logic is separated from infrastructure concerns.
- External services can be replaced with fewer changes to the application.
- Components can be tested independently using mocks and controlled dependencies.
- The architecture improves maintainability and supports future growth.
- External API failures can be managed using retry and Circuit Breaker mechanisms.

### Negative consequences

- The architecture requires more folders, interfaces, and components.
- Developers must understand dependency direction and separation of responsibilities.
- Initial implementation takes more time than a monolithic structure.

## 4. Alternatives Considered

**Monolithic Architecture:** Rejected because it could increase coupling between business logic, database access, and external services.

**Traditional Layered Architecture:** Considered, but Hexagonal Architecture provides a clearer separation between the application core and external adapters.

## 5. Conclusion

Hexagonal Architecture was selected because it provides a maintainable and testable structure for the Student Voting System. It supports the integration of external APIs, analytical processing, and future application improvements while keeping the core logic independent of infrastructure technologies.