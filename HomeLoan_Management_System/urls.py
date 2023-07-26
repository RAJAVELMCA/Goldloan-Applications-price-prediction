from django.contrib import admin
from django.urls import path
from homeloan.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

#login_required="adminlogin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', index, name='index'),
   

# ========================== Admin ==============================
    
    path('adminlogin', adminlogin, name='adminlogin'),
    path('dashboard/', dashboard, name='dashboard'),
    path('newLoan_req', newLoan_req, name='newLoan_req'),
    path('allLoan_req', allLoan_req, name='allLoan_req'),
    path('rejectLoan_req', rejectLoan_req, name='rejectLoan_req'),
    path('newRequest', newRequest, name='newRequest'),
    path('completeRequest', completeRequest, name='completeRequest'),
    path('adminViewloanReqDetails/<int:pid>', adminViewloanReqDetails, name='adminViewloanReqDetails'),
    path('viewDisbursedReqDetails/<int:pid>', viewDisbursedReqDetails, name='viewDisbursedReqDetails'),
    path('betweendateReport', betweendateReport, name='betweendateReport'),
    path('unread_Enquiry', unread_Enquiry, name='unread_Enquiry'),
    path('read_Enquiry', read_Enquiry, name='read_Enquiry'),
    path('viewContactDetails/<int:pid>', viewContactDetails, name='viewContactDetails'),
    path('search', search, name='search'),
    path('regUser', regUser, name='regUser'),
    path('deleteUser/<int:pid>', deleteUser, name='deleteUser'),
    path('adminChangePassword', adminChangePassword, name='adminChangePassword'),
    path('newRequest', newRequest, name='newRequest'),
    path('logout/', Logout, name='logout'),

# ======================== User ============================
    path('',home,name='home'),
    path('predict',Predicts,name='predict'),
    path('signup', signup, name='signup'),
    path('userlogin', userlogin, name='userlogin'),
    path('userDashboard', userDashboard, name='userDashboard'),
    path('applicationForm', applicationForm, name='applicationForm'),
    path('applicationHistory', applicationHistory, name='applicationHistory'),
    path('viewloanRequestDetails/<int:pid>', viewloanRequestDetails, name='viewloanRequestDetails'),
    path('changePassword', changePassword, name='changePassword'),
    path('otp',otp,name='otp'),
    path('emi',emi,name='emi'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
