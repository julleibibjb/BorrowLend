# add the url paths for the views
from django.urls import path
from . import views

app_name = 'loan_back'
urlpatterns = [
    path('sighup/', views.sighup, name='sighup'),
    path('sighin/', views.sighin, name='sighin'),
    path("logout/", views.logout_request, name= "logout"),
    path("profile/<str:user>/", views.profile, name= "profile"),
]
