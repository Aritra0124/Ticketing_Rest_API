from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Ticket, Travellers
from ..serializers import TicketOutputSerializer


class Traveller(APIView):
    def get(self, request, id):
        try:
            traveller = Travellers.objects.get(id=id)
            ticket = Ticket.objects.filter(id=traveller.ticket.id)
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