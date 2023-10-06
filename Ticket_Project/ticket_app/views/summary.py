from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum
from django.db.models.functions import ExtractMonth
from django.utils import timezone
from ..models import Ticket
class TicketSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start_date', '2023-01-01')
        end_date = request.query_params.get('end_date', timezone.now().strftime('%Y-%m-%d'))

        tickets = Ticket.objects.filter(travel_date__range=[start_date, end_date])

        summary_data = tickets.annotate(
            month=ExtractMonth('travel_date')
        ).values('source__name', 'month').annotate(
            ticket_count=Count('id'),
            total_pricing=Sum('pricing__pricing')
        ).order_by('source__name', 'month')

        summary = {}
        for entry in summary_data:
            location_name = entry['source__name']
            month = entry['month']
            ticket_count = entry['ticket_count']
            total_pricing = entry['total_pricing']

            month_year = timezone.datetime(2023, month, 1).strftime('%b-%Y')

            if location_name not in summary:
                summary[location_name] = {}

            summary[location_name][month_year] = {
                'ticket_count': ticket_count,
                'total_pricing': total_pricing,
            }

        return Response(summary, status=status.HTTP_200_OK)