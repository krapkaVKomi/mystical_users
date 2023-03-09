from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from .forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import *
from django.http import JsonResponse
from faker import Faker
import random
import csv
import os
import datetime


faker = Faker()


def data_generator(arr):
    data_type = arr[1]
    if data_type == 'Job':
        data = faker.job()

    elif data_type == 'Email':
        data = faker.email()

    elif data_type == 'Name':
        data = faker.name()

    elif data_type == 'Domain name':
        data = faker.domain_name()

    elif data_type == 'Phone number':
        first = str(random.randint(100, 999))
        second = str(random.randint(1, 888)).zfill(3)
        last = (str(random.randint(1, 9998)).zfill(4))
        data = '{}-{}-{}'.format(first, second, last)

    elif data_type == 'Company name':
        data = faker.word().title()

    elif data_type == 'Text':
        data = ''
        for i in range(int(arr[2])):
            paragraph = '   ' + faker.text() + '\n'
            data = data + paragraph

    elif data_type == 'Integer':
        start = int(arr[2])
        end = int(arr[3])
        data = random.randint(start, end)

    elif data_type == 'Date':
        data = faker.date_of_birth()

    else:
        data = ''
    return data


def data_sort(collection, index):
    for subarr in collection:
        subarr[index] = int(subarr[index])

    # Bubble sort based on last element
    n = len(collection)
    for i in range(n):
        for j in range(n - i - 1):
            if collection[j][index] > collection[j + 1][index]:
                collection[j], collection[j + 1] = collection[j + 1], collection[j]

    return collection


def create_csv_file(data, number):
    print(data)
    titles = []
    for element in data:
        titles.append(element[0])

    file_name = str(datetime.datetime.now().date()) \
                + '_' + str(datetime.datetime.now().time()).replace(':', '.')

    # Create the file path for the CSV file
    file_path = os.path.join(settings.MEDIA_ROOT, f'{file_name}.csv')
    # Write the data to the CSV file

    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(titles)
        for rows in range(number):
            info_for_table = []
            for box in data:
                text = data_generator(box)
                info_for_table.append(text)

            writer.writerow(info_for_table)

    return file_path


@login_required
def schemas(request):
    schemes = Schema.objects.all()
    context = {'schemes': schemes}
    return render(request, 'schemas.html', context)


@login_required
def new_schema(request):
    if request.method == 'POST':

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

        file_name = request.POST.get('fileName')
        schema = Schema.objects.create(title=file_name)

        collection = data_sort(collection=collection, index=-1)
        for element in collection:
            name = element[0]
            type = element[1]
            order = element[-1]
            if len(element) == 3:
                column = Column.objects.create(name=name, type=type, order=order, schema=schema)

            elif len(element) == 4:
                number = element[2]
                column = Column.objects.create(name=name, type=type, number=number, order=order, schema=schema)

            else:
                start = element[2]
                end = element[3]
                column = Column.objects.create(name=name, type=type, start=start, end=end, order=order, schema=schema)

        print(column.schema)

        response_data = {
            'success': True,
            'column_schema_pk': column.schema.pk,
        }
        return JsonResponse(response_data)

    else:
        return render(request, 'new_schema.html')


@login_required
def generate_csv(request, schema_id):
    current_columns = Column.objects.filter(schema_id=schema_id).all()
    current_schema = Schema.objects.get(pk=schema_id)

    if request.method == 'POST':
        count = int(request.POST.get('count'))
        collection = []

        for element in current_columns:
            data = []
            data.append(str(element.name))
            data.append(str(element.type))

            if str(element.type) == 'text':
                data.append(str(element.number))

            elif str(element.type) == 'Integer':
                data.append(str(element.start))
                data.append(str(element.end))

            data.append(str(element.order))
            collection.append(data)

        file_path = create_csv_file(data=collection, number=count)

        csv = File.objects.create(path=file_path, schema=current_schema, file=file_path)
        # Generate CSV data here
        data = {'message': 'CSV data generated successfully'}
        return JsonResponse(data)

    else:
        files = File.objects.filter(schema_id=schema_id).all()

        context = {
            'files': files,
            'current_schema': current_schema,
            'current_columns': current_columns
        }
        return render(request, 'generate_csv.html', context)


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
