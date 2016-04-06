from django import forms
from .models import *
from proxmoxer import ProxmoxAPI
from managevm import secrets

OS = (
        ('l26','Linux 4.X/3.X/2.6 Kernel'),
        ('l24','Linux 2.4 Kernel'),
        ('solaris','Solaris Kernel'),
        ('win8','Microsoft Windows 8/10/2012'),
        ('win7','Microsoft Windows 7/2008r2'),
        ('other','Other OS types'),
    )
DISK_FORMAT = (
        ('qcow2','QEMU Image Format'),
        ('raw','Raw Disk Image'),
        ('vmdk','VMware Image Format'),
    )
NET_MODELS = (
        ('e1000','Intel E1000'),
        ('virtio','VirtIO'),
        ('rtl8139','Realtek RTL8139'),
        ('vmxnet3','VMWare vmxnet3'),
    )

class VM_Form(forms.Form):
    node = forms.ChoiceField(label='Node')
    name = forms.CharField(label='Name', max_length=50,widget=forms.TextInput(attrs={'placeholder': 'Name of machine'}))
    ostype = forms.ChoiceField(label='Operating System',choices=OS)
    memory = forms.IntegerField(label='Memory (MB)',min_value=32,max_value=100000,widget=forms.NumberInput(attrs={'value': 4000}))
    
    def __init__(self, *args, **kwargs):
        super(VM_Form, self).__init__(*args, **kwargs)
        proxmox = ProxmoxAPI(secrets.PROXMOX_HOST,user=secrets.PROXMOX_USER,password=secrets.PROXMOX_PASS,verify_ssl=False)
        nodes = []
        for node in proxmox.nodes.get():
            nodes.append(node['node'])

        self.fields['node'] = forms.ChoiceField(choices=[(node,node) for node in nodes])
class CD_DVD(forms.Form):
    storage = forms.ChoiceField(label='Storage')
    iso = forms.ChoiceField(label='ISO Image')
    
    def __init__(self, *args, **kwargs):
        super(CD_DVD, self).__init__(*args,**kwargs)
        storage = []
        isos = []
        proxmox = ProxmoxAPI(secrets.PROXMOX_HOST,user=secrets.PROXMOX_USER,password=secrets.PROXMOX_PASS,verify_ssl=False)
        for stor in proxmox.storage.get():
            storage.append(stor['storage'])
        for node in proxmox.nodes.get():
            for sotr in proxmox.nodes(node['node']).storage.get():
                for item in proxmox.nodes(node['node']).storage(stor['storage']).content.get():
                    if item['content'] == 'iso':
                        isos.append(item['volid'])
        self.fields['storage'] = forms.ChoiceField(choices=[(stor,stor) for stor in storage])
        self.fields['iso'] = forms.ChoiceField(choices=[(iso,iso) for iso in isos])

class Disk(forms.Form):
    storage = forms.ChoiceField(label='Storage')
    size = forms.IntegerField(label='Disk size (GB)',min_value=1,max_value=10000,widget=forms.NumberInput(attrs={'value': 100}))
    disk_format = forms.ChoiceField(label='Format')
    
    def __init__(self, *args, **kwargs):
        super(Disk, self).__init__(*args, **kwargs)
        proxmox = ProxmoxAPI(secrets.PROXMOX_HOST,user=secrets.PROXMOX_USER,password=secrets.PROXMOX_PASS,verify_ssl=False)
        storage = []
        for stor in proxmox.storage.get():
            storage.append(stor['storage'])
        self.fields['storage'] = forms.ChoiceField(choices=[(stor,stor) for stor in storage])
        self.fields['disk_format'] = forms.ChoiceField(choices=DISK_FORMAT)

class CPU(forms.Form):
    cores = forms.IntegerField(label='Cores',min_value=1,max_value=500,widget=forms.NumberInput(attrs={'value': 4}))
    numa = forms.BooleanField(label='Numa',initial=False)

class Network(forms.Form):
    bridge = forms.ChoiceField(label='Bridge')
    model = forms.ChoiceField(label='Model')

    def __init__(self, *args, **kwargs):
        super(Network, self).__init__(*args, **kwargs)
        proxmox = ProxmoxAPI(secrets.PROXMOX_HOST,user=secrets.PROXMOX_USER,password=secrets.PROXMOX_PASS,verify_ssl=False)
        bridges = []
        for node in proxmox.nodes.get():
            for net in proxmox.nodes(node['node']).network.get():
                if net['type'] == 'bridge':
                    bridges.append(net['iface'])
        self.fields['bridge'] = forms.ChoiceField(choices=[(bridge,bridge) for bridge in bridges])
        self.fields['model'] = forms.ChoiceField(choices=NET_MODELS)
