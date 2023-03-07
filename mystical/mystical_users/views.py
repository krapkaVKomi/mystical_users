from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from .forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse

@login_required
def schemas(request):
    schemes = Schema.objects.all()
    context = {'schemes': schemes}
    return render(request, 'schemas.html', context)


def new_schema(request):
    if request.method == 'POST':
        file_name = request.POST.get('fileName')
        print(file_name)
        column_separator = request.POST.get('columnSeparator')
        string_character = request.POST.get('stringCharacter')
        print(column_separator, string_character)
        # Get the list of schema columns from the POST data
        schema_columns = []
        print(request.POST.items)
        for key, value in request.POST.items():
            if key.startswith('row'):
                column_name = request.POST.get(f'{key}-columnName')
                data_type = request.POST.get(f'{key}-type')
                order = request.POST.get(f'{key}-order')
                # Get the integer field values if the data type is Integer
                if data_type == 'Integer':
                    start = request.POST.get(f'{key}-start')
                    end = request.POST.get(f'{key}-end')
                    schema_columns.append({
                        'column_name': column_name,
                        'data_type': data_type,
                        'order': order,
                        'start': start,
                        'end': end
                    })
                else:
                    schema_columns.append({
                        'column_name': column_name,
                        'data_type': data_type,
                        'order': order
                    })
        for i in schema_columns:
            print(i)
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
