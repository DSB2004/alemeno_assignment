from  rest_framework.viewsets import ViewSet
from django.http import JsonResponse
from  .models import Loans
from .serializer import CheckEligibilityDTO,CreateLoanDTO
from .utils import calculate_credit_score,get_interest_rate,calculate_emi
from dateutil.relativedelta import relativedelta
from django.utils import timezone
import os
from config import settings
from  .task import seed_data


class CheckEligibilityViewSet(ViewSet):

    def create(self,request):
        from apps.customers.models import Customers
        try:
            serializer = CheckEligibilityDTO(data=request.data)
            serializer.is_valid(raise_exception=True)

            data = serializer.validated_data

            customer_id=data["customer_id"]
            loan_amount=data["loan_amount"]
            interest_rate=data["interest_rate"]
            tenure=data["tenure"]

            customer=Customers.objects.get(id=customer_id)

            credit_score=calculate_credit_score(customer)

            print(credit_score)

            if(credit_score<10):
                return JsonResponse({"message": "Loan can't be approved","credit_score":credit_score}, status=200)
            

            computed_interest_rate=get_interest_rate(credit_score)

            interest_rate=max(computed_interest_rate,interest_rate)

            return JsonResponse({
                "customer_id":customer_id,
                "loan_amount":loan_amount,
                "interest_rate":interest_rate,
                "tenure":tenure
            })
        except Customers.DoesNotExist:
            return JsonResponse({
                "message":f"Customer {customer_id} not found"
            },status=404)



class CreateLoanViewSet(ViewSet):

    def create(self,request):
        from apps.customers.models import Customers
        try:
            serializer = CreateLoanDTO(data=request.data)
            serializer.is_valid(raise_exception=True)

            data = serializer.validated_data

            customer_id=data["customer_id"]
            loan_amount=data["loan_amount"]
            interest_rate=data["interest_rate"]
            tenure=data["tenure"]

            customer=Customers.objects.get(id=customer_id)

            credit_score=calculate_credit_score(customer)

            if(credit_score<10):
                return JsonResponse({"message": "Loan can't be approved","credit_score":credit_score}, status=400)
            

            computed_interest_rate=get_interest_rate(credit_score)

            if(computed_interest_rate>interest_rate):
                return JsonResponse({"message": "Interest rate is low","required":computed_interest_rate}, status=400)
            
            interest_rate=max(interest_rate,computed_interest_rate)


            monthly_installment=calculate_emi(loan_amount,interest_rate,tenure)


            approval_date = timezone.now().date()
            end_date = approval_date + relativedelta(months=tenure)


            loan=Loans.objects.create(
                customer=customer,
                loan_amount=loan_amount,
                tenure=tenure,
                monthly_payment=monthly_installment,
                interest_rate=interest_rate,
                date_of_approval = approval_date,
                end_date = end_date
                
            )


            return JsonResponse({
                "customer_id":customer_id,
                "loan_approved":True,
                "monthly_installment ":monthly_installment,
                "loan_id":loan.id,
                "message":"Loan approved"
            })
        except Customers.DoesNotExist:
            return JsonResponse({
                "message":f"Customer {customer_id} not found"
            },status=404)



class ViewLoanViewSet(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            loan = Loans.objects.get(pk=pk)
            data = {
                "loan_id": loan.id,
               "customer": {
                    "id": loan.customer.id,
                    "first_name": loan.customer.first_name,
                    "last_name": loan.customer.last_name,
                    "phone_number": loan.customer.phone_number,
                    "age":loan.customer.age,
                },
                "loan_amount":loan.loan_amount,
                "tenure": loan.tenure,
                "interest_rate": loan.interest_rate,
                "monthly_installment": loan.monthly_payment
            }
            return JsonResponse(data=data)
        except Loans.DoesNotExist:
            return JsonResponse({"error": "Loan not found"}, status=404)
        


class ViewLoansViewSet(ViewSet):

    def retrieve(self, request, pk=None):
        try:
            loans = Loans.objects.filter(customer_id=pk)
            data = []
            for loan in loans:
                data.append({
                    "loan_id": loan.id,
                    "loan_amount":loan.loan_amount,
                    "interest_rate": loan.interest_rate,
                    "monthly_installment": loan.monthly_payment,
                    "repayments_left":loan.tenure-loan.emi_paid_on_time,
                })

            return JsonResponse({"loans":data})
        except Loans.DoesNotExist:
            return JsonResponse({"error": "Loan not found"}, status=404)
        


class SeedDataViewSet(ViewSet):
    def create(self,request):
        try:
            customer_file = request.FILES.get("customers", None)
            loan_file = request.FILES.get("loans", None)

            if customer_file is None or loan_file is None:
                return JsonResponse(
                    {"message": "Both customer and loan file are required"},
                    status=400
                )


            

            upload_dir = os.path.join(settings.BASE_DIR, "uploads")
            os.makedirs(upload_dir, exist_ok=True)


            customer_path = os.path.join(upload_dir, customer_file.name)
            with open(customer_path, "wb+") as f:
                for chunk in customer_file.chunks():
                    f.write(chunk)

            loan_path = os.path.join(upload_dir, loan_file.name)
            with open(loan_path, "wb+") as f:
                for chunk in loan_file.chunks():
                    f.write(chunk)

            seed_data.delay(customer_file_path=customer_path, loan_file_path=loan_path)


            return JsonResponse(
                {
                    "message": "Files uploaded successfully",
                    "customer_file": customer_path,
                    "loan_file": loan_path,
                },
                status=202
            )

        except Exception as e:
            
            print("Error happened",e)
            return JsonResponse(
                {
                    "message": "Error happened",
                },
                status=500
            )
