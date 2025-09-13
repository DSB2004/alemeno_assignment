from rest_framework import serializers


class CheckEligibilityDTO(serializers.Serializer):
    customer_id= serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure= serializers.IntegerField()

    

class CreateLoanDTO(serializers.Serializer):
    customer_id= serializers.IntegerField()
    loan_amount = serializers.FloatField()
    interest_rate = serializers.FloatField()
    tenure= serializers.IntegerField()

    