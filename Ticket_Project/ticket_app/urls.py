from django.urls import path
from .views import ManagerRegistrationAPIView, ManagerLoginAPIView, ManagerLogoutAPIView, LocationListView, \
    TicketViewSet, PricingViewSet, Traveller

urlpatterns = [
    path('api/register/', ManagerRegistrationAPIView.as_view(), name='manager-registration'),
    path('api/login/', ManagerLoginAPIView.as_view(), name='manager-login'),
    path('api/logout/', ManagerLogoutAPIView.as_view(), name='manager-logout'),
    path('api/location/', LocationListView.as_view(), name='location'),
    path('api/pricing/', PricingViewSet.as_view(), name='pricing'),
    path('api/ticket/', TicketViewSet.as_view(), name='ticket'),
    path('api/ticket/<int:id>/', TicketViewSet.as_view(), name='ticket'),
    path('api/traveller/<int:id>/', Traveller.as_view(), name='traveller'),
    path('api/traveller/', Traveller.as_view(), name='traveller'),
]