from __future__ import absolute_import
from celery import shared_task
from ScriptManager import settings
from subprocess import PIPE, Popen

@shared_task
def run_command(jsonified_request):
    request_id = jsonified_request['id']
    command = jsonified_request['command']
    input_params = jsonified_request['input_params']
    output_files = jsonified_request['output_files']

    command_list = []
    command_list.append(settings.SCRIPTS_DIR + command)
    command_list += input_params.strip(' ').split(',')
    stdout, stderr = Popen(command_list, stdout=PIPE, stderr=PIPE).communicate()