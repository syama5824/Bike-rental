from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Bike,Users,NotifyMe

class BikeUpdateForm(forms.ModelForm):
    class Meta:
        model = Bike
        fields = ['name', 'category', 'price_per_day', 'price_per_month', 'registration_number']

class UserForm(forms.ModelForm):
    interested_bikes=forms.ModelMultipleChoiceField(
        queryset=Bike.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Intrested Bikes"
    )
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'contact', 'email', 'age', 'aadhar_number', 'driving_license','interested_bikes']

class NotifyMeForm(forms.ModelForm):
    class Meta:
        model=NotifyMe
        fields=['user','bike']

class ContactForm(forms.Form):
    name=forms.CharField(label='Your Name',max_length=100)
    email=forms.EmailField(label='Your Email')
    message=forms.CharField(label='Your Message',widget=forms.Textarea)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.helper=FormHelper()
        self.helper.form_method='post'
        self.helper.add_input(Submit('submit','Submit'))

        