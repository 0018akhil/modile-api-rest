from rest_framework import serializers
from .models import AppUser

class SearchByNameSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone_number = serializers.CharField()
    spam_likely_hood = serializers.DecimalField(max_digits=5, decimal_places=2)
    email = serializers.EmailField(required=False)


class SpamReportSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    report_time = serializers.DateTimeField()

class YourModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = []  # Include all fields

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Check if email field is None
        if instance.email is None:
            data['email'] = "Email is null"  # Replace with your custom message
        
        return data