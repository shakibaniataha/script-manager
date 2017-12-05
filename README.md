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