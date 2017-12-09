import os

from django.db.utils import IntegrityError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ScriptManager.settings')

import django
django.setup()

from django.contrib.auth.models import User, Group
from main.models import API, Request


def populate():
    user0 = add_user('taha', 'taha')
    user1 = add_user('soroush', 'soroush')
    user2 = add_user('anahid', 'anahid')
    user3 = add_user('amin', 'amin')
    user4 = add_user('maryam', 'maryam')
    user5 = add_user('ali', 'ali')
    user6 = add_user('javad', 'javad')
    user7 = add_user('mitra', 'mitra')
    user8 = add_user('farnaz', 'farnaz')
    user9 = add_user('alireza', 'alireza')

    group0 = add_group('abanppc')
    group1 = add_group('tiara')
    group2 = add_group('abanvas')
    group3 = add_group('roozarooz')

    add_user_group(user0, group0)
    add_user_group(user1, group0)
    add_user_group(user2, group0)
    add_user_group(user3, group0)
    add_user_group(user4, group1)
    add_user_group(user5, group1)
    add_user_group(user6, group2)
    add_user_group(user7, group2)
    add_user_group(user8, group3)
    add_user_group(user9, group3)

    test_api = add_api('test', 'test.sh', 'tmp/output', 'This is just a test api', 0, 'guest')
    add_request(test_api, None, '', 'processing')

    # Printing what we have added
    for g in Group.objects.all():
        for u in g.user_set.all():
            print ('Added user "{0}" to group "{1}"'.format(u, g))

    for a in API.objects.all():
        for r in Request.objects.filter(api_id=a):
            print ('Added request "{0}" to API "{1}"'.format(r, a))


def add_user(username, password):
    try:
        user = User.objects.create_user(username, password=password)
        user.save()
    except IntegrityError:
        user = User.objects.get(username__iexact=username)

    return user


def add_group(name):
    group = Group.objects.get_or_create(name=name)[0]
    group.save()

    return group


def add_user_group(user, group):
    group.user_set.add(user)
    group.save()


def add_api(name, command, output_files, description, num_input_params, authorized_groups):
    api = API.objects.get_or_create(name=name)[0]
    api.command = command
    api.output_files = output_files
    api.description = description
    api.num_input_params = num_input_params
    api.authorized_groups = authorized_groups
    api.save()

    return api


def add_request(api, owner, input_params, status):
    request = Request()
    request.owner = owner
    request.api_id = api
    request.input_params = input_params
    request.status = status
    request.save()

    return request


if __name__ == '__main__':
    print('Populating ScriptManager Database with sample data...')
    populate()