import datetime

from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.template import Template
from .models import Leagues, Follower, Notification
from material import Layout, Row, Fieldset

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    layout = Layout( Row('first_name', 'last_name'),
                    'username', 'email',                       
                    Row('password1', 'password2')) 
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class LeagueForm(ModelForm):
    name = forms.CharField(max_length=30, required=True)
    terms = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    # status = forms.ChoiceField(choices=(('0', 'Normal'), ('1', 'Stop'), ('2', 'Done')))
    layout = Layout( Row('name'), 'terms') 
    class Meta:
        model = Leagues
        fields =  ('name', 'terms')

class FollowerForm(ModelForm):
    class Meta:
        model = Follower
        fields = '__all__'

class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'
