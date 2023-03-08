from django.urls import path
from . import views

urlpatterns = [
    #path("", views.index, name='index'),
    path("", views.schemas, name='schemas'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('new-schema/', views.new_schema, name='new_schema'),
    path('generate_csv/<int:schema_id>/', views.generate_csv, name='generate_csv'),
]