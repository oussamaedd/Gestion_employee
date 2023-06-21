from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('', views.home, name="home-page"),
    path('login', auth_views.LoginView.as_view(template_name = 'employee_information/login.html',redirect_authenticated_user=True), name="login"),
    path('userlogin', views.login_user, name="login-user"),
    path('logout', views.logoutuser, name="logout"),
    path('about', views.about, name="about-page"),
    path('Projets', views.projets, name="projet-page"),
    path('manage_projets', views.manage_projets, name="manage_projets-page"),
    path('save_projet', views.save_projet, name="save-projet-page"),
    path('delete_projet', views.delete_projet, name="delete-projet"),
    path('taches/', views.taches, name="tache-page"),
    path('manage_taches/', views.manage_taches, name="manage_taches-page"),
    path('save_tache/', views.save_tache, name='save_tache'),
    path('delete_tache/', views.delete_tache, name="delete-tache"),
    path('update_tache/', views.update_tache, name="update-tache"),
    path('update_tache/<int:tache_id>/', views.update_tache, name='update_tache'),
    path('delete_tache/<int:tache_id>/', views.delete_tache, name='delete_tache'),
    path('employees', views.employees, name="employee-page"),
    path('manage_employees', views.manage_employees, name="manage_employees-page"),
    path('save_employee', views.save_employee, name="save-employee-page"),
    path('delete_employee', views.delete_employee, name="delete-employee"),
    path('view_employee', views.view_employee, name="view-employee-page"),
    path('performance', views.performance, name='performance-page'),
    path('update_performance/', views.update_performance, name='update_performance'),

]