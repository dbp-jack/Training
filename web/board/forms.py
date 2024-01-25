from django import forms
from board.models import Accident, Replay, Safety
from django.contrib.auth.forms import UserCreationForm
from .models import (Manage, Accident, Replay, Safety,
                     Group, Fieldlog, Employee)
from django.forms import DateInput
from django.core.exceptions import ValidationError
#회원가입
class SignupForm(UserCreationForm):
    class Meta:
        model= Manage
        fields = ('first_name', 'last_name', 'position', 'email', 'username', 'password1', 'password2', 'address', 'call')

#사고보고
class PostForm(forms.ModelForm):
    class Meta:
        model = Accident
        fields =('ac_area', 'ac_status', 'img', 'ac_cont')
        exclude={'writer', }

#안전점검일지
class SafetyForm(forms.ModelForm):
    class Meta:
        model = Safety
        fields =('scl_area', 'scl_status', 'img', 'scl_cont')
        exclude={'writer', }

#작업현장일지
class FieldlogForm(forms.ModelForm):
    class Meta:
        model = Fieldlog
        fields =('fl_area', 'fl_status', 'img', 'fl_cont')
        exclude={'writer', }

#직원
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'start_time': DateInput(attrs={'type': 'date'}),
            'end_time': DateInput(attrs={'type': 'date'}),
            'date_of_birth': DateInput(attrs={'type': 'date'}),
        }
#댓글
class ReplayForm(forms.ModelForm):
    class Meta:
        model = Replay
        fields = ('contents', )
        exclude = ('writer', )

#근무편성
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['employee1', 'employee2']
# message = forms.CharField(widget = forms.Textarea)
# db_table = ''
# managed = True
# verbose_name = 'ModelName'
# verbose_name_plural = 'ModelNames'
# fields = ('contents', ) #__all__