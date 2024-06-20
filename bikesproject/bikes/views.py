import os
import json
import logging
import requests
import random
from django import forms
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView,FormView
from django.views import View
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView,CreateView,UpdateView
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.core.cache import cache
from django.urls import reverse_lazy
from bikes.models import Bike,Users,NotifyMe
from django.http import JsonResponse,HttpResponse
from django.conf import settings
from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client
from datetime import datetime,timedelta
from .serializers import UsersSerializer
from .forms import UserForm,NotifyMeForm,ContactForm
from .utils import otpValidation

class BikeForm(forms.ModelForm):
    class Meta:
        model=Bike
        fields=['category']

    def clean_category(self):
        category=self.cleaned_data.get('category')
        valid_categories=[choice[0] for choice in Bike.CATEGORY_CHOICES]
        if category not in valid_categories:
            raise forms.ValidationError(f"Inavlid category: {category}")
        return category

def home(request):
    categories = ['Scooty', 'Gear Bike', 'EV']
    bikes_by_category = {}

    all_bikes = Bike.objects.all()
    paginator_all = Paginator(all_bikes, 4)
    page_number_all = request.GET.get('all_page')
    page_obj_all = paginator_all.get_page(page_number_all)
    bikes_by_category['all'] = page_obj_all

    for category in categories:
        category_bikes = all_bikes.filter(category=category)
        paginator = Paginator(category_bikes, 4)
        page_number = request.GET.get(f'{category.lower()}_page')
        page_obj = paginator.get_page(page_number)
        bikes_by_category[category] = page_obj

    context = {
        'bikes_by_category': bikes_by_category
    }
    return render(request, 'bikes/home.html', context)

logger=logging.getLogger('django')

class AllBikesView(ListView):
    model = Bike
    template_name = 'bikes/all_bikes.html'
    context_object_name = 'bikes'
    paginate_by=4


    def get_queryset(self):
        # bikes=Bike.objects.all()
        # logger.debug(f"Number of bikes fetched : {bikes.count()}")
        # return bikes
        return Bike.objects.order_by('id')

    # def render_to_response(self, context, **response_kwargs):
    #     queryset = self.get_queryset()
    #     data = serialize('json', queryset)
    #     json_data=json.loads(data)
    #     response_data={
    #         "status":"ok",
    #         "data":json_data
    #     } # status key for json data
    #     pretty_data = json.dumps(response_data, indent=4)
    #     print(pretty_data) # print pretty data in terminal
    #     return super().render_to_response(context, **response_kwargs)
    
class CategoryView(ListView):
    model = Bike
    template_name = 'bikes/all_bikes.html'
    context_object_name = 'bikes'

    def get_queryset(self):
        category_name = self.kwargs.get('category')
        category = category_name.lower()
        queryset = Bike.objects.filter(category__iexact=category)
        return queryset

    def render_to_response(self, context, **response_kwargs):
        queryset = self.get_queryset()
        data = serialize('json', queryset)
        json_data=json.loads(data)
        response_data={
            "status":"ok",
            "data":json_data
        } # status key for json data
        pretty_data = json.dumps(response_data, indent=4)
        print(pretty_data) # print pretty data in terminal
        return super().render_to_response(context, **response_kwargs)
    
class BikeDetailView(DetailView):
    model = Bike
    template_name = 'bikes/bike_detail.html'
    context_object_name = 'bike'

    def get_object(self):
        category = self.kwargs.get('category').lower()
        bike_name_slug = self.kwargs.get('bike_name')
        bike_name=bike_name_slug.replace('-',' ').title()
        print(f"Querying for Category: {category}, Bike Name: {bike_name}")
        bike = get_object_or_404(Bike, category=category, name=bike_name)
        print(f"Retrieved Bike: {bike}")
        return bike
    def render_to_respone(self,context,**response_kwargs):
        bike=self.get_object()
        serializes_data=serialize('json',[bike],indent=4)
        print(serializes_data)
        return super().render_to_response(context, **response_kwargs)

class BikeListView(ListView):
    model=Bike
    template_name='bikes/home.html'#<app>/<model>_<viewtype>.html
    context_object_name='bikes'
    ordering=['-price_per_month']
        
