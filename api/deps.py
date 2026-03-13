from api.config import settings
from api.services.feature_store import FeatureStore
from api.services.model_service import ModelService
from api.services.production_service import ProductionService
from api.services.financial_service import FinancialService
from api.services.report_service import ReportService

feature_store = FeatureStore(settings.feature_data_path)
model_service = ModelService(
    model_path=settings.model_path,
    metadata_path=settings.model_metadata_path,
    feature_store=feature_store,
)
production_service = ProductionService()
financial_service = FinancialService()
report_service = ReportService()


def get_feature_store() -> FeatureStore:
    return feature_store


def get_model_service() -> ModelService:
    return model_service


def get_production_service() -> ProductionService:
    return production_service


def get_financial_service() -> FinancialService:
    return financial_service


def get_report_service() -> ReportService:
    return report_service
