from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.products import ProductRepository
from app.services.products import ProductService

DatabaseSession = Annotated[Session, Depends(get_db)]


def get_product_repository(db_session: DatabaseSession) -> ProductRepository:
    return ProductRepository(db_session)


ProductRepositoryDependancy = Annotated[
    ProductRepository, Depends(get_product_repository)
]


def get_product_service(repository: ProductRepositoryDependancy) -> ProductService:
    return ProductService(repository)


ProductServiceDependency = Annotated[ProductService, Depends(get_product_service)]
