from django import forms
from django.forms import ModelForm
from .models import ContactInfo


class ContactInfoForm(forms.ModelForm):
    
    class Meta:
        model = ContactInfo
        fields = ("facility_id","facility_name", "phone_no", "partner_name")

        widgets = {
            'facility_id':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'facility_id'}),
            'facility_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'facility_name'}),
            'phone_no':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'phone_no'}),
            'partner_name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'partner_name'}),
            
        }
