from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from .forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
import csv


def create_csv(file_name):
    file_name = str(file_name) + '.csv'
    with open(file_name, "w") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(['name', 'age'])



@login_required
def schemas(request):
    schemes = Schema.objects.all()
    context = {'schemes': schemes}
    return render(request, 'schemas.html', context)


def new_schema(request):
    if request.method == 'POST':
        file_name = request.POST.get('fileName')
        column_separator = request.POST.get('columnSeparator')
        string_character = request.POST.get('stringCharacter')
        # Get the list of schema columns from the POST data
        schema_columns = []
        data = request.POST.items()
        arr = []
        for key, value in data:
            id_key = str(key).split('row')[-1].split('-')[0]  # find row id
            try:
                id_key = int(id_key)
            except:
                continue

            fild = [id_key, value]
            arr.append(fild)

        collection = []
        box = []

        for i in range(0, len(arr)):
            box.append(arr[i][1])
            try:
                if arr[i][0] != arr[i+1][0]:
                    collection.append(box)
                    box = []
            except IndexError:
                collection.append(box)

        print(collection)
        # Convert last element to int
        for subarr in collection:
            subarr[-1] = int(subarr[-1])

        # Bubble sort based on last element
        n = len(collection)
        for i in range(n):
            for j in range(n - i - 1):
                if collection[j][-1] > collection[j + 1][-1]:
                    collection[j], collection[j + 1] = collection[j + 1], collection[j]

        print(collection)
        # Save the schema to the database or do something else with it
        # Return a JSON response with a success message
        return JsonResponse({'message': 'Schema submitted successfully.'})
    else:
        return render(request, 'new_schema.html')




def generate_users(request):
    count = request.GET.get('count')
    print(count)
    html = ''
    for user in range(int(count)):
        html += '<div>{}</div>'.format(user)

    # Return generated users as HTML response
    return HttpResponse('Wait, we are creating CSV files')


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
