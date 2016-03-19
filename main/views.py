from django.shortcuts import render
from .forms import *

def index(request):
    return render(request, 'index.html')

def create_vm(request):
  vm_form = VM_Form()
  disk_form = Disk_Form()
  return render(request, 'create.html',{'vm_form': vm_form, 'disk_form': disk_form})
