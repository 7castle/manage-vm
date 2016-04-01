from django.shortcuts import render
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404

def index(request):
  return render(request, 'index.html')

def manage(request):
  machines = VM.objects.all()
  return render(request,'manage.html',{'machines': machines})

def machine(request, machine_name):
    machine = get_object_or_404(VM, hostname=machine_name) 
    return render(request,'machine.html',{'machine': machine})

def admin_machines(request):
    machines = VM.objects.all()
    return render(request,'manage.html',{'machines': machines})

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
