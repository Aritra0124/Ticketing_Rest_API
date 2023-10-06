from django.urls import path, include
from .views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tickets', TicketFilterViewSet, basename='ticket')

urlpatterns = [
    path('api/register/', ManagerRegistrationAPIView.as_view(), name='manager-registration'),
    path('api/login/', ManagerLoginAPIView.as_view(), name='manager-login'),
    path('api/logout/', ManagerLogoutAPIView.as_view(), name='manager-logout'),
    path('api/location/', LocationListView.as_view(), name='location'),
    path('api/pricing/', PricingViewSet.as_view(), name='pricing'),
    path('api/ticket/', TicketViewSet.as_view(), name='ticket-list-create'),
    path('api/ticket/<int:id>/', TicketViewSet.as_view(), name='ticket-detail'),
    path('api/', include(router.urls)),
    path('api/ticket-summary/', TicketSummaryAPIView.as_view(), name='ticket-summary'),
    path('api/traveller/<int:id>/', Traveller.as_view(), name='traveller'),
    path('api/traveller/', Traveller.as_view(), name='traveller'),
    path('', index, name='index'),
]