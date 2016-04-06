from django import forms

from .models import *

class VM_Form(forms.Form):
    node = forms.CharField(label='Node', max_length=40,widget=forms.TextInput(attrs={'placeholder': 'Node'}))
    name = forms.CharField(label='Name', max_length=50,widget=forms.TextInput(attrs={'placeholder': 'Name of machine'}))
    ostype = forms.ChoiceField(label='Operating System')
    memory = forms.IntegerField(label='Memory (MB)',min_value=32,max_value=100000,widget=forms.NumberInput(attrs={'value': 4000}))

class CD_DVD(forms.Form):
    storage = forms.ChoiceField(label='Storage')
    iso = forms.ChoiceField(label='ISO Image')

class Disk(forms.Form):
    device = forms.ChoiceField(label='Bus/Device')
    storage = forms.ChoiceField(label='Storage')
    size = forms.IntegerField(label='Disk size (GB)',min_value=1,max_value=10000,widget=forms.NumberInput(attrs={'value': 100}))
    disk_format = forms.ChoiceField(label='Format')

class CPU(forms.Form):
    cores = forms.IntegerField(label='Cores',min_value=1,max_value=500,widget=forms.NumberInput(attrs={'value': 4}))
    numa = forms.BooleanField(label='Numa')

class Network(forms.Form):
    bridge = forms.ChoiceField(label='Bridge')
    firewall = forms.BooleanField(label='Firewall')
    model = forms.ChoiceField(label='Model')
