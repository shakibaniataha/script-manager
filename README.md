# Project ScriptManager
This application aims at automating and managing bash-script execution. The main point of it is to enable users to run tasks (bash scripts) that are
pertinent to their group and wait for the process to finish and download the results later. 
### Project flow
There are two main models or notions in this project that need to be explained. The first one is the API model. In this application,
an API is basically an interface to run commands. A command might be a simple shell command like "ls -l" or a reference to an already-made script file.
An API might take some inputs and generate outputs in three different categories: stdout, stderr, and files.
Each API has an "output files" field which describes the name of the files that the bash script creates (not including stdout and stderr).

Each API is only accessible for specific groups of users. But if you add the "guest" group to the authorized groups, then any user can access the API.

The second model is called "Request". A Request is basically a call to an API to run its command with some specific inputs (if any) and provide the results for download. 
The project uses the "celery" module to schedule tasks. When a request is done executing, its results will be available for download. 
These results include the stdout and stderr of the script, plus the output files related to that command.   

If we want to explain the main aspects, we can follow these steps to understand the basic flow of the application:

1- Just like any typical django project, there is a backend panel that an admin logs in, defines an API, assigns some authorized groups to that API and fills other complimentary fields. 

2- Users register in the application.

3- The admin defines groups and assigns users to them in order to give them permission to execute different APIs.

4- Now each user can browse the APIs that they are allowed to see and can execute them and download the results later.
There is a page called "My Requests" for users in order to manage their Requests.  

<b>Note: </b>Each new user is considered 'guest' by default after registration. Later the admin decides which group to add the new user to. 

Any logged-in individual can only see the APIs that his group has access to, plus the APIs which are assigned to the 'guest' group

<b>Note: </b>By default all the scripts that the APIs refer to should be in the 'bash_scripts' directory. If you want to change it, just make sure you change the SCRIPTS_DIR variable in the settings.py accordingly.

### Sample Data
There is a file named "populate_db.py" which you can execute to create sample data to work with the application. 


### Postgresql database setup
Install and initialize postgresql using the following commands (for CentOS):
```bash
$ sudo yum install postgresql-server postgresql-contrib

$ sudo postgresql-setup initdb
```
Now open the configuration file using:
```bash
$ sudo vim /var/lib/pgsql/data/pg_hba.conf
```
At the end of this file change 'ident' to 'md5' for both lines. 

Now you can setup ScriptManager database. Switch to the postgres user:
```bash
sudo su - postgres
```
Create a database user:
```bash
createuser aban
```
Create a new database and set the user as the owner:
```bash
createdb script_manager --owner aban
```
Define a strong password for the user:
```bash
psql -c "ALTER USER aban WITH PASSWORD 'xxxxxxxxxxxx'"
```
We can now exit the postgres user:
```bash
exit
```
In case you want to connect to your database, use the following command:
```bash
psql -U aban -h 127.0.0.1 script_manager
```
It will ask for your password and then you are good to go!

### Important Note: celery as daemon
Make sure you have celery service running on your server. 
in order to do this, follow this instruction:

In this configuration we make celery use Redis as its queue. So make sure you have redis installed and running. 

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

### Daemonizing celery using celeryd
If you are using CentOS, chances are you cannot install supervisor. So follow these steps instead:

1- The file from https://github.com/celery/celery/blob/3.0/extra/generic-init.d/celeryd needs to be copied in your /etc/init.d folder with the name celeryd

2- Then you need to create a configuration file in the folder /etc/default with the name celeryd that is used by the above script. This configuration file basically defines certain variables and paths that are used by the above script. Here's an example configuration:
```bash
# Names of nodes to start
#   most people will only start one node:
CELERYD_NODES="worker1"
#   but you can also start multiple and configure settings
#   for each in CELERYD_OPTS
#CELERYD_NODES="worker1 worker2 worker3"
#   alternatively, you can specify the number of nodes to start:
#CELERYD_NODES=10

# Absolute or relative path to the 'celery' command:
CELERY_BIN="/root/.virtualenvs/script-manager/bin/celery"
#CELERY_BIN="/virtualenvs/def/bin/celery"

# App instance to use
# comment out this line if you don't use an app
CELERY_APP="ScriptManager"
# or fully qualified:
#CELERY_APP="proj.tasks:app"

# Where to chdir at start.
CELERYD_CHDIR="/root/PythonProjects/script-manager/"

# Extra command-line arguments to the worker
CELERYD_OPTS="--time-limit=300 --concurrency=8"
# Configure node-specific settings by appending node name to arguments:
#CELERYD_OPTS="--time-limit=300 -c 8 -c:worker2 4 -c:worker3 2 -Ofair:worker1"

# Set logging level to DEBUG
CELERYD_LOG_LEVEL="DEBUG"

# %n will be replaced with the first part of the nodename.
CELERYD_LOG_FILE="/root/PythonProjects/script-manager/logs/celery-worker.log"
CELERYD_PID_FILE="/var/run/celery/%n.pid"

# Workers should run as an unprivileged user.
#   You need to create this user manually (or you can choose
#   a user/group combination that already exists (e.g., nobody).
CELERYD_USER="root"
CELERYD_GROUP="root"

# If enabled pid and log directories will be created if missing,
# and owned by the userid/group configured.
CELERY_CREATE_DIRS=1
```
3- Then do:
```bash
sudo systemctl daemon-reload
```
Now you can execute systemctl {enable|start|stop|restart|...} celeryd

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


## Another important note
Be sure that you give enough permissions to the folders that the application needs to read from and write to them.
For example the app must be able to create directories to store the output files of the requests it executes.
For starters, the default folders 'bash_scripts' and 'output_files' need to be considered. A 755 permission will be desirable.   
Also remember That the celery logs are saved in the "celery_logs" folder