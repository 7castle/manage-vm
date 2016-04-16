from django.shortcuts import render, redirect
from .forms import *
from proxmoxer import ProxmoxAPI
from managevm import secrets
from .models import *
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import ldap

def index(request):
    return render(request, 'index.html')

def manage(request):
    machines = VM.objects.all()
    return render(request,'manage.html',{'machines': machines})

def machine(request, machine_name):
    machine = get_object_or_404(VM, name=machine_name) 
    return render(request,'machine.html',{'machine': machine})

def check_limits(memory, cores, size):
    limits = VM_Limits.objects.get(id=1)
    return memory > limits.memory or cores > limits.cores or size > limits.disk_size

def create_vm(request):
    vm_form = VM_Form(data=request.POST or None)
    drive_form = CD_DVD(data=request.POST or None)
    disk_form = Disk(data=request.POST or None)
    cpu_form = CPU(data=request.POST or None)
    net_form = Network(data=request.POST or None)
    
    if request.method == 'POST':
        if vm_form.is_valid() and drive_form.is_valid() and disk_form.is_valid() and cpu_form.is_valid() and net_form.is_valid():
            
            if '_request' in request.POST:
                # Request VM
                print('VM REQUEST')
                request_vm(vm_form, drive_form, disk_form, cpu_form, net_form)

            if check_limits(vm_form.cleaned_data['memory'],cpu_form.cleaned_data['cores'],disk_form.cleaned_data['size']):
                return render(request, 'create.html',{'vm_form': vm_form,'drive_form': drive_form,'disk_form': disk_form,'cpu_form': cpu_form,'net_form': net_form,'request_vm': True})

            proxmox = ProxmoxAPI(secrets.PROXMOX_HOST,user=secrets.PROXMOX_USER,password=secrets.PROXMOX_PASS,verify_ssl=False)

            node = proxmox.nodes(vm_form.cleaned_data['node'])
            vm_id = int(proxmox.cluster.nextid.get())
            testdata = node.qemu.create(vmid=vm_id,
                        name=vm_form.cleaned_data['name'],
                        ostype=vm_form.cleaned_data['ostype'],
                        ide2=drive_form.cleaned_data['iso']+',media=cdrom',
                        ide0='ceph_pool:'+str(disk_form.cleaned_data['size'])+',format='+disk_form.cleaned_data['disk_format'],
                        sockets=1,
                        cores=cpu_form.cleaned_data['cores'],
                        numa=0,
                        pool=secrets.PROXMOX_POOL,
                        memory=vm_form.cleaned_data['memory'],
                        net0=net_form.cleaned_data['model']+',bridge='+net_form.cleaned_data['bridge'])
            # Testing
            use = User.objects.get_or_create(username='test')
            vm = VM(user=use[0],vmid=vm_id,name=vm_form.cleaned_data['name'],nodename=vm_form.cleaned_data['node'])
            vm.save()
            return redirect('/manage/') 
    return render(request, 'create.html',{'vm_form': vm_form,'drive_form': drive_form,'disk_form': disk_form,'cpu_form': cpu_form,'net_form': net_form})

def request_vm(vm, drive, disk, cpu, net):
    ldap_conn = ldap.initialize(secrets.LDAP_SERVER)
    ldap_conn.simple_bind_s(secrets.LDAP_USER, secrets.LDAP_PASS)

