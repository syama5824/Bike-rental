from rest_framework import viewsets
from ..models import Users
from ..serializers import UsersSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
