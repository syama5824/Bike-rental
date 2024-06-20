from django.urls import path,include
from django.views.generic import TemplateView
from .views import (
    CategoryView,
    AllBikesView,
    BikeDetailView,
    bikes_by_category,
    scooty,
    ev,
    gear_bike,
    sendOtp,
    otpVerification,
    contact_view
)
from rest_framework.routers import DefaultRouter
from .api.viewsets import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('all/', AllBikesView.as_view(), name='all-bikes'),
    path('api/categories/', bikes_by_category, name='bikes-by-category'),
    path('api/scooty/',scooty, name='scooty'),
    path('api/ev/', ev, name='ev'),
    path('api/gear-bike/', gear_bike, name='gear-bike'),
    path('success/', TemplateView.as_view(template_name="bikes/success.html"), name='success'),
    path('otpgen/',sendOtp.as_view(),name='otp-generations'),
    path('contact/',contact_view,name='contact'),
    path('verifyotp/',otpVerification.as_view(),name='verifyotp'),
    path('<str:category>/', CategoryView.as_view(), name='category-bikes'),
    path('<str:category>/<slug:bike_name>/', BikeDetailView.as_view(), name='bike-detail'),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
