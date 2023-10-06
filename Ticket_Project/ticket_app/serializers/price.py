from rest_framework import serializers
from ..models import Pricing, Location
from decimal import Decimal, DecimalException
from ..serializers import LocationSerializer


class PricingInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = ('source', 'destination', 'pricing')

    def create(self, validated_data):
        source = validated_data['source']
        destination = validated_data['destination']
        pricing = validated_data['pricing']

        if source != destination:
            try:
                source_location = Location.objects.get(id=source.id)
                destination_location = Location.objects.get(id=destination.id)

                existing_pricing = Pricing.objects.filter(
                    source=source_location,
                    destination=destination_location,
                    pricing=pricing
                ).first()

                if existing_pricing:
                    raise serializers.ValidationError("Pricing with the same source, destination, and price already exists.")
                else:
                    new_pricing = Pricing.objects.create(source=source_location, destination=destination_location, pricing=pricing)
                    return new_pricing

            except Location.DoesNotExist:
                raise serializers.ValidationError("Invalid source or destination location names.")
        else:
            raise serializers.ValidationError("Source and destination locations cannot be the same.")
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