class UserFormView(FormView):
    template_name = 'bikes/contact_form.html'
    form_class = UserForm
    success_url = reverse_lazy('success')  # URL to redirect after form submission

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get(f'{self.request.scheme}://{self.request.get_host()}/bikes/api/categories/')
        if response.status_code == 200:
            context['categories'] = response.json()
        return context

def bikes_by_category(request):
    scooties = Bike.objects.filter(category='scooty').values_list('name', flat=True)
    evs = Bike.objects.filter(category='ev').values_list('name', flat=True)
    gear_bikes = Bike.objects.filter(category='gear-bike').values_list('name', flat=True)

    data = {
        'scooties': list(scooties),
        'evs': list(evs),
        'gear_bikes': list(gear_bikes)
    }
    return JsonResponse(data)

def scooty(request):
    scooties = Bike.objects.filter(category='scooty').values_list('name', flat=True)
    data = {
        'scooties': list(scooties),
    }
    return JsonResponse(data)

def ev(request):
    evs = Bike.objects.filter(category='ev').values_list('name', flat=True)   
    data = {
        'evs': list(evs),
    }
    return JsonResponse(data)

def gear_bike(request):
    gear_bikes = Bike.objects.filter(category='gear-bike').values_list('name', flat=True)
    data = {
        'gear_bikes': list(gear_bikes)
    }
    return JsonResponse(data)

def all_bikes(request):
    all_bikes = Bike.objects.values_list('name', flat=True)
    bike_names = list(all_bikes)
    data = {
        'all_bikes': bike_names
    }
    return JsonResponse(data)
# >>> request = RequestFactory().get('/all_bikes/')
# >>> response = all_bikes(request)
# >>> print(response.content.decode('utf-8'))


def generateOTP():
    return random.randint(100000, 999999)

class sendOtp(APIView):
    def post(self, request):
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)
        
        number = request.data['number']
        print(number)
        otp = generateOTP()
        print(otp)

        message = client.messages.create(
            from_='+16066293062',
            body=f'Your OTP for login is: {otp}',
            to=number
        )

        expiry_time = datetime.now() + timedelta(minutes=2)
        otpValidation.update({number: {"otp": otp, "expiry_time": expiry_time}})
        print(otpValidation)

        if message.sid:
            return Response({"success": True, "otp": otp}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class otpVerification(APIView):
    def post(self, request):
        entered_otp = request.data['otp']
        number = request.data['number']
        user_data = otpValidation.get(number)

        if user_data:
            given_otp = user_data.get("otp")
            expiry_time = user_data.get("expiry_time")

            print(f"Entered OTP: {entered_otp}")
            print(f"Stored OTP: {given_otp}")
            print(f"Expiry Time: {expiry_time}")
            print(f"Current Time: {datetime.now()}")

            if str(given_otp) == str(entered_otp):
                if datetime.now() <= expiry_time:
                    # OTP is correct and within expiry time
                    return Response({"success": True, "message": "OTP verified successfully."}, status=status.HTTP_200_OK)
                else:
                    # OTP is correct but has expired
                    new_otp = generateOTP()
                    otpValidation.update({number: {"otp": new_otp, "expiry_time": datetime.now() + timedelta(minutes=2)}})
                    self.send_new_otp(number, new_otp)
                    return Response({"success": False, "message": "OTP expired. A new OTP has been sent."}, status=status.HTTP_200_OK)
            else:
                if datetime.now() <= expiry_time:
                    # OTP is incorrect but within expiry time
                    return Response({"success": False, "message": "Incorrect OTP. Please try again."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # OTP is incorrect and has expired
                    new_otp = generateOTP()
                    otpValidation.update({number: {"otp": new_otp, "expiry_time": datetime.now() + timedelta(minutes=2)}})
                    self.send_new_otp(number, new_otp)
                    return Response({"success": False, "message": "Incorrect OTP and it has expired. A new OTP has been sent."}, status=status.HTTP_200_OK)
        else:
            print(f"No user data found for number: {number}")
            return Response({"success": False, "message": "Invalid number or OTP not sent."}, status=status.HTTP_400_BAD_REQUEST)
    
    def send_new_otp(self, number, otp):
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_='+16066293062',
            body=f'Your new OTP for login is: {otp}',
            to=number
        )

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        # if form.is_valid():
        #     pass
    else:
        form = ContactForm()
    
    return render(request, 'bikes/contact_form.html', {'form': form})