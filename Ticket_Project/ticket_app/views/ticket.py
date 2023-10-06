from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Ticket
from ..serializers import TicketInputSerializer, TicketOutputSerializer

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
        try:
            ticket = Ticket.objects.get(id=id)
        except Ticket.DoesNotExist:
            return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        if ticket.is_cancelled:
            return Response({'error': 'Cancelled ticket cannot be modified'}, status=status.HTTP_400_BAD_REQUEST)

        ticket.is_cancelled = True
        ticket.save()
        serializer = TicketOutputSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TicketFilterViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketOutputSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['source__name', 'destination__name', 'travel_date', 'passenger_name']
    ordering_fields = ['travel_date']

    def get_queryset(self):
        queryset = super().get_queryset()

        source_name = self.request.query_params.get('source_name')
        destination_name = self.request.query_params.get('destination_name')
        travel_date = self.request.query_params.get('travel_date')
        passenger_name = self.request.query_params.get('passenger_name')

        if source_name:
            queryset = queryset.filter(source__name=source_name)
        if destination_name:
            queryset = queryset.filter(destination__name=destination_name)
        if travel_date:
            queryset = queryset.filter(travel_date=travel_date)
        if passenger_name:
            queryset = queryset.filter(passenger_name=passenger_name)

        return queryset
