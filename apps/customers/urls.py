from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterCustomerViewset
router=DefaultRouter()
router.register(r'register', RegisterCustomerViewset, basename='register')


urlpatterns = [
    path('', include(router.urls)),
]