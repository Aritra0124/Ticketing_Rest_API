from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from ..models import Manager

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
