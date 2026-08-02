from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, status
from app.dependencies import ProductServiceDependency
from app.models import Product
from app.schemas import (
    ProductCreate,
    ProductRead,
    ProductUpdate,
    ProductFilters,
    ProductListRead,
)
from app.services.products import ProductAlreadyExistsError, ProductNotFoundError

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=ProductListRead)
def get_products(
    filters: Annotated[ProductFilters, Query()],
    product_service: ProductServiceDependency,
) -> ProductListRead:
    products, total = product_service.get_products(filters)
    return ProductListRead(
        items=products, total=total, page=filters.page, page_size=filters.page_size
    )


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate, product_service: ProductServiceDependency
) -> Product:
    try:
        return product_service.create_product(product_data)
    except ProductAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A product with this SKU already exists",
        ) from error


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, product_service: ProductServiceDependency) -> Product:
    try:
        return product_service.get_product(product_id)
    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        ) from error


@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    product_service: ProductServiceDependency,
) -> Product:
    try:
        return product_service.update_product(product_id, product_data)
    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        ) from error
    except ProductAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A product with this SKU already exists",
        ) from error


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, product_service: ProductServiceDependency) -> None:
    try:
        product_service.delete_product(product_id)
    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        ) from error
