# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from datetime import date, datetime, timedelta
from django.forms.models import model_to_dict
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, Record, Payment
from .filters import RecordFilter, PaymentFilter
from .adminfilters import AdminRecordFilter,AdminUserFilter, AdminPaymentFilter, AdminSelectFilter
from .forms import AddUserForm, EditUserForm, EditProfileForm, SelectForPaymentForm, FilterSelectForm

# Create your views here.

#common views
def index(request):
    if(request.user.user_type !='A'):
        return render(request,'timesheet/index.html')
    else:
        return render(request,'timesheet/admin_index.html')
def login(request):
    return
def view_profile(request):
    current_user = CustomUser.objects.get(username=request.user.username)
    return render(request, 'timesheet/view_profile.html',{'display_user':current_user})
def edit_profile(request):
    usel = CustomUser.objects.get(username=request.user.username)
    data = model_to_dict(usel)
    error_message=""
    if(request.method=="POST"):
        form=EditProfileForm(request.POST,instance=usel)
        if form.is_valid():
            form.save()
            with open("timesheet/user_files/"+form.cleaned_data.get('username')+".txt","a") as file:

                file.write(str(timezone.localtime()))
                for key, value in form.cleaned_data.iteritems():
                    file.write(" - "+str(value))
                file.write(" - updated by "+str(request.user.username))
                file.write("\n")
            return redirect(reverse('view_profile'),{'message':"user edited successfully"})
        else:
            error_message="EDIT FAIL"
            form=EditProfileForm(request.POST,instance=usel)
    else:
        form=EditProfileForm(data)
    return render(request, 'timesheet/edit_user.html', {'usel':usel,'form':form, 'error_message': error_message})
def change_password(request):
    error_message=""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            error_message="updated_successfully"
            return redirect('view_profile')
        else:
            error_message=""
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'timesheet/change_password.html',{'form':form,'error_message':error_message})
def time_in(request):
    #request access to last row in records accdng to timestamp.
    #if time_out value null, show error.
    #else, create new record. show confirmation button, returns to index.
    last_record = Record.objects.filter(username=request.user).last()
    if(last_record and last_record.time_out is None):
        if(request.user.user_type !='A'):
            return render(request,'timesheet/index.html',{'error_message': "You have not timed out yet."},)
        else:
            return render(request,'timesheet/admin_index.html',{'error_message': "You have not timed out yet."},)       
    else:
        last_user = CustomUser.objects.get(username=request.user.username)
        new_record = Record(username=last_user,time_in=timezone.localtime(),time_out=None,)
        new_record.save()
        return render(request,'timesheet/time_in.html')
def time_out(request):
    #request access to last row in records accdng to timestamp.
    #if time_out value !null, show error.
    #else, alter. show confirmation button, returns to index.
    last_record = Record.objects.filter(username=request.user).last()
    if(last_record is None or last_record.time_out is not None):
        if(request.user.user_type !='A'):
            return render(request,'timesheet/index.html',{'error_message': "You have not timed in yet."},)
        else:
            return render(request,'timesheet/admin_index.html',{'error_message': "You have not timed in yet."},)
    else:
        last_record.time_out=timezone.localtime()
        last_record.save()
        
        rate=CustomUser.objects.get(username=request.user.username).rate_per_hour
        outdelta=timedelta(hours=last_record.time_out.hour,minutes=last_record.time_out.minute,seconds=last_record.time_out.second)
        indelta=timedelta(hours=last_record.time_in.hour,minutes=last_record.time_in.minute,seconds=last_record.time_in.second)
        
        timedif=outdelta-indelta #datetime.combine(date.today(),last_record.time_in)
        last_record.amount=Decimal.from_float(timedif.total_seconds())*rate/3600
        last_record.save()
        return render(request,'timesheet/time_out.html')

def view_records(request):
    
    if(request.user.user_type =='R'):
        last_user=CustomUser.objects.get(username=request.user.username)
        latest_records_list = Record.objects.filter(username=last_user).order_by('date')
        record_filter = RecordFilter(request.GET, queryset=latest_records_list)
    else:
        latest_records_list = Record.objects.order_by('date')
        record_filter = AdminRecordFilter(request.GET, queryset=latest_records_list)
    return render(request, 'timesheet/view_records.html', {'latest_records_list': latest_records_list,'filter':record_filter})
def print_records(request):

    #get records
    if(request.user.user_type =='R'):
        last_user=CustomUser.objects.get(username=request.user.username)
        latest_records_list = Record.objects.filter(username=last_user).order_by('date')
    else:
        latest_records_list = Record.objects.order_by('date')
    
    applied_filters = request.GET
    print(applied_filters)
    if('username' in applied_filters): #if admin is viewing the records
        if(applied_filters.get('username') is not ''):
            latest_records_list = latest_records_list.filter(username=applied_filters.get('username'))
        if(applied_filters.get('date_year') is not ''):
            latest_records_list = latest_records_list.filter(date__year=applied_filters.get('date_year'))
        if(applied_filters.get('date_month') is not ''):
            latest_records_list = latest_records_list.filter(date__month=applied_filters.get('date_month'))
        
    #else: #if non-admin
     #   if(applied_filters.get('paid') is not ''):
     #       latest_records_list = latest_records_list.filter(paid=applied_filters.get('paid'))
    
    if(applied_filters.get('paid') is not ''):
        latest_records_list = latest_records_list.filter(paid=applied_filters.get('paid'))
    if(applied_filters.get('date_between_0') is not '' or applied_filters.get('date_between_1') is not ''):
        date_a=applied_filters.get('date_between_0')
        date_b=applied_filters.get('date_between_1')
        if date_a is '': date_a="0001-01-01"
        if date_b is '': date_b="9999-12-31"
        
        latest_records_list = latest_records_list.filter(date__range=[date_a,date_b])    
    #records_list = Record.objects.filter(record_id__in=applied_filters)
    return render(request, 'timesheet/print_records.html',{'latest_records_list': latest_records_list, 'last_user':request.user.username,'access_time':timezone.localtime()})

def view_payments(request):
    if(request.user.user_type == 'R'):
        last_user=CustomUser.objects.get(username=request.user.username)
        payment_list = Payment.objects.filter(username=last_user).order_by('date_paid')
        payment_filter = PaymentFilter(request.GET, queryset=payment_list)
    else:
        payment_list = Payment.objects.order_by('date_paid')
        payment_filter = AdminPaymentFilter(request.GET, queryset=payment_list)
    applied_filters=request.GET
    if(applied_filters.get('date_between_0') is not '' or applied_filters.get('date_between_1') is not ''):
        date_a=applied_filters.get('date_between_0')
        date_b=applied_filters.get('date_between_1')
        if date_a is '': date_a="0001-01-01"
        if date_b is '': date_b="9999-12-31"
        payment_list = payment_list.filter(date_paid__range=[date_a,date_b])
    return render(request, 'timesheet/view_payments.html', {'payment_list': payment_list,'filter':payment_filter})

def print_payments(request,print_id):
    payment_to_print = Payment.objects.get(transaction_id=print_id)
    records_in_payment = Record.objects.filter(record_id__in=payment_to_print.record.all())
    total=0
    for record in records_in_payment:
        if(record.amount is None):
            total+=0
        else:
            total+=record.amount
    return render(request,'timesheet/print_payments.html',{'payment_to_print':payment_to_print,'records_in_payment':records_in_payment,'total':total,'last_user':request.user.username,'access_time':timezone.localtime()})


#secretary views share with RA views but with greater access, i.e. viewing all records, not just self

#admin views

def view_users(request):
    
    user_list = CustomUser.objects.filter().order_by('date_joined')
    user_filter = AdminUserFilter(request.GET, queryset=user_list)
    return render(request, 'timesheet/view_users.html', {'user_list': user_list,'filter':user_filter,})

def add_user(request):
    error_message=""
    if(request.method=="POST"):
        form=AddUserForm(request.POST)
        if form.is_valid():
            if(form.cleaned_data.get('user_type')=="A"):
                new_user=CustomUser.objects.create_superuser(**form.cleaned_data)
            else:
                new_user=CustomUser.objects.create_user(**form.cleaned_data)
            new_user.save()
        
            with open("timesheet/user_files/"+form.cleaned_data.get('username')+".txt","a") as file:
                file.write(str(timezone.localtime())+" - "+str(form.cleaned_data.get('rate_per_hour'))+"\n")
            return HttpResponseRedirect(reverse('view_users'))
        else:
            error_message="FAIL"
            form=AddUserForm(request.POST)
    else:
        form=AddUserForm()
    return render(request, 'timesheet/add_user.html',{'form':form,'error_message':error_message})

def edit_user(request,useredit):
    usel = CustomUser.objects.get(username=useredit)
    data = model_to_dict(usel)
    error_message=""
    if(request.method=="POST"):
        form=EditUserForm(request.POST,instance=usel)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            for key, value in form.cleaned_data.iteritems():
                print(key,value)
            if(form.cleaned_data.get('user_type')=="A"):
                user = CustomUser.objects.get(username=form.cleaned_data.get('username'))
                user.is_staff = True
                user.is_admin = True
                user.is_superuser = True
                user.save()
            else:
                user = CustomUser.objects.get(username=form.cleaned_data.get('username'))
                user.is_staff = False
                user.is_admin = False
                user.is_superuser = False
                user.save()
            with open("timesheet/user_files/"+form.cleaned_data.get('username')+".txt","a") as file:

                file.write(str(timezone.localtime()))
                for key, value in form.cleaned_data.iteritems():
                    file.write(" - "+str(value))
                file.write(" - updated by "+str(request.user.username))
                file.write("\n")
            return redirect(reverse('view_users'),{'message':"user edited successfully"})
        else:
            error_message="EDIT FAIL"
            form=EditUserForm(request.POST,instance=usel)
    else:
        form=EditUserForm(data)
    return render(request, 'timesheet/edit_user.html', {'usel':usel,'form':form, 'error_message': error_message})
def delete_user(request, userdel):

    usel=CustomUser.objects.get(username=userdel)
    if(request.method=="POST"):
        usel.delete()
        return redirect(reverse('view_users'),{'message':"user deleted successfully"})
    return render(request,'timesheet/delete_user.html',{'usel':usel})

def select_for_payment(request):
    error_message=""
    #GET method is for filtering records
    if(request.method=="GET"):
        filterform = FilterSelectForm(request.GET)
        form=SelectForPaymentForm()
        if(request.GET.get('username') is not None):
            form.fields['table'].queryset=Record.objects.all().exclude(time_out=None).exclude(paid='Y').filter(username=request.GET.get('username'))
    #POST method is for actual selection and submission of records
    elif(request.method=="POST"):
        form=SelectForPaymentForm(request.POST)
        if form.is_valid():
            update_ids=request.POST.getlist('table')
            
            un_update = Record.objects.values('username').filter(record_id__in=update_ids).distinct()
            un_update = list(CustomUser.objects.filter(id__in=un_update))
            print (un_update)
            for user in un_update:
                new_payment = Payment(username=CustomUser.objects.get(username=user.username),amount=0,transaction_type='payment')
                new_payment.save()
                update = list(Record.objects.filter(record_id__in=update_ids).filter(username=user).exclude(paid="Y"))
                for record in update:
                    if (record.paid=="N"):
                        record.paid="Y"
                        record.save()

                        new_payment.record.add(record)

                        amt=record.amount
                        new_payment.amount+=amt
                        new_payment.save()
                if (new_payment.amount==0):
                    new_payment.delete()
            return HttpResponseRedirect(reverse('view_payments'))
        else:
            error_message="FAIL"
            form=SelectforPaymentForm(request.POST)
    else:
        form=SelectForPaymentForm()
    return render(request, 'timesheet/select_for_payment.html', {'form':form,'filterform':filterform,'error_message':error_message})


def testmail(request):
    send_mail('hello','wow',settings.EMAIL_HOST_USER,['josemirabueno@gmail.com'])
    return render(request,'timesheet/admin_index.html',{'error_message': "mail sent!"},)       
