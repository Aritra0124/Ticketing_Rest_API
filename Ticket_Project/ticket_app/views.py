from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .models import Location, Pricing, Ticket, Travellers
from .serializers import ManagerRegistrationSerializer, ManagerLoginSerializer, LocationSerializer, \
    TicketOutputSerializer, TicketInputSerializer, PricingInputSerializer, PricingOutputSerializer


class ManagerRegistrationAPIView(APIView):
    def post(self, request):
        serializer = ManagerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ManagerLoginAPIView(APIView):
    def post(self, request):
        serializer = ManagerLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class ManagerLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Simply delete the token to force a logout for the user
        request.auth.delete()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

class LocationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        locations = Pricing.objects.all()
        serializer = PricingOutputSerializer(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PricingInputSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PricingViewSet(APIView):
    def get(self, request):
        prices = Pricing.objects.all()
        serializer = PricingOutputSerializer(prices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PricingInputSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = Ticket.objects.all()
        serializer = TicketOutputSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TicketInputSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        print("Received ticket id:", id)  # Debugging line, print the received ticket id
        try:
            ticket = Ticket.objects.get(id=id)
            print("Found ticket:", ticket)  # Debugging line, print the ticket object
        except Ticket.DoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        # If the ticket is already cancelled, prevent further modifications
        if ticket.is_cancelled:
            return Response({'error': 'Cancelled ticket cannot be modified'}, status=status.HTTP_400_BAD_REQUEST)

        # Update only the is_cancelled field
        ticket.is_cancelled = True
        ticket.save()
        serializer = TicketOutputSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Traveller(APIView):
    def get(self, request, id):
        try:
            traveller = Travellers.objects.get(id=id)
            ticket = Ticket.objects.filter(id=traveller.ticket.id)
            print("Found ticket:", ticket)  # Debugging line, print the ticket object
            serializer = TicketOutputSerializer(ticket, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        ticket_id = request.data.get('ticket')
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            traveller = Travellers.objects.create(ticket=ticket)
            serializer = TicketOutputSerializer(ticket)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Ticket.DoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)