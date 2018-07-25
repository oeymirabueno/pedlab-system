# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import AbstractUser

# Create your models here.

#we add user_type and rate_per_hour to CustomUser
@python_2_unicode_compatible
class CustomUser(AbstractUser):
    usertype_choices = (
        ('R','RA'),
        ('S','Secretary'),
        ('A','Admin')
    )

    
    user_type = models.CharField(max_length=1,choices=usertype_choices,default='R')
    rate_per_hour = models.DecimalField(max_digits=7,decimal_places=2,null=True)
    def is_usertype(self):
        return self.get_user_type_display()
    def __str__(self):
        return "%s %s"  % (self.first_name,self.last_name)
    def actual_un(self):
        return self.username

#stores timesheet data
@python_2_unicode_compatible
class Record(models.Model):
    paid_choices = (('Y','Yes'),('N','No'))

    record_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time_in = models.TimeField('Time In')
    time_out = models.TimeField('Time Out',null=True,blank=True)
    amount = models.DecimalField('Amount',null=True,blank=True,max_digits=12,decimal_places=2)
    paid = models.CharField(max_length=1,choices=paid_choices,default='N')

    def is_paid(self):
        return self.paid
    def __str__(self):
        return "%s by %s" % (self.record_id,self.username)
    def actual_id(self):
        return "%s" % self.record_id    

@python_2_unicode_compatible
class Payment(models.Model):
    type_choices=(('payment','payment'),('update','budget update'))

    transaction_id=models.AutoField(primary_key=True)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    record = models.ManyToManyField(Record)
    amount = models.DecimalField(max_digits=12,decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)
    transaction_type = models.CharField(max_length=10,choices=type_choices,default='payment')

    def __str__(self):
        return "%s" % self.transaction_id

#WIP: determine all labels to be used
#@python_2_unicode_compatible
#class ProdRating(models.Model):
