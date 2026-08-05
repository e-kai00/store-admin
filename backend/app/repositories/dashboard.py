from decimal import Decimal
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models import Order, Product

OPEN_ORDER_STATUSES = (
    "pending",
    "processing",
    "shipped",
)


class DashboardRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_order_metrics(self) -> tuple[int, Decimal, int, int]:
        statement = select(
            func.count(Order.id).label("total_orders"),
            func.coalesce(
                func.sum(Order.total).filter(Order.status == "delivered"),
                Decimal("0.00"),
            ).label("total_revenue"),
            func.count(Order.id)
            .filter(Order.status.in_(OPEN_ORDER_STATUSES))
            .label("open_orders"),
            func.count(Order.id)
            .filter(Order.status == "delivered")
            .label("completed_orders"),
        )
        result = self.db_session.execute(statement).one()
        return (
            result.total_orders,
            result.total_revenue,
            result.open_orders,
            result.completed_orders,
        )

    def get_low_stock_products(self) -> list[Product]:
        statement = (
            select(Product)
            .where(Product.stock_quantity <= 5)
            .order_by(Product.stock_quantity, Product.name)
            .limit(5)
        )
        return list(self.db_session.scalars(statement).all())
