from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Signup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    MobileNumber = models.CharField(max_length=15, null=True)
    RegDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name
class predict(models.Model):
    open=models.CharField(max_length=10)
    high=models.CharField(max_length=10)
    low=models.CharField(max_length=10)
    close=models.CharField(max_length=10)
    wap=models.CharField(max_length=10)
    no_of_shares=models.CharField(max_length=10)
    no_of_trades=models.CharField(max_length=10)
    deli_qty=models.CharField(max_length=10)
    traded_qty=models.CharField(max_length=10)
    spread_hl=models.CharField(max_length=10)
    spread_co=models.CharField(max_length=10) 
    
class Application(models.Model):
    signup = models.ForeignKey(Signup, on_delete=models.CASCADE)
    ApplicationNumber = models.IntegerField(null=True)
    PanNumber = models.CharField(max_length=50, null=True)
    PanCardCopy = models.FileField(max_length=200, null=True)
    Address = models.CharField(max_length=250, null=True)
    AddressProofType = models.CharField(max_length=200, null=True)
    AddressDoc = models.FileField(max_length=200, null=True)
    ServiceType = models.CharField(max_length=250, null=True)
    MontlyIncome = models.CharField(max_length=250, null=True)
    ExistingLoan = models.CharField(max_length=250, null=True)
    ExpectedLoanAmount = models.CharField(max_length=250, null=True)
    ProfilePic = models.FileField(max_length=200, null=True)
    Tenure = models.CharField(max_length=250, null=True)
    GName = models.CharField(max_length=250, null=True)
    Gmobnum = models.CharField(max_length=250, null=True)
    Gemail = models.CharField(max_length=250, null=True)
    Gaddress = models.CharField(max_length=250, null=True)
    SubmitDate = models.DateField(null=True)
    Remark = models.CharField(max_length=250, null=True)
    Status = models.CharField(max_length=250, null=True)
    LoanamountDisbursed = models.CharField(max_length=250, null=True)
    RateofInterest = models.CharField(max_length=250, null=True)
    DTenure = models.CharField(max_length=250, null=True)
    UpdationDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.signup.user.first_name

class Applicationtracking(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    Remark = models.CharField(max_length=250, null=True)
    Status = models.CharField(max_length=250, null=True)
    UpdationDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.application.signup.user.first_name

class Contact(models.Model):
    name = models.CharField(max_length=100, null=True)
    emailid = models.CharField(max_length=50, null=True)
    contact = models.CharField(max_length=15, null=True)
    message = models.CharField(max_length=300, null=True)
    enquiryDate = models.DateField(null=True)
    isread = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.emailid
