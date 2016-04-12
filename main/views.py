from django.shortcuts import render
from .forms import *
from proxmoxer import ProxmoxAPI
from managevm import secrets
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

def create_vm(request):
    vm_form = VM_Form(data=request.POST or None)
    drive_form = CD_DVD(data=request.POST or None)
    disk_form = Disk(data=request.POST or None)
    cpu_form = CPU(data=request.POST or None)
    net_form = Network(data=request.POST or None)

    if request.method == 'POST':
        if vm_form.is_valid() and drive_form.is_valid() and disk_form.is_valid() and cpu_form.is_valid() and net_form.is_valid():
        
            proxmox = ProxmoxAPI(secrets.PROXMOX_HOST,user=secrets.PROXMOX_USER,password=secrets.PROXMOX_PASS,verify_ssl=False)

            node = proxmox.nodes(vm_form.cleaned_data['node'])
        
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
  
    return render(request, 'create.html',{'vm_form': vm_form,'drive_form': drive_form,'disk_form': disk_form,'cpu_form': cpu_form,'net_form': net_form})
