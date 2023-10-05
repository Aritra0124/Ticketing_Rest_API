from datetime import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Manager, Location, Pricing, Ticket
from decimal import Decimal, DecimalException

User = get_user_model()

class ManagerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Manager.objects.create_user(**validated_data)
        return user

class ManagerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate the input data and authenticate the user.
        """
        username = data.get('username')
        password = data.get('password')

        if username and password:
            manager = authenticate(username=username, password=password)

            if manager:
                if not manager.is_active:
                    raise serializers.ValidationError("Manager account is disabled.")
                data['user'] = manager
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        return data


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name')

class PricingInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = ('source', 'destination', 'pricing')

class PricingOutputSerializer(serializers.ModelSerializer):
    source = LocationSerializer()
    destination = LocationSerializer()

    class Meta:
        model = Pricing
        fields = ('id','source', 'destination', 'pricing')

    def validate_pricing(self, value):
        try:
            decimal_value = Decimal(value)
            return decimal_value
        except DecimalException:
            raise serializers.ValidationError("Invalid pricing value. Please provide a valid decimal number.")

class TicketInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('source', 'destination', 'travel_date', 'passenger_name', 'pricing', 'seat_number', 'is_cancelled')

class TicketOutputSerializer(serializers.ModelSerializer):
    source = LocationSerializer()
    destination = LocationSerializer()
    pricing = PricingOutputSerializer()

    class Meta:
        model = Ticket
        fields = ('id','uuid', 'source', 'destination', 'travel_date', 'passenger_name', 'pricing', 'seat_number', 'is_cancelled', 'created_at')

    def create(self, validated_data):
        return Ticket.objects.create(**validated_data, created_at=timezone.now())