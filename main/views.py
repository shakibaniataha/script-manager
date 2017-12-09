# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import RegisterForm, AddRequestForm
from .models import API


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

        # To be continued...

    return render(request, 'main/home.html', {'apis': user_apis})


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