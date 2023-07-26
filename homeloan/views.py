import random
from datetime import date
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate, logout, login
import math
from django.contrib import auth,messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User,auth
from.models import predict
# Create your views here.
import numpy as np
import pandas as pd

import os
import matplotlib.pyplot as plt
#import pandas_datareader as web
import datetime as dt

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

import matplotlib.dates as dates
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from django.contrib.auth.decorators import login_required


otp=None
def home(request):
    return render(request,'home.html')

def otpGen(request):
	string = '0123456789'
	OTP = ''
	for i in range(4):
		OTP += string[math.floor(random.random() * len(string))]
        
    
	return OTP
 

def otpSend(request,user,otp):
    #emailto = user.email
    from redmail import outlook

    outlook.user_name = "rajavelraja732@outlook.com"
    outlook.password = "8940365257@Ra"

    outlook.send(
            receivers=user.email,
            subject="OTP",
            #text="Hi, this is an example."
        text = """\
                Your otp is {0}. Do not share it with anyone by any means. This is confidential and to be used by you only.",'admin@no-reply.com',
                    \
                """.format(otp))
#@login_required(login_url="adminlogin")


def Predicts(request):
    if request.method=="POST":
        open=request.POST['Open'] 
        high=request.POST['High'] 
        low=request.POST['Low'] 
        close=request.POST['Close'] 
        wap=request.POST['WAP'] 
        no_of_shares=request.POST['No. of Shares'] 
        no_of_trades=request.POST['No. of Trades'] 
        deli_qty=request.POST['Deliverable Quantity'] 
        traded_qty=request.POST['Deli. Qty to Traded Qty'] 
        spread_hl=request.POST['Spread H-L'] 
        spread_co=request.POST['Spread C-O'] 
        stock=pd.read_csv(r"E:\Django\goldloanapp\homeloan\static\BSE-BOM590111.csv")
        print(stock[0:3])
        n=len(stock)
        data=stock[0:(n//10)*9]
        test_data=stock[(n//10)*9:]
        fig=make_subplots(specs=[[{"secondary_y":False}]])
        fig.add_trace(go.Scatter(x=stock['Open'],y=stock['Total Turnover'].rolling(window=28).mean(),name="netflix"),secondary_y=False,)
        fig.update_layout(autosize=False,width=700,height=500,title_text="Gold Price")
        fig.update_xaxes(title_text="Open")
        fig.update_yaxes(title_text="Total Turnover",secondary_y=False)
        fig.show()
        plt.show()
        fig=make_subplots(specs=[[{"secondary_y":False}]])
        fig.add_trace(go.Scatter(x=stock['High'],y=stock['Total Turnover'].rolling(window=28).mean(),name="netflix"),secondary_y=False,)
        fig.update_layout(autosize=False,width=700,height=500,title_text="Gold Price")
        fig.update_xaxes(title_text="High")
        fig.update_yaxes(title_text="Total Turnover",secondary_y=False)
        fig.show()
        plt.show()
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(data['Open'].values.reshape(-1,1))
        prediction_days = 100

        x_train = []
        y_train = []

        for x in range(prediction_days, len(scaled_data)):
            x_train.append(scaled_data[x - prediction_days:x, 0])
            y_train.append(scaled_data[x, 0])
    
        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        print(x_train.shape)
        print(y_train.shape)
        def LSTM_model():
    
            model = Sequential()    
            model.add(LSTM(units = 50, return_sequences = True, input_shape = (x_train.shape[1],1)))
            model.add(Dropout(0.2))
            model.add(LSTM(units = 50, return_sequences = True))
            model.add(Dropout(0.2))
            model.add(LSTM(units = 50))
            model.add(Dropout(0.2))
            model.add(Dense(units=1))
    
            return model
        model = LSTM_model()
        model.summary()
        model.compile(optimizer='adam', loss='mean_squared_error')
        checkpointer = ModelCheckpoint(filepath = 'weights_best.hdf5', verbose = 1, save_best_only = True)
        model.fit(x_train, y_train, epochs=5, batch_size = 32,callbacks = [checkpointer])
        actual_prices = test_data['Open'].values
        total_dataset = pd.concat((data['Open'], test_data['Open']), axis=0)

        model_inputs = total_dataset[len(total_dataset)-len(test_data)-prediction_days:].values
        model_inputs = model_inputs.reshape(-1,1)
        model_inputs = scaler.transform(model_inputs)
        x_test = []
        for x in range(prediction_days,len(model_inputs)):
            x_test.append(model_inputs[x-prediction_days:x,0])

        x_test = np.array(x_test)
        x_test = np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))

        predicted_prices = model.predict(x_test)
        predicted_prices = scaler.inverse_transform(predicted_prices)
        plt.plot(actual_prices, color='black', label=f"actual price")
        plt.plot(predicted_prices, color= 'green', label=f"predicted price")
        plt.title(f"Gold Price")
        plt.xlabel("day")
        plt.ylabel(f"price")
        plt.legend()
        plt.show()
        real_data = [model_inputs[len(model_inputs)+1-prediction_days:len(model_inputs+1),0]]
        real_data = np.array(real_data)
        real_data = np.reshape(real_data,(real_data.shape[0],real_data.shape[1],1))
        print(real_data.shape)
        prediction = model.predict(real_data)
        predict1=model.predict([[open,high,low,close,wap,no_of_shares,no_of_trades,deli_qty,traded_qty,spread_hl,spread_co]])
        prediction = scaler.inverse_transform(predict1)

        print(f"prediction: {prediction}")
        return render(request,"user/output.html")
    else:
        return render(request,"user/predict.html")

def index(request):
    try:
        if request.method == 'POST':
            name = request.POST['name']
            emailid = request.POST['emailid']
            contact = request.POST['contact']
            message = request.POST['message']
            try:
                Contact.objects.create(name=name, contact=contact, emailid=emailid,message=message, enquiryDate=date.today(),isread="No")
                error = "no"
            except:
                error = "yes"
    except:
        rate = None
        if request.method == "POST":
            lamount = request.POST['lamount']
            lrate = request.POST['lrate']
            tenure = request.POST['tenure']

            rate = float(lrate) / 12  # converting int to month
            time = int(tenure) * 12  # Converting in to month
            simpleinterst = rate * time * int(lamount) / 100

            totalpayable = simpleinterst + int(lamount)
            monthlyEmi = round(totalpayable / time, 2)
    return render(request, 'index.html', locals())

# ================ Admin Here ====================

def adminlogin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user =authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
                return redirect('dashboard')
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'adminlogin.html', locals())



                


def emi(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')

    user = User.objects.get(id=request.user.id)
    signup = Signup.objects.get(user=user)

    rate = None
    if request.method == "POST":
        lamount =request.POST['lamount']
        lrate = request.POST['lrate']
        tenure = request.POST['tenure']


        rate = float(lrate) / 12  # converting int to month
        time = int(tenure) * 12  # Converting in to month
        simpleinterst = rate * time * int(lamount) / 100

        totalpayable = simpleinterst + int(lamount)
        monthlyEmi = round(totalpayable / time, 2)
    return render(request,'user/emi.html',locals())



def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    totalreguser = Signup.objects.all().count()
    totalnewloan = Application.objects.filter(Status__isnull=True).count()
    totalapprovedloan = Application.objects.filter(Status="Approved").count()
    totalrejectloan = Application.objects.filter(Status="Rejected").count()
    totaldisbursedloan = Application.objects.filter(Status="Disbursed").count()
    totalunread = Contact.objects.filter(isread="No").count()
    totalread = Contact.objects.filter(isread="yes").count()
    return render(request, 'admin/dashboard.html', locals())

def newLoan_req(request):
    if not request.user.is_authenticated:
        return redirect('newLoan_req')
    application = Application.objects.filter(Status__isnull=True)
    return render(request, 'admin/newLoan_req.html', locals())

def allLoan_req(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    application = Application.objects.all()
    return render(request, 'admin/allLoan_req.html', locals())

def rejectLoan_req(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    application = Application.objects.filter(Status="Rejected")
    return render(request, 'admin/rejectLoan_req.html', locals())

def adminViewloanReqDetails(request,pid):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    application = Application.objects.get(id=pid)
    appreport = Applicationtracking.objects.filter(application=application)

    reportcount = Applicationtracking.objects.filter(application=application).count()

    if request.method == "POST":
        if request.method == "POST":
            status = request.POST['Status']
            remark = request.POST['Remark']

            try:
                apptracking = Applicationtracking.objects.create(application=application, Remark=remark, Status=status)
                application.Status = status
                application.Remark = remark
                application.save()
                error = "no"
            except:
                error = "yes"
    return render(request, 'admin/adminViewloanReqDetails.html', locals())

def newRequest(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    application = Application.objects.filter(Status='Approved')
    return render(request, 'admin/newRequest.html', locals())

def completeRequest(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    application = Application.objects.filter(Status='Disbursed')
    return render(request, 'admin/completeRequest.html', locals())

def viewDisbursedReqDetails(request,pid):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    application = Application.objects.get(id=pid)
    appreport = Applicationtracking.objects.filter(application=application)

    reportcount = Applicationtracking.objects.filter(application=application).count()

    try:
        rate = float(application.RateofInterest)/12  #converting int to month
        time = int(application.DTenure)*12       #Converting in to month
        simpleinterst = rate * time * int(application.LoanamountDisbursed) / 100

        totalpayable =simpleinterst + int(application.LoanamountDisbursed)
        monthlyEmi = round(totalpayable/time,2)
    except:
        pass

    if request.method == "POST":
        LoanamountDisbursed =request.POST['LoanamountDisbursed']
        RateofInterest = request.POST['RateofInterest']
        DTenure = request.POST['DTenure']
        remark = request.POST['Remark']

        try:
            apptracking = Applicationtracking.objects.create(application=application, Remark=remark, Status="Disbursed")
            application.LoanamountDisbursed = LoanamountDisbursed
            application.RateofInterest = RateofInterest
            application.DTenure = DTenure
            application.Status = 'Disbursed'
            application.Remark = remark
            application.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'admin/viewDisbursedReqDetails.html', locals())

def betweendateReport(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    if request.method == "POST":
        fd = request.POST['FromDate']
        td = request.POST['ToDate']
        application = Application.objects.filter(Q(SubmitDate__gte=fd) & Q(SubmitDate__lte=td))
        return render(request, 'admin/reportbtwdates.html', locals())
    return render(request, 'admin/betweendateReport.html')

def unread_Enquiry(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    contact = Contact.objects.filter(isread="No")
    return render(request, 'admin/unread_Enquiry.html', locals())

def read_Enquiry(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    contact = Contact.objects.filter(isread="yes")
    return render(request, 'admin/read_Enquiry.html', locals())

def viewContactDetails(request,pid):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    contact = Contact.objects.get(id=pid)
    contact.isread = "yes"
    contact.save()
    return render(request, 'admin/viewContactDetails.html', locals())

def search(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    sd = None
    signup = None
    if request.method == 'POST':
        sd = request.POST['searchdata']
    try:
        signup = Signup.objects.get(MobileNumber=sd)
        application = Application.objects.filter(signup=signup)
    except:
        application = Application.objects.filter(ApplicationNumber=sd)
    return render(request, 'admin/search.html', locals())

def regUser(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    reguser = Signup.objects.all()
    return render(request, 'admin/regUser.html', locals())

def deleteUser(request,pid):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    User.objects.get(id=pid).delete()
    return redirect('regUser')

def adminChangePassword(request):
    if not request.user.is_authenticated:
        return redirect('adminlogin')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'admin/adminChangePassword.html', locals())

def Logout(request):
    logout(request)
    return redirect('index')

# ====================  User ====================================

def signup(request):
    error =""
    if request.method == 'POST':
        fname = request.POST['firstName']
        lname = request.POST['lastName']
        mob = request.POST['MobileNumber']
        emailid = request.POST['emailid']
        pwd = request.POST['password']

        try:
            user = User.objects.create_user(username=emailid, password=pwd, first_name=fname, last_name=lname)
            Signup.objects.create(user=user, MobileNumber=mob)
            error = "no"
        except:
            error = "yes"
    return render(request, 'signup.html', locals())

def userlogin(request):
    error =""
    if request.method == 'POST':
        e = request.POST['email']
        p = request.POST['password']
        user = authenticate(username=e, password=p)
        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'userlogin.html', locals())

def userDashboard(request):
  
    return render(request, 'user/userDashboard.html', locals())

def applicationForm(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')

    user = User.objects.get(id=request.user.id)
    signup = Signup.objects.get(user=user)

    error = ""
    if request.method == "POST":
        applicationNo = str(random.randint(10000000, 99999999))
        PanNumber = request.POST['PanNumber']
        PanCardCopy = request.FILES['PanCardCopy']
        Address = request.POST['Address']
        AddressProofType = request.POST['AddressProofType']
        AddressDoc = request.FILES['AddressDoc']
        ServiceType = request.POST['ServiceType']
        MontlyIncome = request.POST['MontlyIncome']
        ExistingLoan = request.POST['ExistingLoan']
        ExpectedLoanAmount = request.POST['ExpectedLoanAmount']
        ProfilePic = request.FILES['ProfilePic']
        Tenure = request.POST['Tenure']
        GName = request.POST['GName']
        Gmobnum = request.POST['Gmobnum']
        Gemail = request.POST['Gemail']
        Gaddress = request.POST['Gaddress']

        try:
            Application.objects.create(signup=signup, ApplicationNumber=applicationNo, PanNumber=PanNumber, PanCardCopy=PanCardCopy,
                                       Address=Address, AddressProofType=AddressProofType, AddressDoc=AddressDoc, ServiceType=ServiceType,
                                       MontlyIncome=MontlyIncome, ExistingLoan=ExistingLoan, ExpectedLoanAmount=ExpectedLoanAmount, ProfilePic=ProfilePic,
                                       Tenure=Tenure, GName=GName, Gmobnum=Gmobnum, Gemail=Gemail, Gaddress=Gaddress, SubmitDate=date.today())
                                       
            error = "no"
           
        except:
            error = "yes"
    return render(request, 'user/applicationForm.html', locals())

def applicationHistory(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    signup = Signup.objects.get(user=request.user)
    application = Application.objects.filter(signup=signup)
    return render(request, 'user/applicationHistory.html', locals())

def viewloanRequestDetails(request,pid):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    application = Application.objects.get(id=pid)
    appreport = Applicationtracking.objects.filter(application=application)
    reportcount = Applicationtracking.objects.filter(application=application).count()

    try:
        rate = float(application.RateofInterest) / 12  # converting int to month
        time = int(application.DTenure) * 12  # Converting in to month
        simpleinterst = rate * time * int(application.LoanamountDisbursed) / 100

        totalpayable = simpleinterst + int(application.LoanamountDisbursed)
        monthlyEmi = round(totalpayable / time, 2)
    except:
        pass

    return render(request, 'user/viewloanRequestDetails.html', locals())

def changePassword(request):
    if not request.user.is_authenticated:
        return redirect('userlogin')
    if not request.user.is_authenticated:
        return redirect('employees')
    error = ""
    user = request.user
    if request.method == "POST":
        o = request.POST['oldpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if user.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = 'not'
        except:
            error = "yes"
    return render(request, 'user/changePassword.html', locals())
def otp(request):
    return render(request,'otp.html',locals())