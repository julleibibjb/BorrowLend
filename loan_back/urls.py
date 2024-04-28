# add the url paths for the views
from django.urls import path
from . import views

app_name = 'loan_back'
urlpatterns = [
    path('', views.base_view, name='base'),
    path('loan/application', views.loan_request, name='loan'),
    path("manager/dashboard/",views.manager,name="manager"),
    path("manager/requested-loans",views.RequestedLoan,name="request"),
    path("manager/approved-loans",views.ApprovedLoans,name="approved"),
    path("manager/rejected-loans",views.RejectedLoans,name="reject"),
    path("manager/users",views.usersmanagers,name="usersmanagers"),
    path("manager/users/active",views.users,name="users"),
    path("manager/users/borrowers",views.Borrowers,name="borrowers"),
    path("manager/users/staff",views.staff,name="staff"),
    path("manager/users/admin",views.superusers,name="admin"),
    path("manager/Transactions/",views.Transactions,name="Transactions"),

]
