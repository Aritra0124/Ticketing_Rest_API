from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class Manager(AbstractUser):
    pass

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Adding unique constraint to the name field

    def __str__(self):
        return self.name

class Pricing(models.Model):
    source = models.ForeignKey(Location, related_name='source_pricings', on_delete=models.CASCADE)
    destination = models.ForeignKey(Location, related_name='destination_pricings', on_delete=models.CASCADE)
    pricing = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pricing from {self.source.name} to {self.destination.name}: {self.pricing}"

class Ticket(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    source = models.ForeignKey(Location, related_name='source_tickets', on_delete=models.CASCADE)
    destination = models.ForeignKey(Location, related_name='destination_tickets', on_delete=models.CASCADE)
    travel_date = models.DateField()
    passenger_name = models.CharField(max_length=255)
    pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ticket #{self.pk}'

class Travellers(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return f'Traveller {self.id} for Ticket #{self.ticket.pk}'
