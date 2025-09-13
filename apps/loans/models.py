from django.db import models

class Loans(models.Model):
    customer=models.ForeignKey(
        "customers.Customers",            
        on_delete=models.CASCADE,  
        related_name="loans" 
    )
    loan_amount=models.FloatField(default=0)
    tenure = models.IntegerField()  
    interest_rate = models.FloatField()  
    monthly_payment = models.FloatField()  
    emi_paid_on_time= models.IntegerField(default=0)
    date_of_approval = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def __str__(self):
        return f"{self.id} {self.customer}"
