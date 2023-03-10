from django.urls import path
from . import views

urlpatterns = [
    path("", views.schemas, name='schemas'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('new-schema/', views.new_schema, name='new_schema'),
    path('generate_csv/<int:schema_id>/', views.generate_csv, name='generate_csv'),
    path('generate_csv_post/<int:schema_id>/', views.generate_csv_post, name='generate_csv_post'),
    path('download-file/<int:file_id>/', views.download_file, name='download-file'),
]
