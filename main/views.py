from django.shortcuts import render, redirect
from .forms import *
from proxmoxer import ProxmoxAPI
from managevm import secrets
from .models import *
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
import datetime
import ldap

def index(request):
    return render(request, 'index.html')

def manage(request):
    machines = VM.objects.all()
    return render(request,'manage.html',{'machines': machines})

def machine(request, machine_name):
    machine = get_object_or_404(VM, name=machine_name) 
    return render(request,'machine.html',{'machine': machine})

def admin_machines(request):
    machines = VM.objects.all()
    return render(request,'manage.html',{'machines': machines})

def requests(request):
    machines = VM_Request.objects.all()
    return render(request,'requests.html',{'machines': machines})

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
                use = User.objects.get_or_create(username='test')
                request_vm(vm_form, drive_form, disk_form, cpu_form, net_form,use[0])
                return redirect('/')

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

def request_vm(vm, drive, disk, cpu, net, use):
    request = VM_Request(user = use,
                        node = vm.cleaned_data['node'],
                        name=vm.cleaned_data['name'],
                        ostype = vm.cleaned_data['ostype'],
                        iso = drive.cleaned_data['iso'],
                        size = disk.cleaned_data['size'],
                        disk_format = disk.cleaned_data['disk_format'],
                        cores = cpu.cleaned_data['cores'],
                        memory = vm.cleaned_data['memory'],
                        net_model = net.cleaned_data['model'],
                        bridge = net.cleaned_data['bridge'],
                        request_time=datetime.datetime.now())
    request.save()

    #ldap_conn = ldap.initialize(secrets.LDAP_SERVER)
    #ldap_conn.simple_bind_s('uid='+secrets.LDAP_USER+'ou=Users,dc=csh,dc=rit,dc=edu', secrets.LDAP_PASS)
    #emails = get_rtp_email(ldap_conn)
    # is_staff will denote if they want email alerts
    rtps = User.objects.filter(is_superuser=True,is_staff=True)
    emails = ['peter7661211@gmail.com']
    for rtp in rtps:
        emails.append(rtp.email)

    send_mail('Virtual Machine Request '+vm.cleaned_data['name'],
            use.username+' requests a virtual machine with the following resources\n'+'Disk Size(GB): '+str(disk.cleaned_data['size'])+'\nMemory (MB): '+str(vm.cleaned_data['memory'])+'\nCores: '+str(cpu.cleaned_data['cores'])+'\nName: '+vm.cleaned_data['name']+'\nNode: '+vm.cleaned_data['node']+'\nOS Type: '+vm.cleaned_data['ostype']+'\nISO: '+drive.cleaned_data['iso'],'cshmanagevm@gmail.com',emails)

def get_rtp_email(ldap_c):
    members = ldap_c.search_s(group,ldap.SCOPE_SUBTREE,'cn=rtp')

    if len(members) == 0:
        return members
    else:
        member_dns = members[0][1]['member']
        members = []
        for member_dn in member_dns:
            members.append(ldap_c.search_s(member_dn.decode("utf-8"),ldap.SCOPE_SUBTREE))

        emails = []
        for member in members:
            emails.append(member[0][1]['mail'][0].decode("utf-8"))
        return emails
