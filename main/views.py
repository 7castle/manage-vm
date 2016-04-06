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
    drive_form = CD_DVD(data=request.POST)
    disk_form = Disk(data=request.POST)
    cpu_form = CPU(data=request.POST)
    net_form = Network(data=request.POST)

    if vm_form.is_valid() and drive_form.is_valid() and disk_form.is_valid() and cpu_form.is_valid() and net_form.is_valid():
        
        proxmox = ProxmoxAPI(secrets.PROXMOX_HOST,user=secrets.PROXMOX_USER,password=secrets.PROXMOX_PASS,verify_ssl=False)

        node = proxmox.nodes(vm_form.cleaned_data['node'])

      # [TESTING] Create openvz container 
        vm_id = int(proxmox.cluster.nextid.get())
        testdata = node.qemu.create(vmid=vm_id,
                        name=vm_form.cleaned_data['name'],
                        ostype=vm_form.cleaned_data['ostype'],
                        ide2=drive_form.cleaned_data['iso']+',media=cdrom',
                        ide0=disk_form.cleaned_data['storage']+':'+str(disk_form.cleaned_data['size'])+',format='+disk_form.cleaned_data['disk_format'],
                        sockets=1,
                        cores=cpu_form.cleaned_data['cores'],
                        numa=0,
                        memory=vm_form.cleaned_data['memory'],
                        net0=net_form.cleaned_data['model']+',bridge='+net_form.cleaned_data['bridge'])
 
        print(str(testdata))

  else:
    vm_form = VM_Form()
    drive_form = CD_DVD()
    disk_form = Disk()
    cpu_form = CPU()
    net_form = Network()
  
  return render(request, 'create.html',{'vm_form': vm_form,'drive_form': drive_form,'disk_form': disk_form,'cpu_form': cpu_form,'net_form': net_form})
