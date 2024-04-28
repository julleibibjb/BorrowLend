from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,UserManager,BaseUserManager 
from django.utils.translation import gettext_lazy 
from django.utils import timezone

class custom_account_manager(UserManager):

    def create_superuser(self,email,username,lastname,idnumber,password,**other_fields):

        other_fields.setdefault("is_staff",True)
        other_fields.setdefault("is_superuser",True)
        other_fields.setdefault("is_active",True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('super user must be assighned to is_staff=True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('super user must be assighned to is_superuser=True')
        
        if not email:
            raise ValueError(gettext_lazy("you must provide a value error"))
        email=self.normalize_email(email)
        user=self.model(email=email,username=username,idnumber=idnumber,lastname=lastname,**other_fields)
        user.set_password(password)
        user.save()


    
    def create_user(self,email,username,lastname,idnumber,password,**other_fields):

        other_fields.setdefault("is_active",True)

        if not email:
            raise ValueError(gettext_lazy("you must provide a value error"))
        email=self.normalize_email(email)
        user=self.model(email=email,username=username,idnumber=idnumber,lastname=lastname,**other_fields)
        user.set_password(password)
        user.save()


class CustomUser(AbstractBaseUser, PermissionsMixin):
    idnumber=models.PositiveIntegerField(unique=True)
    email=models.EmailField(gettext_lazy("email addres"), unique=True)
    username=models.CharField(max_length=200,unique=True)
    lastname=models.CharField(max_length=200,blank=True)
    phone=models.CharField(max_length=200,unique=True,blank=True)
    address=models.CharField(max_length=200,blank=True)
    created_at=models.DateField(default=timezone.now)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    avatar=models.ImageField(upload_to="images",blank=True)

    objects=custom_account_manager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','lastname',"idnumber"]

    def __str_(self):
        return self.username

