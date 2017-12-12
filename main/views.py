# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import RegisterForm, AddRequestForm
from .models import API, Request
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .tasks import run_command


def home(request):
    user_apis = []
    user_groups = ['guest'] + list(request.user.groups.all().values_list('name', flat=True)) # Each user is at least in the guest group. If the user is in other groups too, we append them to the list
    all_apis = API.objects.all()
    for api in all_apis:
        authorized_groups = str(api.authorized_groups).replace(' ', '').split(',')
        if len(set(user_groups).intersection(set(authorized_groups))) > 0:
            user_apis.append(api)

    if request.method == 'POST':
        form = AddRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.api_id = API.objects.get(pk=request.POST.get('api-select'))
            req.owner = request.user
            req.status = 'processing'
            req.save()

            serialized_request = {
                'id': req.id,
                'command': req.api_id.command,
                'input_params': req.input_params,
                'output_files': req.api_id.output_files
            }
            run_command.delay(serialized_request)

            return redirect('requests')

    else:
        form = AddRequestForm()

    return render(request, 'main/home.html', {'apis': user_apis, 'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})


@login_required
def requests(request):
    return render(request, 'main/requests.html')


def ajaxGetRequests(request):
    response = []
    if request.user.id:
        reqs = Request.objects.filter(owner=request.user)
        for req in reqs:
            response.append({
                'request_id': req.id,
                'api_name': req.api_id.name,
                'input_params': req.input_params,
                'date_added': req.date_added,
                'status': dict(Request.REQUEST_STATUS)[req.status]
            })

    return JsonResponse(response, safe=False)