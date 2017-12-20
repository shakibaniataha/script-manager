from __future__ import absolute_import
from celery import shared_task
from ScriptManager import settings
from subprocess import PIPE, Popen
import os, errno
from shutil import copyfile
from .models import Request


@shared_task
def run_command(jsonified_request):
    request_id = jsonified_request['id']
    command = jsonified_request['command']
    input_params = jsonified_request['input_params']

    working_dir = settings.WORKING_DIR + str(request_id) + '/'
    mkdir_p(working_dir)
    cwd = os.path.realpath(working_dir) + '/'

    # If the command is a file name, we must copy that file into our working directory so that
    # we can execute it from there.
    temp = settings.SCRIPTS_DIR + command
    if os.path.isfile(temp):
        command = cwd + command
        copyfile(temp, command)
        os.chmod(command, 0555)

    command_list = []
    command_list.append(command)
    command_list += input_params.strip(' ').split(',')
    stdout, stderr = Popen(command_list, stdout=PIPE, stderr=PIPE, cwd=cwd).communicate()

    out_file = open(cwd + 'std.out', 'w')
    err_file = open(cwd + 'std.err', 'w')
    out_file.write(stdout)
    err_file.write(stderr)
    out_file.close()
    err_file.close()

    if os.path.isfile(command):
        os.remove(command)

    # Updating request status from processing to finished
    request = Request.objects.get(pk=request_id)
    request.status = 'finished'
    request.save()


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise