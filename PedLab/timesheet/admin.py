# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BUA
from .models import CustomUser, Record, Payment
# Register your models here.

#modify views in localhost:8080/admin
class UserAdmin(BUA):
    fieldsets = [
    (None,              {'fields': ['username','password']}),
    ('Personal info',   {'fields': ['first_name','last_name','email']}),
    ('Work info',       {'fields': ['user_type','rate_per_hour','date_joined']}),
    ]
    list_display=('id','username','first_name','last_name','user_type')
class RecordAdmin(admin.ModelAdmin):
    list_display = ('record_id','username','date','paid')
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id','username','amount','date_paid','transaction_type')

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Record,RecordAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.site_url="/timesheet"