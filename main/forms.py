from django import forms

from .models import *

def get_templates():
  return []

def get_formats():
  return []

class VM_Form(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(VM_Form, self).__init__(*args, **kwargs)
    self.fields['template'] = forms.ChoiceField(choices=get_templates())

  class Meta:
    model = VM
    exclude = ['user','cluster','disk','nic']
    labels = {
      'vm_name': 'Name',
      'memory': 'Memory (GB)',
    }
    widgets = {
      'vm_name': forms.TextInput(attrs={'placeholder': 'Name of Machine'}),
      'description': forms.Textarea(attrs={
                          'placeholder': 'Description of Machine',
                          'rows': 3,
                        }
                      ),
      'memory': forms.NumberInput(attrs={'value': 1}),
      'cores': forms.NumberInput(attrs={'value': 1}),
    }

class Disk_Form(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(Disk_Form, self).__init__(*args, **kwargs)
    self.fields['format'] = forms.ChoiceField(choices=get_formats())

  class Meta:
    model = Disk
    exclude = ['storage_domain','status','interface']
    labels = {
      'size': 'Size (GB)',
    }
    widgets = {
      'disk_name': forms.TextInput(attrs={'placeholder': 'Name of Disk'}),
      'size': forms.NumberInput(attrs={'value': 1}),
    }
