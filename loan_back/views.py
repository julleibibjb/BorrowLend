from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Loan,Notifcation,loanTransaction
from .decoratos import staff_member_required
from accounts.models import CustomUser
from django.db.models import Sum
# Create your views here.
# create views from the models created
from django.http import HttpResponse
from django.shortcuts import render

#create a view for base template
def base_view(request):

    notifcation=Notifcation.objects.filter(user=1)
    context={"notifcation":notifcation,"num":notifcation.count()}
    if request.user.is_anonymous:
        return render(request, 'loan_back/test.html',context)
    return render(request, 'loan_back/home.html',context)


@login_required(login_url="/accounts/sighin")
def loan_request(request):
    options = {12:6.99,36:7.59,48:7.99,60:8.28,72:9.67,84:10.45}      
   
    if request.method=="POST":
        borrower=request.user
        loan_category=request.POST.get("category")
        loan_amount=request.POST.get("amount")
        loan_term =request.POST.get("term")
        interest_rate = options.get(int(loan_term))
        

        if(loan_amount and loan_category and loan_term and interest_rate and borrower):
            loanrequest=Loan.objects.create(borrower=borrower,loan_category=loan_category,loan_amount=loan_amount,loan_term=loan_term,interest_rate=interest_rate)
            if(loanrequest):
                messages.info(request,"loan request has been sent pending approval")
                return redirect(f"/accounts/profile/{request.user.username}")
            
    return render(request,"loan_back/loan.html")


def Transactions(request):
    context={"loanrequest":loanTransaction.objects.all()}
    return render(request,"loan_back/transaction.html",context)


@staff_member_required
def manager(request):
    totalusers=CustomUser.objects.all().count()
    totalborrowers=Loan.objects.all().count()
    approvedloans=Loan.objects.filter(status="approved").count()
    rejectedloans=Loan.objects.filter(status="rejected").count()
    requestedloans=Loan.objects.all().count()
    totalapprovedamount=Loan.objects.filter(status="approved").aggregate(Sum('loan_amount')).get("loan_amount__sum")
    totalpayableamount=Loan.objects.aggregate(Sum('loan_amount')).get("loan_amount__sum")

    context={
        "users":totalusers,
        "totalborrowers":totalborrowers,
        "approvedloans":approvedloans,
        "rejectedloans":rejectedloans,
        "requestedloans":requestedloans,
        "total":totalapprovedamount,
        "payable":totalpayableamount,
    }
    return render(request,"loan_back/dashboard.html",context)



@staff_member_required
def RequestedLoan(request):
    if request.method=="POST":
        if "id-approve" in request.POST:
            id=request.POST.get("id-approve")
            req=Loan.objects.get(id=id)
            req.status="approved"
            req.save()
            message=Notifcation.objects.create(user=request.user,message="loan request has been approved")
        elif "id-reject" in request.POST:
            id=request.POST.get("id-reject")
            req=Loan.objects.get(id=id)
            req.status="rejected"
            req.save()
            message=Notifcation.objects.create(user=request.user,message="loan request has been rejected")

    
    loanrequest=Loan.objects.filter(status="pending")
    return render(request,"loan_back/request.html",{"loanrequest":loanrequest})



@staff_member_required
def ApprovedLoans(request):
    loanrequest=Loan.objects.filter(status="approved")
    print(loanrequest)
    return render(request,"loan_back/approved.html",{"loanrequest":loanrequest})



@staff_member_required
def RejectedLoans(request):
    loanrequest=Loan.objects.filter(status="rejected")
    return render(request,"loan_back/rejected.html",{"loanrequest":loanrequest})

@staff_member_required
def usersmanagers(request):
    return render(request,"loan_back/users.html",{})

@staff_member_required
def users(request):
    context={
        "Users":CustomUser.objects.all(),
        "type":"active users"
    }
    return render(request,"loan_back/usermanager.html",context)

@staff_member_required
def Borrowers(request):
    context={
        "Users":CustomUser.objects.filter(),
        "type":"active Borrowers"
    }
    return render(request,"loan_back/usermanager.html",context)

@staff_member_required
def staff(request):
    context={
        "Users":CustomUser.objects.filter(is_staff=True),
        "type":"active staff"
    }
    return render(request,"loan_back/usermanager.html",context)

@staff_member_required
def superusers(request):
    context={
        "Users":CustomUser.objects.filter(is_superuser=True),
        "type":"active admin users"

    }
    return render(request,"loan_back/usermanager.html",context)