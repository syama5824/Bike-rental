from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class Bike(models.Model):
    CATEGORY_CHOICES=[
        ('scooty', _('Scooty')),
        ('gear-bike', _('Gear Bike')),
        ('ev', _('EV')),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    registration_number = models.CharField(max_length=20)
    imagefile = models.CharField(max_length=100, blank=True, null=True)
    purchase_date=models.CharField(max_length=100,blank=True,null=True)
    model_name = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(default=False)
    color = models.CharField(max_length=100, blank=True, null=True)
    brand_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    kilometers_driven = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def slug(self):
        return slugify(self.name)
    
    def __str__(self):
        return self.name
    
    class Meta:
        app_label='bikes'
    
class Rental(models.Model):
    bike = models.ForeignKey(Bike, related_name='rentals', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Rental for {self.bike.name} from {self.start_date} to {self.end_date}"

class Users(models.Model):
    user_choices = [
        ('admin', 'Admin'),
        ('host', 'Host'),
        ('user', 'User')
    ]
    
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Phone number must be exactly 10 digits.'
            )
        ]
    )
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)  # Set a default value
    user_role = models.CharField(max_length=100, choices=user_choices, default='user')
    age = models.IntegerField()
    aadhar_number = models.CharField(
        max_length=14,
        validators=[
            RegexValidator(
                regex=r'^\d{4}\s\d{4}\s\d{4}$',
                message='Aadhar number must be exactly 12 digits.'
            )
        ]
    )
    driving_license = models.CharField(
        max_length=20, unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{2}\d{2}\s\d{11}$',
                message='Enter a valid driving license number in the format "TS01 987654321098".'
            )
        ]
    )
    interested_bikes = models.ManyToManyField(Bike, related_name='interested_users')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class NotifyMe(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE)
    bike=models.ForeignKey(Bike,on_delete=models.CASCADE)
    notified=models.BooleanField(default=False)

    def __str__(self):
        return f"Notify {self.user} about {self.bike}"
