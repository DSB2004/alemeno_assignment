from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ViewLoansViewSet,ViewLoanViewSet,CheckEligibilityViewSet,CreateLoanViewSet,SeedDataViewSet


router=DefaultRouter()
router.register(r'view-loans', ViewLoansViewSet, basename='view-loans')
router.register(r'view-loan', ViewLoanViewSet, basename='view-loan')
router.register(r'create-loan', CreateLoanViewSet, basename='create-loans')
router.register(r'check-eligibility',CheckEligibilityViewSet, basename='check-eligibility')
router.register(r'seed-data',SeedDataViewSet, basename='seed-data')


urlpatterns = [
    path('', include(router.urls)),
]