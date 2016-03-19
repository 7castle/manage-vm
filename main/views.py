from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def create_vm(request):
  return render(request, 'create.html')
