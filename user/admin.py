from django.contrib import admin
from user.models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_filter = ['updated', 'is_active']
    search_fields = ['email']
    exclude = ('password','newsletter','invited_others','username')
    

admin.site.register(User, UserAdmin)

