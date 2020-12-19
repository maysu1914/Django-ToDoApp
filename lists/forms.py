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
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control'
        }),
        self.fields['description'].widget.attrs.update({
            'class': 'form-control'
        }),
        self.fields['status'].widget.attrs.update({
            'class': 'form-control'
        }),
        self.fields['deadline'].widget.attrs.update({
            'class': 'form-control'
        })

    class Meta:
        model = Item
        exclude = ('list_id',)
        widgets = {
            'deadline': DateInput()
        }
