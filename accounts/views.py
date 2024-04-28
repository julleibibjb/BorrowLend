from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from loan_back.models import Loan,loanTransaction

def sighup(request):
    if request.method=="POST":
        username=request.POST['firstname']
        lastname=request.POST['lastname']
        idnumber=request.POST['idnumber']
        email=request.POST['email']
        password=request.POST['password']
        phone=request.POST['phone']
        address=request.POST['address']
        password=request.POST['password']
        password1=request.POST['password1']


        if CustomUser.objects.filter(email=email):
            messages.error(request,"username already exist")
            return redirect("/sighup")
        
        if CustomUser.objects.filter(idnumber=idnumber):
            messages.error(request,"id number already in use")
            return redirect("/sighup")
        
        if password!=password1:
            messages.error(request,"password doesnt match")
            return redirect("/sighup")
        
        user=CustomUser.objects.create_user(username=username,lastname=lastname,email=email,idnumber=idnumber,password=password,phone=phone,address=address)
       
        
        messages.success(request, "account succesfully created" )
        return redirect("/accounts/sighin")
    return render(request,"accounts/sighup.html",{})


def sighin(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        user = authenticate(email=email, password=password)
        print("user",user)
        if user is not None:
            login(request,user)
            messages.success(request, "succesfully logged in" )
            return redirect(f"/accounts/profile/{request.user.username}")
        else:
             messages.error(request, " username or password incorrect" )
             
	   
        
    return render(request,"accounts/sighin.html",{})



def logout_request(request):
    logout(request)
    messages.success(request, "succesfully logged out" )
    return redirect("/accounts/sighin")



@login_required(login_url='/sighin')
def profile(request,user):
    if request.method=="POST":
        email=CustomUser.objects.get(email=request.POST.get("email"))
        amount=int(request.POST.get("amount"))
        id=request.POST.get("id")

        if email and amount < Loan.objects.get(id=id).loan_amount:
            req=Loan.objects.get(id=id)
            req.loan_amount=req.loan_amount-amount
            req.save()
            transaction=loanTransaction.objects.create(borrower=email,payment=amount,status="approved")
            messages.success(request,"payment successfully made")
      
    if user!=request.user.username:
        return redirect("/sighup")
    userloan=Loan.objects.filter(borrower=request.user)
    print(userloan)
    context={"loans":Loan.objects.filter(borrower=request.user)}
    return render(request,"accounts/profile.html",context)






