from .models import Bike

def update_bike_availability(bike_name, is_available):
    try:
        bike = Bike.objects.get(name=bike_name)
        bike.is_available = is_available
        bike.save()
        return True, f"Bike availability updated: {bike.name} is {'available' if is_available else 'not available'}"
    except Bike.DoesNotExist:
        return False, f"Bike with ID {bike_name} does not exist"

otpValidation = {}