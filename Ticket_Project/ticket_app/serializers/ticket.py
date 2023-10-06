from rest_framework import serializers
from ..models import Pricing, Ticket
from ..serializers import LocationSerializer, PricingOutputSerializer
class TicketInputSerializer(serializers.ModelSerializer):
    pricing = PricingOutputSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ('source', 'destination', 'travel_date', 'passenger_name', 'seat_number', 'is_cancelled', 'pricing')

    def validate(self, data):
        source = data['source']
        destination = data['destination']
        travel_date = data['travel_date']
        seat_number = data['seat_number']

        existing_tickets = Ticket.objects.filter(
            source=source,
            destination=destination,
            travel_date=travel_date,
            seat_number=seat_number
        )

        if existing_tickets.exists():
            raise serializers.ValidationError(
                "Ticket with the same seat number, source, destination, and travel date already exists.")

        return data

    def create(self, validated_data):
        source = validated_data['source']
        destination = validated_data['destination']

        pricing = Pricing.objects.filter(source=source, destination=destination).first()

        if not pricing:
            raise serializers.ValidationError(
                "Pricing information not available for the provided source and destination.")

        validated_data['pricing'] = pricing

        ticket = Ticket.objects.create(**validated_data)
        return ticket

class TicketOutputSerializer(serializers.ModelSerializer):
    source = LocationSerializer()
    destination = LocationSerializer()
    pricing = PricingOutputSerializer()
    class Meta:
        model = Ticket
        fields = ('uuid','source', 'destination', 'travel_date', 'passenger_name', 'seat_number', 'is_cancelled', 'pricing')