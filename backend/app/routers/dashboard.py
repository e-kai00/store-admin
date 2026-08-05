from fastapi import APIRouter
from app.dependencies import DashboardServiceDependency
from app.schemas import DashboardSummaryRead

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
)


@router.get("/summary", response_model=DashboardSummaryRead)
def get_dashboard_summary(
    dashboard_service: DashboardServiceDependency,
) -> DashboardSummaryRead:
    return dashboard_service.get_summary()
