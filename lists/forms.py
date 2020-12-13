from django.forms import ModelForm
from django import forms
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateListForm(ModelForm):
    class Meta:
        model = List
        exclude = ('user_id',)


class CreateItemForm(ModelForm):
    class Meta:
        model = Item
        exclude = ('list_id',)
        widgets = {
            'deadline': DateInput()
        }
