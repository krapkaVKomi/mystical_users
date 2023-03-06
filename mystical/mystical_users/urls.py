from django.urls import path
from . import views

urlpatterns = [
    #path("", views.index, name='index'),
    path("", views.schemas, name='schemas'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create-schema/', views.create_schema, name='create_schema'),
    path('new-schema/', views.new_schema, name='new_schema'),
    path('generate-users/', views.generate_users, name='generate-users'),
]