from app.repositories.dashboard import DashboardRepository
from app.schemas import DashboardSummaryRead


class DashboardService:
    def __init__(self, repository: DashboardRepository):
        self.repository = repository

    def get_summary(self) -> DashboardSummaryRead:
        (
            total_orders,
            total_revenue,
            open_orders,
            completed_orders,
        ) = self.repository.get_order_metrics()

        low_stock_products = self.repository.get_low_stock_products()

        return DashboardSummaryRead(
            total_orders=total_orders,
            total_revenue=total_revenue,
            open_orders=open_orders,
            completed_orders=completed_orders,
            low_stock_products=low_stock_products,
        )
