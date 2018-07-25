from django import forms
from .models import Record, CustomUser, Payment
import django_filters

#all of these are for the filtering in the admin access

class AdminRecordFilter(django_filters.FilterSet):
    date_year = django_filters.NumberFilter('date',lookup_expr='year',label="Filter by Year")
    date_month = django_filters.NumberFilter('date',lookup_expr='month', label="Filter by Month")
    date_between = django_filters.DateFromToRangeFilter(name='date',label='Date Between (YYYY-MM-DD)')
    class Meta:
        model = Record
        fields = ['username', 'date_year','date_month','date_between', 'paid']

class AdminUserFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'date_joined','user_type']

#viewing payments
class AdminPaymentFilter(django_filters.FilterSet):
    date_year = django_filters.NumberFilter('date_paid',lookup_expr='year',label="Filter by Year")
    date_month = django_filters.NumberFilter('date_paid',lookup_expr='month', label="Filter by Month")
    date_between = django_filters.DateFromToRangeFilter(name='date_paid',label='Date Between (YYYY-MM-DD)')
    class Meta:
        model = Payment
        fields = ['username','date_year','date_month','date_between']

#selecting payments
class AdminSelectFilter(django_filters.FilterSet):
    date_year = django_filters.NumberFilter('date',lookup_expr='year',label="Filter by Year")
    date_month = django_filters.NumberFilter('date',lookup_expr='month', label="Filter by Month")
    class Meta:
        model = Record
        fields = ['username','date_year','date_month']