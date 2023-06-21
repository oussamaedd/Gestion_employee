from django.contrib import admin
from employee_information.models import Projet, Tache, Employees,Performance

# Register your models here.
admin.site.register(Projet)
admin.site.register(Tache)
admin.site.register(Employees)
admin.site.register(Performance)

