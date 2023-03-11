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
from django.views.decorators.http import require_POST


def data_generator(arr, faker):
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
    faker = Faker()
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
                text = data_generator(box, faker)
                info_for_table.append(text)

            writer.writerow(info_for_table)

    return file_path


@login_required
def download_file(request, file_id):
    file_obj = File.objects.get(id=file_id)
    file_path = file_obj.file.path
    file_name = file_obj.name

    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
        return response


@login_required
def schemas(request):
    schemes = Schema.objects.all()
    context = {'schemes': schemes}
    return render(request, 'schemas.html', context)


@login_required
def new_schema(request):
    if request.method == 'POST':
        data = request.POST.items()
        arr = []

        # Extract row ID and value from each field in the request
        for key, value in data:
            id_key = str(key).split('row')[-1].split('-')[0]  # find row id

            # If row ID can't be converted to int, skip this field
            if not id_key.isdigit():
                continue

            id_key = int(id_key)
            field = [id_key, value]
            arr.append(field)

        collection = []
        box = []

        # Group values by row ID
        for i in range(len(arr)):
            box.append(arr[i][1])

            # If next tuple has different row ID or this is the last tuple, add current box to collection
            if i == len(arr) - 1 or arr[i][0] != arr[i + 1][0]:
                collection.append(box)
                box = []

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
    files = File.objects.filter(schema_id=schema_id).all()

    context = {
        'files': files,
        'current_schema': current_schema,
        'current_columns': current_columns
    }
    return render(request, 'generate_csv.html', context)


@login_required
@require_POST
def generate_csv_post(request, schema_id):
    current_columns = Column.objects.filter(schema_id=schema_id).all()
    current_schema = Schema.objects.get(pk=schema_id)
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
    csv_name = os.path.split(file_path)[-1]
    csv = File.objects.create(path=file_path, schema=current_schema, file=file_path, name=csv_name)

    response_data = {
        'file_id': csv.id,
        'file_path': csv.file.url,
        'csv_name': csv_name,
        'created_at': csv.created
    }

    return JsonResponse(response_data)


@login_required
def delete_schema(request, schema_id):
    schema = Schema.objects.get(id=schema_id)
    schema.delete()
    return redirect('schemas')


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
