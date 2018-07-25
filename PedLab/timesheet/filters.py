from .models import Record, Payment
import django_filters

class RecordFilter(django_filters.FilterSet):
    date_between = django_filters.DateFromToRangeFilter(name='date',label='Date Between (YYYY-MM-DD)')
    class Meta:
        model = Record
        fields = ['date_between', 'paid']

class PaymentFilter(django_filters.FilterSet):
    date_year = django_filters.NumberFilter('date',lookup_expr='year',label="Filter by Year")
    date_month = django_filters.NumberFilter('date',lookup_expr='month', label="Filter by Month")
    date_between = django_filters.DateFromToRangeFilter(name='date_paid',label='Date Between (YYYY-MM-DD)')
    class Meta:
        model = Payment
        fields = ['date_year','date_month','date_between']