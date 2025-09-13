from rest_framework import serializers


class RegisterCustomerDTO(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    age = serializers.IntegerField()
    monthly_salary = serializers.FloatField()
    phone_number = serializers.CharField(max_length=15)
    approved_limit = serializers.FloatField(read_only=True)

    
