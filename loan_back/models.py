from django.db import models
from accounts.models import CustomUser
import uuid

LOAN_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

TERM_CHOICES = (
        (12, '12 months'),
        (24,'24 months'),
        (36, '36 months'),
        (48, '48 months'),
        (72, '72 months'),
        (80, '80 months')
)
LOAN_CATEGORY_CHOICES = (
    ("pay of credit card", "pay of credit card"),
    ("Mortgage Loans", "Mortgage Loans"),
    ("Debt Consolidation Loans", "Debt Consolidation Loans"),
    ("Home improvemen", "Home improvement"),
    ("Medical expense", "Medical expense"),
    ("Travel", "Travel"),
    ("Student Loans", "Student Loans"),
    ("Other", "Other"),
)



class Loan(models.Model):
    borrower = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    loan_category=models.CharField(max_length=30, choices=LOAN_CATEGORY_CHOICES, default='Mortgage Loans')
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    request_date =  models.DateField(auto_now_add=True)
    loan_term =  models.IntegerField(choices=TERM_CHOICES,default=12)
    status = models.CharField(max_length=10, choices=LOAN_STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ('request_date', )
    

    @property
    def monthly_installment(self):
        r = (self.interest_rate / 100) / 12
        n = self.loan_term
        P = self.loan_amount
        monthly_payment = (r * P) / (1 - (1 + r) ** -n)
        return monthly_payment
    
    def __str__(self):
         return self.borrower.username


class loanTransaction(models.Model):
    borrower = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='transaction_borrower')
    transaction = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.PositiveIntegerField(default=0)
    payment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100, default='pending')

    def __str__(self):
        return self.borrower.username

  
class Notifcation(models.Model):
        user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='user_messages')
        message=models.CharField(max_length=100)
        seen=models.BooleanField(default=False)
        date=models.DateField(auto_now_add=True)

        def __str__(self):
             return self.message






