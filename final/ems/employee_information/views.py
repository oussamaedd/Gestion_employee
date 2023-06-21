from django.shortcuts import redirect, render
from django.http import HttpResponse
from employee_information.models import Projet, Tache, Employees,Performance
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
# Login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

#Logout
def logoutuser(request):
    logout(request)
    return redirect('/')

@login_required
def home(request):
    context = {
        'page_title':'Home',
        'employees':employees,
        'total_projet':len(Projet.objects.all()),
        'total_tache':len(Tache.objects.all()),
        'total_employee':len(Employees.objects.all()),
        'total_performance':len(Performance.objects.all()),
    }
    return render(request, 'employee_information/home.html',context)


def about(request):
    context = {
        'page_title':'About',
    }
    return render(request, 'employee_information/about.html',context)

# projets
@login_required
def projets(request):
    projet_list = Projet.objects.all()
    context = {
        'page_title':'Projets',
        'projets':projet_list,
    }
    return render(request, 'employee_information/projets.html',context)
@login_required
def manage_projets(request):
    projet = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            projet = Projet.objects.filter(id=id).first()
    
    context = {
        'projet' : projet
    }
    return render(request, 'employee_information/manage_projet.html',context)

@login_required
def save_projet(request):
    data =  request.POST
    resp = {'status':'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            save_projet = Projet.objects.filter(id = data['id']).update(name=data['name'], description = data['description'],status = data['status'])
        else:
            save_projet = Projet(name=data['name'], description = data['description'],status = data['status'])
            save_projet.save()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_projet(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Projet.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Taches
# views.py

@login_required
def taches(request):
    tache_list = Tache.objects.all()
    context = {
        'page_title': 'Taches',
        'taches': tache_list,
    }
    return render(request, 'employee_information/taches.html', context)


@login_required
def manage_taches(request):
    tache = {}
    projets = Projet.objects.all()  # Fetch all Projets
    if request.method == 'GET':
        data = request.GET
        tache_id = data.get('id', '')
        if tache_id.isnumeric() and int(tache_id) > 0:
            try:
                tache = Tache.objects.get(id=tache_id)
            except Tache.DoesNotExist:
                pass

    context = {
        'tache': tache,
        'projets': projets,  # Pass Projets to the template
    }
    return render(request, 'employee_information/manage_tache.html', context)

import logging

@login_required

def save_tache(request):
    if request.method == 'POST':
        tache_id = request.POST.get('tache-id')
        name = request.POST.get('name')
        description = request.POST.get('description')
        status = request.POST.get('status')
        deadline = request.POST.get('deadline')
        projet_id = request.POST.get('projet')

        if tache_id:
            tache = get_object_or_404(Tache, id=tache_id)
        else:
            tache = Tache()

        tache.name = name
        tache.description = description
        tache.status = status
        tache.deadline = deadline
        tache.projet = get_object_or_404(Projet, id=projet_id)

        tache.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


@login_required
def update_tache(request, tache_id):
    try:
        tache = Tache.objects.get(id=tache_id)
    except Tache.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Tache not found.'})
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        status = request.POST.get('status')
        deadline = request.POST.get('deadline')
        
        tache.name = name
        tache.description = description
        tache.status = status
        tache.deadline = deadline
        tache.save()
        
        return JsonResponse({'status': 'success'})
    
    context = {
        'tache': tache
    }
    return render(request, 'employee_information/manage_tache.html', context)


@login_required
def delete_tache(request):
    data = request.POST
    resp = {'status': ''}
    try:
        tache_id = data.get('id', '')
        if tache_id.isnumeric() and int(tache_id) > 0:
            try:
                Tache.objects.filter(id=tache_id).delete()
                resp['status'] = 'success'
            except Exception as e:
                logging.error(str(e))
                resp['error'] = 'An error occurred while deleting tache.'
        else:
            resp['error'] = 'Invalid tache ID.'
    except Exception as e:
        logging.error(str(e))
        resp['error'] = 'An error occurred while deleting tache.'

    return HttpResponse(json.dumps(resp), content_type="application/json")

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Employees, Projet
import json


@login_required
def employees(request):
    employee_list = Employees.objects.all()
    context = {
        'page_title': 'Employees',
        'employees': employee_list,
    }
    return render(request, 'employee_information/employees.html', context)


@login_required
def manage_employees(request):
    employee = {}
    projets = Projet.objects.filter(status=1).all()
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            employee = Employees.objects.filter(id=id).first()
    context = {
        'employee': employee,
        'projets': projets,
    }
    return render(request, 'employee_information/manage_employee.html', context)


@login_required
def view_employee(request):
    employee = {}
    projets = Projet.objects.filter(status=1).all()

    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            employee = Employees.objects.filter(id=id).first()
    context = {
        'employee': employee,
        'projets': projets,
    }
    return render(request, 'employee_information/view_employee.html', context)


@csrf_exempt
@login_required
def save_employee(request):
    data = request.POST
    resp = {'status': 'failed'}

    if data['id'].isnumeric() and int(data['id']) > 0:
        check = Employees.objects.exclude(id=data['id']).filter(code=data['code'])
    else:
        check = Employees.objects.filter(code=data['code'])

    if len(check) > 0:
        resp['status'] = 'failed'
        resp['msg'] = 'Code Already Exists'
    else:
        try:
            if data['id'].isnumeric() and int(data['id']) > 0:
                save_employee = Employees.objects.filter(id=data['id']).update(
                    code=data['code'],
                    firstname=data['firstname'],
                    middlename=data['middlename'],
                    lastname=data['lastname'],
                    dob=data['dob'],
                    gender=data['gender'],
                    contact=data['contact'],
                    email=data['email'],
                    address=data['address'],
                    projet_id=data['projet_id'],  # Use the project name directly
                    date_hired=data['date_hired'],
                    salary=data['salary'],
                    status=data['status']
                )
            else:
                save_employee = Employees(
                    code=data['code'],
                    firstname=data['firstname'],
                    middlename=data['middlename'],
                    lastname=data['lastname'],
                    dob=data['dob'],
                    gender=data['gender'],
                    contact=data['contact'],
                    email=data['email'],
                    address=data['address'],
                    projet_id=data['projet_id'],  # Use the project name directly
                    date_hired=data['date_hired'],
                    salary=data['salary'],
                    status=data['status']
                )
                save_employee.save()

            resp['status'] = 'success'
        except Exception as e:
            resp['status'] = 'failed'
            error_message = str(e)  # Get the error message
            resp['msg'] = 'An error occurred: ' + error_message
            return HttpResponse(json.dumps(resp), content_type="application/json")

    return HttpResponse(json.dumps(resp), content_type="application/json")


@csrf_exempt
@login_required
def delete_employee(request):
    data = request.POST
    resp = {'status': ''}
    try:
        Employees.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")
'''''''''''''''''''''
@login_required
def performance(request):
    performance_list = Performance.objects.all()
    context ={
        'page_title':'Performances',
        'Performances':performance_list,
    }    
    return render(request, 'employee_information/performance.html', context)
'''''''''''''''
from django.db.models import Count, Q

def update_performance(request):
    data = {'message': 'Performance table updated successfully'}
    return JsonResponse(data)

@login_required
def performance(request):
    # Fetch all performances
    performances = Performance.objects.all()

    # Iterate over each performance
    for performance in performances:
        code = performance.employee.code

        # Find the projects associated with the employee's tasks
        projects = Tache.objects.filter(Q(projet__employee__code=code) | Q(projet__employee__code__isnull=True))

        # Count the number of completed tasks for each project
        completed_tasks = Performance.objects.filter(
            employee__code=code,
            tache__projet__in=projects,
            tache__status='complet'
        ).values('tache__projet').annotate(nmbr_tache_effectue=Count('tache')).values('nmbr_tache_effectue')

        # Get the total number of completed tasks for all projects
        total_completed_tasks = sum(item['nmbr_tache_effectue'] for item in completed_tasks)

        # Update the tache_effectue field with the total number of completed tasks
        performance.tache_effectue = total_completed_tasks
        performance.save()

    context = {
        'page_title': 'Performances',
        'performances': performances,
    }
    return render(request, 'employee_information/performance.html', context)
