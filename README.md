# Store Admin Dashboard

A full-stack e-commerce administration app for managing products and orders. The project is currently intended for development and demonstration purposes and is not production-ready.

**Project status**: under active development. The products and orders backend APIs are implemented. The Angular frontend is currently in progress.

### Current Features

#### Products

- Create a product
- View all products
- View a product by ID
- Update product information
- Delete a product
- Search and filter products
- Server-side pagination

#### Orders

- Create an order with multiple products
- View all orders
- View an order by ID
- Search and filter orders
- Server-side pagination
- Update order status
- Automatic order-total calculation

### Tech Stack

- **Frontend:** Angular, TypeScript, Angular Material, RxJS
- **Backend:** Python, FastAPI, SQLAlchemy, Pydantic, Alembic
- **Database and tooling:** PostgreSQL, Docker Compose

#### Backend Architecture

```text
Router → Service → Repository → Database
