# Project ScriptManager
[project description ...]
### Project flow
...

Each new user is considered 'guest' by default after registration. Later the admin decides which group to add the new user to. 

Any logged-in individual can only see the APIs that his group has access to, plus the APIs which are assigned to the 'guest' group

By default all your scripts should be in the 'bash_scripts' directory. If you want to change it, just make sure you change the SCRIPTS_DIR variable in the settings.py accordingly.

...


### Important Note: celery as daemon
Make sure you have celery service running on your server. 
in order to do this, follow this instruction:

In production we can use supervisord to start Celery workers and make sure they are restarted in case of a system reboot or crash. Installation of Supervisor is simple:
(for ubuntu server)
```bash
$ sudo apt install supervisor
```
When Supervisor is installed you can give it programs to start and watch by creating configuration files in the /etc/supervisor/conf.d directory. For our ScriptManager worker we’ll create a file named /etc/supervisor/conf.d/script_manager.conf with this content:
(make sure you change it according to your own settings)
```bash
[program:ScriptManager]
command=/home/aban/.virtualenvs/script-manager/bin/celery --app=ScriptManager.celery:app worker --loglevel=INFO
directory=/home/aban/PycharmProjects/ScriptManager
user=aban
numprocs=1
stdout_logfile=/home/aban/PycharmProjects/ScriptManager/logs/celery-worker.log
stderr_logfile=/home/aban/PycharmProjects/ScriptManager/logs/celery-worker.log
autostart=true
autorestart=true
startsecs=10

; Need to wait for currently executing tasks to finish at shutdown.
; Increase this if you have very long running tasks.
stopwaitsecs = 600

; When resorting to send SIGKILL to the program to terminate it
; send SIGKILL to its whole process group instead,
; taking care of its children as well.
killasgroup=true

; if rabbitmq is supervised, set its priority higher
; so it starts first
priority=998

```

Now create the log folder and log file (which we specified in the config file above)

Then do the following:

```bash
$ sudo supervisorctl reread
ScriptManager: available
$ sudo supervisorctl update
ScriptManager: added process group 
```

Now you can do:

```bash
$ sudo supervisorctl [status | start | stop | restart] ScriptManager 
```
## !!! Very important note !!!:
Make sure you have only ONE celery daemon running on your server or your tasks will be spread amongst the running daemons and you will lose some of them!!!
In order to see how many daemons are running, run ```$ sudo supervisorctl status```. You should see only one daemon with the status RUNNING.
## Monitoring celery queues
Using "Flower" package you can easily monitor your celery queues and do other useful things. 
In order to install and use flower, follow this procedure:

```bash
$ pip install flower
```

Now launch it:
```bash
$ flower -A ScriptManager --port=5555
```

Now open "localhost:5555" and enjoy :D

## Automatically restarting celery after each change
When you change your files, especially tasks.py, you must restart celery (or the daemon) for the changes to take effect. In order to do that you can use "watchdog". For that, do the following:

```bash
$ sudo apt install libyaml-dev
$ pip install watchdog
```
Now we must change the 'command' line of our script_manager daemon (script_manager.conf) to this:

```bash
command=/home/aban/.virtualenvs/script-manager/bin/watchmedo auto-restart -p '*.py' -d main/ -- /home/aban/.virtualenvs/script-manager/bin/celery --app=ScriptManager.celery:app worker --loglevel=INFO
```
This basically tells watchdog that if any changes happen to any '*.py' file in the 'main' folder (which includes tasks.py) of our ScriptManager project, it must restart celery.

Now again we must reread and update supervisorctl:

```bash
$ sudo supervisorctl reread
$ sudo supervisorctl update
```
And now you are good to go!