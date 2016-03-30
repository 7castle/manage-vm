from django import forms

from .models import *

def get_templates():
  return []

class VM_Form(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(VM_Form, self).__init__(*args, **kwargs)
    self.fields['template'] = forms.ChoiceField(choices=get_templates())

  class Meta:
    model = VM
    exclude = ['user','vmid','ip','storage']
    labels = {
      'hostname': 'Name',
      'memory': 'Memory (GB)',
      'swap': 'Swap (GB)',
      'disk': 'Disk Size (GB)',
    }
    widgets = {
      'hostname': forms.TextInput(attrs={'placeholder': 'Hostname of Machine'}),
      'description': forms.Textarea(attrs={
                          'placeholder': 'Description of Machine',
                          'rows': 3,
                        }
                      ),
      'memory': forms.NumberInput(attrs={'value': 1}),
      'cores': forms.NumberInput(attrs={'value': 1}),
      'swap': forms.NumberInput(attrs={'value': 1}),
      'disk': forms.NumberInput(attrs={'value': 1}),
    }
