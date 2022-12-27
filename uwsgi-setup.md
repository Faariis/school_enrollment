$ cat uwsgi-files/test.ini
[uwsgi]
home = /home/anel/my_playground/webapps
chdir = %(home)/p_tscze
wsgi-file =%(chdir)/p_tscze/wsgi.py
master=true
processes=5

socket = /home/anel/testproject.sock
vacuum = true
chown-socket = anel:www-data
chmod-socket = 660

$ cat uwsgi-files/tscze.ini 
[uwsgi]
home = /home/anel/web-workspace/webapps/
chdir = %(home)/upis
wsgi-file =%(chdir)/upis/wsgi.py
master=true
processes=5

socket = /home/anel/upis.sock
vacuum = true
chown-socket = anel:www-data
chmod-socket = 660

$ cat uwsgi-mojezagadjenje/mojezagadjenje.ini
[uwsgi]
home = /home/anel/mojezagadjenje/env
chdir = /home/anel/mojezagadjenje/my_pollution
wsgi-file =%(chdir)/my_pollution/wsgi.py
master=true
processes=5

#http= 0:9000
socket = /home/anel/mojezagadjenje1.sock
vacuum = true
logto = /home/anel/uwsgi.log
debug = true
chown-socket = anel:www-data
chmod-socket = 775

$ cat uwsgi-scada/eacon_scada.ini
[uwsgi]
home = /home/anel/eacon_scada/pyscada-anel/env
chdir = /home/anel/eacon_scada/pyscada-anel/scada_eacon
#wsgi-file =%(chdir)/scada_eacon/wsgi.py
wsgi-file=/home/anel/eacon_scada/pyscada-anel/scada_eacon/scada_eacon/wsgi.py
master=true
processes=5

socket = /home/anel/scada.sock
vacuum = true
chown-socket = anel:www-data
chmod-socket = 660


$ cat test_zagadjenje.ini
[uwsgi]
home=  /home/anel/mojezagadjenje/env
chdir= /home/anel/mojezagadjenje/my_pollution
wsgi-file=/home/anel/mojezagadjenje/my_pollution/my_pollution/wsgi.py

http=0:9000
#stats= 0:9191
#socket = /home/anel/testproject.sock
#vacuum = true
#chown-socket = anel:www-data
#chmod-socket = 660

