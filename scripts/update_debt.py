import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.loans.models import Loan
from apps.customers.models import Customers


def update_customer_debt():
    customers = Customers.objects.all()

    for customer in customers:
        loans = Loan.objects.filter(customer=customer)

        total_debt = 0
        for loan in loans:
            remaining_emis = max(loan.tenure - loan.emi_paid_on_time, 0)
            remaining_amount = remaining_emis * loan.monthly_payment
            total_debt += remaining_amount

        customer.current_debt = total_debt
        customer.save()

        print(f"Updated Customer {customer.id} → Current Debt = {customer.current_debt}")

    print("All customer debts updated successfully")


if __name__ == "__main__":
    update_customer_debt()
