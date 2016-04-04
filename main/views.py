from django.shortcuts import render
from .forms import *
from proxmoxer import ProxmoxAPI
from managevm import secrets

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

      proxmox = ProxmoxAPI(secrets.PROXMOX_HOST,user=secrets.PROXMOX_USER,password=secrets.PROXMOX_PASS,verify_ssl=True)

      node = proxmox.nodes('test_node')

      # [TESTING] Create openvz container 
      node.openvz.create(vmid=202,
                        hostname=vm_form.cleaned_data['hostname'],
                        storage='local',
                        memory=vm_form.cleaned_data['memory'],
                        swap=vm_form.cleaned_data['swap'],
                        cpus=vm_form.cleaned_data['cores'],
                        disk=vm_form.cleaned_data['disk'],
                        password=secrets.PROXMOX_PASS,
                        ip_address='0.0.0.0')

  else:
    vm_form = VM_Form()
  
  return render(request, 'create.html',{'vm_form': vm_form,})
