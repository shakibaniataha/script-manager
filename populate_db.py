import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ScriptManager.settings')

import django
django.setup()

from django.contrib.auth.models import User, Group
from main.models import API, Request


def populate():
    pass


def add_user(username, password):
    user = User.objects.create_user(username, password=password)
    user.save()

    return user


def add_group(name):
    group = Group.objects.get_or_create(name=name)[0]
    group.save()

    return group


def add_user_group(group, user):
    user_group = group.user_set.add(user)
    user_group.save()

    return user_group


def add_api():
    pass


def add_request():
    pass


if __name__ == '__main__':
    print('Populating ScriptManager Database with sample data...')
    populate()