from django.contrib import admin
from .models import Loan,Notifcation,loanTransaction

admin.site.register(Loan)
admin.site.register(Notifcation)

admin.site.register(loanTransaction)


