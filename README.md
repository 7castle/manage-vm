# manage-vm [![Build Status](https://travis-ci.org/zujko/manage-vm.svg?branch=master)](https://travis-ci.org/zujko/manage-vm)
A simple web app which uses Proxmox to manage virtual machines. 

## Running
In the managevm directory, copy secrets.py.template to secrets.py, and replace all variables with your information. 

Install requirements

```pip install -r requirements```

Run migrations

```python manage.py migrate```

Run server

```python manage.py runserver```
