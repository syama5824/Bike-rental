from django.contrib import admin
from .models import Bike,Users

admin.site.register(Bike)

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'contact', 'age', 'is_admin', 'user_role')
    search_fields = ('first_name', 'last_name', 'email', 'contact')
