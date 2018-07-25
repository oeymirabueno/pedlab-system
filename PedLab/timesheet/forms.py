from django.forms import ModelForm, PasswordInput, ModelMultipleChoiceField,CheckboxSelectMultiple

from .models import CustomUser, Record

class AddUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','password','first_name','last_name','email','user_type','rate_per_hour']
class EditUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','email','user_type','rate_per_hour']

class EditProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','email',]

class SelectForPaymentForm(ModelForm):
    table = ModelMultipleChoiceField(queryset=Record.objects.all().exclude(time_out=None).exclude(paid='Y'),widget=CheckboxSelectMultiple,required=False)
    class Meta:
        model = Record
        fields = ['table']

class FilterSelectForm(ModelForm):
    class Meta:
        model = Record
        fields = ['username']