from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class custom_user_admin_config(UserAdmin):
    search_fields=('email','username','lastname')
    list_filter=('email','username','lastname',"phone","address",'is_active','is_superuser')

    ordering=['-created_at']
    list_display=['email','username','lastname',"idnumber","phone","address",'is_active','is_superuser']

    fieldsets=(
        (None,{"fields":('email','username','lastname',)}),
        ('permission',{"fields":("is_staff",'is_active','is_superuser')}),
        ('personal',{"fields":("idnumber","phone","address",)}),
        
    )
    add_fieldsets = (
        (None,{
            'classes':("wide",),
            'fields':('email','username','lastname',"idnumber","phone","address",'password1','password2','is_active','is_staff','is_superuser')
        }),
    )
   
 

admin.site.register(CustomUser,custom_user_admin_config)
