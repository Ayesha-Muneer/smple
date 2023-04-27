import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from LeakDetectionApp.models import Login, Consumer, Worker, Schedule, Appointment, Complaint


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'

def phone_number_validator(value):
    if not re.compile(r'^[7-9]\d{9}$').match(value):
        raise ValidationError('This is Not a Valid Phone Number')

class LoginForm(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = Login
        fields = ('username', 'password1', 'password2')


class UserForm(forms.ModelForm):
    Mobile_Number = forms.CharField(validators=[phone_number_validator])
    class Meta:
        model = Consumer
        fields = ('Consumer_number', 'Name', 'Address', 'Mobile_Number')


class WorkerForm(forms.ModelForm):
    Contact_Number = forms.CharField(validators=[phone_number_validator])
    class Meta:
        model = Worker
        fields = ('Name', 'Location', 'Contact_Number', 'Email','Photo')


class ScheduleForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    start_time = forms.TimeField(widget=TimeInput)
    end_time = forms.TimeField(widget=TimeInput)

    class Meta:
        model = Schedule
        fields = ('date', 'start_time', 'end_time')


class ComplaintForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)

    class Meta:
        model = Complaint
        fields = ('subject', 'feedback', 'date')
