from datetime import datetime
from django.db import models
from django.utils import timezone

class Projet(models.Model):
    name = models.TextField() 
    description = models.TextField() 
    status = models.IntegerField() 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name

class Tache(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, default=None, null=True)  
    name = models.TextField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('en_cours', 'En Cours'), ('complet', 'Complet')])
    deadline = models.DateTimeField()
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Employees(models.Model):
    code = models.CharField(max_length=100,blank=True) 
    firstname = models.TextField() 
    middlename = models.TextField(blank=True,null= True) 
    lastname = models.TextField() 
    gender = models.TextField(blank=True,null= True) 
    dob = models.DateField(blank=True,null= True) 
    contact = models.TextField() 
    address = models.TextField() 
    email = models.TextField() 
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, default=None, null=True)
    date_hired = models.DateField() 
    salary = models.FloatField(default=0) 
    status = models.IntegerField() 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 
    def __str__(self):
        return self.firstname + ' ' +self.middlename + ' '+self.lastname + ' '

class Performance(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
    tache_effectue = models.IntegerField(default=0)



#class Performance(models.Model):
 #   projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
  #  employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
   # tache_id = models.ForeignKey(Tache, on_delete=models.CASCADE)
    #tache_field = models.ForeignKey(Tache, on_delete=models.CASCADE, related_name='performances', default=None)


    #def calculate_completed_tasks_before_deadline(self):
     #   return self.employee.tasks.filter(completed=True, deadline__lt=self.projet.deadline).count()

    #@property
    #def tache_effectue(self):
     #   return self.calculate_completed_tasks_before_deadline()

    #def save(self, *args, **kwargs):
     #   self.tache_effectue = self.calculate_completed_tasks_before_deadline()
      #  super().save(*args, **kwargs)

    #def __str__(self):
     #   return f"Performance: {self.employee.firstname} {self.employee.lastname} | Project: {self.projet.name} | Tasks Completed: {self.tache_effectue}"





#class Performance(models.Model):
 #   employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
  #  tache = models.ForeignKey(Tache, on_delete=models.CASCADE)
   # tache_effectue = models.BooleanField(default=False)
