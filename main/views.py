from django.shortcuts import render
from .forms import *

def index(request):
  return render(request, 'index.html')

def manage(request):
  return render(request,'manage.html')

def create_vm(request):
  if request.method == 'POST':
    vm_form = VM_Form(data=request.POST)

    if vm_form.is_valid():

      vm = vm_form.save(commit=False)
      vm.user = request.user
      vm.save()
  else:
    vm_form = VM_Form()
  
  return render(request, 'create.html',{'vm_form': vm_form,})
