from django.forms import ValidationError


def validate_quantity(quantity):
    if quantity <= 0:
        raise ValidationError('Quantity must be positive number')

def validate_total_quantity(quantity, inventory):
    if quantity > inventory:
        raise ValidationError('Quantity cannot be more than inventory')