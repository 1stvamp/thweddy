from django import forms

from thweddy.main.models import *

class TwitterUserForm(forms.ModelForm):
    class Meta:
        model = TwitterUser


