from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from .forms import UserLoginForm
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'index.html')


def create_schema(request):
    selected_fields = []
    if request.method == 'GET':
        if 'fullName' in request.GET:
            selected_fields.append('fullName')
        if 'job' in request.GET:
            selected_fields.append('job')
        if 'email' in request.GET:
            selected_fields.append('email')
        if 'domainName' in request.GET:
            selected_fields.append('domainName')
        if 'phoneNumber' in request.GET:
            selected_fields.append('phoneNumber')
        if 'companyName' in request.GET:
            selected_fields.append('companyName')
        if 'text' in request.GET:
            selected_fields.append('text')
        if 'integer' in request.GET:
            selected_fields.append('integer')
        if 'date' in request.GET:
            selected_fields.append('date')

        # Code to create schema using selected_fields goes here
        print(selected_fields)
        return HttpResponse('The scheme has been successfully created')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('/login')
