from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.products import ProductRepository
from app.services.products import ProductService
from app.repositories.orders import OrderRepository
from app.services.orders import OrderService
from app.repositories.dashboard import DashboardRepository
from app.services.dashboard import DashboardService

DatabaseSession = Annotated[Session, Depends(get_db)]


def get_product_repository(db_session: DatabaseSession) -> ProductRepository:
    return ProductRepository(db_session)


ProductRepositoryDependancy = Annotated[
    ProductRepository, Depends(get_product_repository)
]


def get_product_service(repository: ProductRepositoryDependancy) -> ProductService:
    return ProductService(repository)


ProductServiceDependency = Annotated[ProductService, Depends(get_product_service)]


def get_order_repository(db_session: DatabaseSession) -> OrderRepository:
    return OrderRepository(db_session)


OrderRepositoryDependency = Annotated[OrderRepository, Depends(get_order_repository)]


def get_order_service(
    order_repository: OrderRepositoryDependency,
    product_repository: ProductRepositoryDependancy,
) -> OrderService:
    return OrderService(
        order_repository=order_repository, product_repository=product_repository
    )


OrderServiceDependency = Annotated[OrderService, Depends(get_order_service)]


def get_dashboard_repository(db_session: DatabaseSession) -> DashboardRepository:
    return DashboardRepository(db_session)


DashboardRepositoryDependency = Annotated[
    DashboardRepository, Depends(get_dashboard_repository)
]


def get_dashboard_service(
    repository: DashboardRepositoryDependency,
) -> DashboardService:
    return DashboardService(repository)


DashboardServiceDependency = Annotated[DashboardService, Depends(get_dashboard_service)]
