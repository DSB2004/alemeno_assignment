from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.viewsets import ViewSet
from  .serializer import RegisterCustomerDTO
from .models import Customers
class RegisterCustomerViewset(ViewSet):

    def create(self,request):

        serializer = RegisterCustomerDTO(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        
        first_name=data["first_name"]
        last_name=data["last_name"]
        age=data["age"]
        monthly_salary=data["monthly_salary"]
        phone_number=data["phone_number"]

        approved_limit = 36 * monthly_salary

        customer = Customers.objects.create(
            # customer_id=
            first_name=first_name,
            last_name=last_name,
            age=age,
            monthly_salary=monthly_salary,
            phone_number=phone_number,
            approved_limit=approved_limit,
        )
     
        return JsonResponse(data={
            "customer_id":customer.id,
            "name":first_name+" "+last_name,
            "age":age,
            "monthly_income":monthly_salary,
            "approved_limit":approved_limit,
            "phone_number":phone_number
        })