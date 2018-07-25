from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/$',views.view_profile, name='view_profile'),
    url(r'^profile/edit/$',views.edit_profile,name='edit_profile',),
    url(r'^profile/change_password/$',views.change_password,name='change_password',),
    url(r'^login/$', views.login, name='login'),
    url(r'^view_records/$',views.view_records, name='view_records'),
    url(r'^print_records/$',views.print_records, name='print_records'),
    url(r'^time_in/$',views.time_in,name='time_in'),
    url(r'^time_out/$',views.time_out,name='time_out'),
    url(r'^users/view/$',views.view_users,name='view_users'),
    url(r'^users/add$',views.add_user,name='add_user'),
    url(r'^users/edit_user=(?P<useredit>\w+)/$',views.edit_user,name='edit_user',),
    url(r'^users/delete_user=(?P<userdel>\w+)/$',views.delete_user,name='delete_user',),
    url(r'^view_payments/$',views.view_payments,name='view_payments'),
    url(r'^print_payments=(?P<print_id>\d+)/$',views.print_payments,name='print_payments'),
    url(r'^select_for_payment/$',views.select_for_payment,name='select_for_payment'),
    url(r'^testmail/$',views.testmail,name='testmail'),
    
    #path('accounts/', include('django.contrib.auth.urls')),
]