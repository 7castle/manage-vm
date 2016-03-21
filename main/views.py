from django.shortcuts import render
from .forms import *
from .models import *

def index(request):
  return render(request, 'index.html')

def manage(request):
  machines = VM.objects.all()
  return render(request,'manage.html',{'machines': machines})

def machine(request, machine_name):
  return render(request,'machine.html')

def create_vm(request):
  if request.method == 'POST':
    vm_form = VM_Form(data=request.POST)
    disk_form = Disk_Form(data=request.POST)

    if vm_form.is_valid() and disk_form.is_valid():
      disk = disk_form.save(commit=False)
      disk.storage_domain = ''
      disk.status = None
      disk.interface = ''
      disk.save()
      
      nic = NIC()
      nic.name = ''
      nic.network = ''
      nic.interface = ''
      nic.save()

      vm = vm_form.save(commit=False)
      vm.user = request.user
      vm.cluster = ''
      vm.disk = disk
      vm.nic = nic
      vm.save()
      print('Success')
  else:
    vm_form = VM_Form()
    disk_form = Disk_Form()
  
  return render(request, 'create.html',{'vm_form': vm_form, 'disk_form': disk_form})
