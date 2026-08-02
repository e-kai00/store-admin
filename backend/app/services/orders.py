from decimal import Decimal
from uuid import uuid4

from app.models import Order, OrderItem
from app.repositories.orders import OrderRepository
from app.repositories.products import ProductRepository
from app.schemas import (
    OrderCreate,
    OrderFilters,
    OrderStatusUpdate,
)


class OrderNotFoundError(Exception):
    pass


class InvalidOrderError(Exception):
    pass


class OrderService:
    def __init__(
        self, order_repository: OrderRepository, product_repository: ProductRepository
    ):
        self.order_repository = order_repository
        self.product_repository = product_repository

    def get_orders(self, filters: OrderFilters) -> tuple[list[Order], int]:
        offset = (filters.page - 1) * filters.page_size
        search = filters.search.strip() if filters.search else None
        return self.order_repository.get_all(
            search=search, status=filters.status, offset=offset, limit=filters.page_size
        )

    def get_order(self, order_id: int) -> Order:
        order = self.order_repository.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError
        return order

    def create_order(self, order_data: OrderCreate) -> Order:
        # check for duplicate products in Order
        product_ids = [item.product_id for item in order_data.items]
        if len(product_ids) != len(set(product_ids)):
            raise InvalidOrderError("The same product cannot appear more than once")

        order_items: list[OrderItem] = []
        order_total = Decimal("0.00")

        for item in order_data.items:
            product = self.product_repository.get_by_id(item.product_id)
            if product is None:
                raise InvalidOrderError(f"Product {item.product_id} does not exist")
            line_total = product.price * item.quantity
            order_items.append(
                OrderItem(
                    product_id=product.id,
                    product_name=product.name,
                    quantity=item.quantity,
                    unit_price=product.price,
                    line_total=line_total,
                )
            )
            order_total += line_total

        order = Order(
            order_number=self._generate_order_number(),
            customer_name=order_data.customer_name,
            customer_email=order_data.customer_email,
            status="pending",
            total=order_total,
            items=order_items,
        )
        return self.order_repository.add(order)

    def update_status(self, order_id: int, status_data: OrderStatusUpdate) -> Order:
        order = self.order_repository.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError
        order.status = status_data.status
        return self.order_repository.save(order)

    @staticmethod
    def _generate_order_number() -> str:
        identifier = uuid4().hex[:10].upper()
        return f"ORD-{identifier}"
