from django.db import models

class Customers(models.Model):
    first_name = models.CharField(max_length=100, default="")  
    last_name = models.CharField(max_length=100, default="")  
    phone_number = models.CharField(max_length=10, default="")  
    monthly_salary = models.FloatField(default=0.0)
    approved_limit = models.FloatField(default=0.0)
    current_debt = models.FloatField(default=0.0)
    age=models.IntegerField(default=0)
    def __str__(self):
        return f"{self.id} {self.first_name}"

