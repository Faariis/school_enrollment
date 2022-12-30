

- No need for pid
```bash
$ gunicorn --bind 0.0.0.0:8000 myEnrollment.wsgi:application --pid /tmp/mygunicorn.pid
```

- Install nginx and create file in `site-available` and symlink of file in `site-enabled`
- In case only socket file is located in `/etc/systemd/system` and not service file
  start of socket activation will fail
  ```bash
  $ journal -b
  gunicorn.socket: Socket service gunicorn.service not loaded, refusing.
  Failed to listen on gunicorn socket activation.
  ```

- Enable socket for gunicorn withot server
```bash
$ sudo systemctl enable gunicorn.socket
Created symlink /etc/systemd/system/sockets.target.wants/gunicorn.socket → /etc/systemd/system/gunicorn.socket.
```
It is eanbled, but inactive
Now creating the service and again starting the socket still problem.

https://ubuviz.com/blog/2021/06/09/deploying-django-based-app-systemd/
https://www.mindyourdata.org/posts/autostart-application-as-a-service-in-linux/

### NOtes how to start gunicorn service with socket activation
- Create a socket
```bash
$ sudo systemctl cat gunicorn.socket 
# /etc/systemd/system/gunicorn.socket
[Unit] 
Description=gunicorn socket activation  
Documentation= https://eacon.ba

[Socket] 
# We could have multiple streams
# ListenStream= 4444  
ListenStream=/run/gunicorn.sock
# default false means AF_UNIX socket (same machine)
# yes AF_INET
Accept= false
SocketMode= 777
# gunicorn.service will inherit FD by socket activation,
# no need  permissions for socket.
# nginx will need permision
SocketUser=www-data

[Install] 
WantedBy= sockets.target
```

- Create a service
```bash
# /etc/systemd/system/gunicorn.service
[Unit]
# Unit can be timer,path, service,socket
Description=Gunicorn for app
Documentation=https://eacon.ba
After=network.target
Requires=gunicorn.socket

[Service]
#Add env var, that can be used by ExecStart script
#Environment=DJANGO_DEBUG=True

Environment=PROJECT_PATH=/home/anel/GitHub/school_enrollment
Environment=APP_NAME=myEnrollment
Environment=APP_PATH=/home/anel/GitHub/school_enrollment/myEnrollment
Environment=GUNICORN_BIN=
Environment=WORKER_NUM=1
EnvironmentFile=/home/anel/GitHub/school_enrollment/.systemd_env
#PIDFile used only for forking
#Can be found from systemctl and $MAINPID
User=anel
Group=www-data
#RuntimeDirectory=/home/anel/GitHub/school_enrollment/myEnrollment
# It has to be absolute path
WorkingDirectory=/home/anel/GitHub/school_enrollment/myEnrollment
# This will start new shell
#ExecStartPre=/bin/bash -c "source /home/anel/school_enrollment/school_enrollment/env/bin/activate"
#ExecStartPre=/bin/bash -c "source /home/anel/school_enrollment/school_enrollment/.env"
# print to stdout and catch with StandardOutput
ExecStartPre=/bin/bash -c "env"
# ExecStartPre=/bin/bash -c "env >/tmp/venv-vars.log" # doesn't work
ExecStart=/home/anel/GitHub/school_enrollment/env/bin/gunicorn\
          --access-logfile /tmp/gunicorn.service.log\
          --workers ${WORKER_NUM}\
          --error-logfile /tmp/gunicorn.service.error \
          --bind unix:/run/gunicorn.socket\
          ${APP_NAME}.wsgi
ExecReload=/bin/kill -s HUP $MAINPID

#If we wanted to pass stdin to script ^
#StandardInput=socket 
# test with: socat - TCP:server_IP_address:4444
# https://www.linux.com/training-tutorials/systemd-services-beyond-starting-and-stopping/
# Default Type=simple
Type=notify
Restart=always
TimeoutStopSec=5
PrivateTmp=true
KillSignal=SIGQUIT
StandardError=syslog
NotifyAccess=all
StandardError=file:/tmp/gunicorn-errors.err
StandardOutput=file:/tmp/gunicorn-output.log

[Install]
WantedBy=multi-user.target
```
- On the server I have created dedicated directory for environment files only
- If we change env var, we have to stop socket and start daemon and service again
- Enable the socket
```bash
$ sudo systemctl enable gunicorn.socket
```
- If changes are made on service, stop the systemd daemon, stop the gunicorn socket and start the service, yes service, it will activate the socket
```bash
$ sudo systemctl daemon-reload && sudo systemctl start gunicorn.service && sudo systemctl status gunicorn
```
- Watch error and logs in file instead of syslog (journal)
```bash
$ cat /tmp/gunicorn-errors.err 
Not Found: /

$ cat /tmp/gunicorn-output.log 
SHELL=/bin/bash
DATABASE_PASS=whatever
GUNICORN_BIN=
PWD=/home/anel/GitHub/school_enrollment/myEnrollment
DATABASE_NAME=myEnrollmentDB
LOGNAME=anel
HOME=/home/anel
LANG=en_US.UTF-8
DATABASE_USER=anel
SECRET_KEY=django-insecure-atyjk60=yq7#xy@+@_jx
JWT_PRIVATE_KEY=whatever
INVOCATION_ID=9e3962391
# DJANGO_ALLOWED_HOSTS=localhost
# Here must be server name too
DJANGO_ALLOWED_HOSTS="localhost,51.15.114.199"
APP_PATH=/home/anel/GitHub/school_enrollment/myEnrollment
PROJECT_PATH=/home/anel/GitHub/school_enrollment
USER=anel
DJANGO_DEBUG=True
NOTIFY_SOCKET=/run/systemd/notify
APP_NAME=myEnrollment
SHLVL=0
DATABASE_HOST=db
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin
WORKER_NUM=1
_=/usr/bin/env
```
- Difference between systemd directive `Environment=` and `PassEnvironment= KEY1 KEY2` is that later is used by systemd (PID 1) itself, no need for that.
- Gunicorn is installed _inside_ virtualenv and when started 
that binary we don't need to load explicitly venv.
- Got working!

- After that install reverse-proxy `nginx`
```bash
$ sudo apt install nginx-core
```
- Create virtual host for nginx and set to desired port and proxy to socket
```bash
$ cat /etc/nginx/sites-available/gunicorn-nginx 
server {
    listen 5000;
    server_name 51.15.114.199;
    location = /favicon.ico { access_log off; log_not_found off; }

    location / {
        proxy_pass http://unix:/run/gunicorn.sock;
        }
    }
```
- Create symlink with full path to `sites-enabled`
```bash
$ sudo ln -s /etc/nginx/sites-available/gunicorn-nginx /etc/nginx/sites-enabled/gunicorn-nginx
$ ls -la /etc/nginx/sites-enabled/|grep gunicorn
lrwxrwxrwx 1 root root   41 Dec 30 01:01 gunicorn-nginx -> /etc/nginx/sites-available/gunicorn-nginx
```
- Test `nginx`
```bash
$ sudo nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```
