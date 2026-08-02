from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, status
from app.dependencies import OrderServiceDependency
from app.models import Order
from app.schemas import (
    OrderCreate,
    OrderFilters,
    OrderListRead,
    OrderRead,
    OrderStatusUpdate,
)
from app.services.orders import InvalidOrderError, OrderNotFoundError

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.get("", response_model=OrderListRead)
def get_orders(
    filters: Annotated[OrderFilters, Query()], order_service: OrderServiceDependency
) -> OrderListRead:
    orders, total = order_service.get_orders(filters)
    return OrderListRead(
        items=orders, total=total, page=filters.page, page_size=filters.page_size
    )


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, order_service: OrderServiceDependency) -> Order:
    try:
        return order_service.get_order(order_id)
    except OrderNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        ) from error


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate, order_service: OrderServiceDependency) -> Order:
    try:
        return order_service.create_order(order_data)
    except InvalidOrderError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
        ) from error


@router.patch("/{order_id}/status", response_model=OrderRead)
def update_order_status(
    order_id: int, status: OrderStatusUpdate, order_service: OrderServiceDependency
) -> Order:
    try:
        return order_service.update_status(order_id, status)
    except OrderNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        ) from error
