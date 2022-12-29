### Removing logs
- Resizing the logs

```bash
$ du -sh /var/log
$ journalctl --vacuum-size=500M
```
- set in `/etc/systemd/journald.conf` `SystemMaxUse=100M` and restart journald
```bash
$ sudo systemctl restart systemd-journald
```
- `/var/log/btmp` is huge 6GB, attackers are trying to findout password
```bash
echo ''>/var/log/btmp #not working
$ sudo lastb -a|more  # this is reading from /var/log/btmp
```
This file is owned by root so
```bash
cat /dev/null > /var/log/btmp
```

fail2ban change port to 22
changing `/etc/ssh/sshd_config` to non-standard port like 8022 instad of 22
- To see who is running
```bash
$ last -f /var/run/utmp 
anel     pts/0        5.43.76.171      Tue Dec 27 18:37   still logged in
```

- Content of `wtmp` last logged in
```bash
/var/log$ last -f wtmp
anel     pts/0        5.43.76.171      Tue Dec 27 18:37   still logged in
anel     pts/0        5.43.74.222      Tue Jun  7 15:08 - 17:22  (02:14)
```
- To see the state of processes
```bash
$ ps -eo pid,stat,command
# man ps -> T - stopped state by job handle
```

### Change the ssh port number
- `ssh anel@51.15.114.199`
1. To use it `ssh -p 2222 anel@server`, `sftp -P port openssh-server`,
   `scp -P port source target` or `scp -P /path/ user@server:/dest/`
2. Navigate to `/etc/ssh/sshd_config` and change port
3. Restart service `sudo systemctl restart ssh`
4. Validate `netstat -tlpn|grep 2222` or `ss `
```bash
$ sudo netstat -tlpn|grep 2807
$ sudo netstat -tlpn|grep 22
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      32368/sshd          
tcp6       0      0 :::22                   :::*                    LISTEN      32368/sshd          
$ sudo systemctl restart ssh
$ sudo netstat -tlpn|grep 22
$ sudo netstat -tlpn|grep 2807
tcp        0      0 0.0.0.0:2807            0.0.0.0:*               LISTEN      26312/sshd          
tcp6       0      0 :::2807                 :::*                    LISTEN      26312/sshd 
```
Login with (Majra)
`ssh -p 2807 anel@51.15.114.199`
```bash
$ du -sh /var/log/btmp
68K	/var/log/btmp

```

- For `sshd_config`
  - I can change `PasswordAuthentication` to `no` and don't allow nobody to connect
    with password (only with public key), but will not do that now
  - Same happens for `PermitRootLogin` to `no`, but still is `yes`

### Working on server
- After performing `GitHub action` go to Actions->Runners and use `self-hosted` runners
- Check `python3` and `pip3` versions, update to 3.8 at least
```bash
$ python3 --version
Python 3.6.9
$ pip3 --version
pip 20.0.2 from /home/anel/.local/lib/python3.6/site-packages/pip (python 3.6)
$ ls ~/.local/bin/
pip  pip3  pip3.6
$ which pip3
/home/anel/.local/bin/pip3
$ which python3
/usr/bin/python3

```
### Intsall python 3.8.15
- Install `python3` and `pip3` to new version
```bash
$ sudo apt install python3.8
# installed in /usr/bin/python3.8
$ python3.8 --version
Python 3.8.0
# Create symbolic link to python3 < THIS DOESN'T WORK SEE BELOW serve is bionic >
$ sudo rm /usr/bin/python3 # this is symlink removed
$ sudo ln -s /usr/bin/python3.8 /usr/bin/python3 # created symlink
$ python3 --version
Python 3.8.0
# Upgrade pip3
$ python3 -m pip install --upgrade pip
$ pip3 --version
pip 22.3.1 from /home/anel/.local/lib/python3.8/site-packages/pip (python 3.8)
```

- Problem with symlinks above 3.8
  - Got the problem with `sudo apt update` where `python3-apt` was making problems.
  ```bash
  $ sudo apt update
  $ ModuleNotFoundError: No module named 'apt_pkg'
  ```
  - Solution drop symlink 3.8 and create new/old for 3.6
  - Have to do PROPER UPDATE To 3.8 on bionic [LINK](https://www.itsupportwale.com/blog/how-to-upgrade-to-python-3-8-on-ubuntu-18-04-lts/)
  ```BASH
    $ sudo add-apt-repository ppa:deadsnakes/ppa
    $ sudo update
    $ sudo apt list --upgradable
    Listing... Done
    libpython3.8-minimal/bionic 3.8.16-1+bionic1 amd64 [upgradable from: 3.8.0-3ubuntu1~18.04.2]
    libpython3.8-stdlib/bionic 3.8.16-1+bionic1 amd64 [upgradable from: 3.8.0-3ubuntu1~18.04.2]
    python3.8/bionic 3.8.16-1+bionic1 amd64 [upgradable from: 3.8.0-3ubuntu1~18.04.2]
    python3.8-minimal/bionic 3.8.16-1+bionic1 amd64 [upgradable from: 3.8.0-3ubuntu1~18.04.2]
    $ sudo apt upgrade
    $ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
    $ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2
    $ python3 --version
    Python 3.8.16
    $ sudo update-alternatives --config python3 # to see alternatives
  ```
- Install `venv`
  - After above, we have to install for 3.8 venv
  ```bash
  $ sudo apt install python3.8-distutils
  ```

- Since CI doesn't support 3.8.16 on x64 see [this](https://raw.githubusercontent.com/actions/python-versions/main/versions-manifest.json)
  I have to downgrade to stable 3.8.10 from ptyhon ftp
```bash
    $ apt-cache policy python3.8
    python3.8:
    Installed: 3.8.16-1+bionic1
    Candidate: 3.8.16-1+bionic1
    Version table:
    *** 3.8.16-1+bionic1 500
            500 http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic/main amd64 Packages
            100 /var/lib/dpkg/status
        3.8.0-3ubuntu1~18.04.2 500
            500 http://archive.ubuntu.com/ubuntu bionic-updates/universe amd64 Packages
            500 http://security.ubuntu.com/ubuntu bionic-security/universe amd64 Packages
  
```
- Uninstall old version and remove it from `update-alternatives`
- Download lower version and follow the [LINK](https://realpython.com/installing-python/)
```bash
# DON'T FORGET TO INSTALL DEPENDECIES
$ wget https://www.python.org/ftp/python/3.8.10/
$ tar -xf Python.3.8.10
$ cd Python 3.8.10 && ./configure --enable-optimization
$ make # create binary in local directory not in /usr/
$ sudo make altinstall
# It gets installed in /usr/local/bin/
$ /usr/local/bin/python3.8 --version
Python 3.8.10
$ sudo update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.8 3
update-alternatives: using /usr/local/bin/python3.8 to provide /usr/bin/python3 (python3) in auto mode
$ python3 --version
Python 3.8.10
# Still not updating the cache properly
# Commented $ sudo vim /etc/apt/apt.conf.d/50command-not-found
```
- IT CANNOT BE DONE ! SYSTEM VERSION 3.6.9 ON BIONIC, 3.8.10 CAN BE INSTALLED
  AND USED ON VIRTUAL ENV, BUT NOT AS SYSTEM INTSALLATION.

#### SOLUTION TO USE MULTIPLE PTYHON VERSIONS
- On bionic: `python3` == `3.6.9` global system one installation
- I have installed `python3.8.10` from source and is installed in
`/usr/local/bin` by invoking `sudo make <altsomethingtarget>`
- In order to use `3.8.10` I cannot *upgrade* from `3.6.9` to `3.8.10` on bionic,
but rather to use virtualenv. Now `python -m pip venv` doesn't allow to say which
python verion to use, but `virtualenv` package does. To be sure we will not install
it globally, but rather per user `--user` flat below:
```bash
$ python3 -m pip install --user virtualenv
```
- Create venv with other python version:
```bash
$ virtualenv -p="/usr/local/bin/python3.8" env

(env) /tmp/env$ python --version
Python 3.8.10
```

### Setting up Runner
- See GitHub Project ->Settings->Actions->Runners how to create and configure
  new runner (the same name as a server). Created `svc.sh` script to start the service of runners
  ```bash
    ~/actions-runner$ ls
    bin  config.sh  _diag  env.sh  externals  run-helper.cmd.template  run-helper.sh.template  run.sh  safe_sleep.sh  svc.sh
    $ sudo ./svc.sh install
    $ $ sudo ./svc.sh install
    Creating launch runner in /etc/systemd/system/actions.runner.aheacon-school_enrollment.start-tehnicka.service
    Run as user: anel
    Run as uid: 1001
    gid: 1001
    Created symlink /etc/systemd/system/multi-user.target.wants/actions.runner.aheacon-school_enrollment.start-tehnicka.service → /etc/systemd/system/actions.runner.aheacon-school_enrollment.start-tehnicka.service.
  ```
  - Start it and get status
  ```bash
    $ sudo ./svc.sh start

    /etc/systemd/system/actions.runner.aheacon-school_enrollment.start-tehnicka.service
    ● actions.runner.aheacon-school_enrollment.start-tehnicka.service - GitHub Actions Runner (aheacon-school_enrollment.start-tehnicka)
    Loaded: loaded (/etc/systemd/system/actions.runner.aheacon-school_enrollment.start-tehnicka.service; enabled; vendor preset: enabled)
    Active: active (running) since Wed 2022-12-28 17:10:20 UTC; 34ms ago
    Main PID: 8971 (runsvc.sh)
        Tasks: 2 (limit: 1066)
    CGroup: /system.slice/actions.runner.aheacon-school_enrollment.start-tehnicka.service
            └─8971 /bin/bash /home/anel/actions-runner/runsvc.sh

    Dec 28 17:10:20 start-tehnicka systemd[1]: Started GitHub Actions Runner (aheacon-school_enrollment.start-tehnicka).
    # Get status
    $ sudo ./svc.sh status

    /etc/systemd/system/actions.runner.aheacon-school_enrollment.start-tehnicka.service
    ● actions.runner.aheacon-school_enrollment.start-tehnicka.service - GitHub Actions Runner (aheacon-school_enrollment.start-tehnicka)
    Loaded: loaded (/etc/systemd/system/actions.runner.aheacon-school_enrollment.start-tehnicka.service; enabled; vendor preset: enabled)
    Active: active (running) since Wed 2022-12-28 17:10:20 UTC; 4s ago
    Main PID: 8971 (runsvc.sh)
        Tasks: 21 (limit: 1066)
    CGroup: /system.slice/actions.runner.aheacon-school_enrollment.start-tehnicka.service
            ├─8971 /bin/bash /home/anel/actions-runner/runsvc.sh
            ├─8978 ./externals/node16/bin/node ./bin/RunnerService.js
            └─8988 /home/anel/actions-runner/bin/Runner.Listener run --startuptype service

    Dec 28 17:10:20 start-tehnicka systemd[1]: Started GitHub Actions Runner (aheacon-school_enrollment.start-tehnicka).
    Dec 28 17:10:20 start-tehnicka runsvc.sh[8971]: .path=/home/anel/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
    Dec 28 17:10:20 start-tehnicka runsvc.sh[8971]: Starting Runner listener with startup type: service
    Dec 28 17:10:20 start-tehnicka runsvc.sh[8971]: Started listener process, pid: 8988
    Dec 28 17:10:20 start-tehnicka runsvc.sh[8971]: Started running service
    Dec 28 17:10:22 start-tehnicka runsvc.sh[8971]: √ Connected to GitHub
    Dec 28 17:10:23 start-tehnicka runsvc.sh[8971]: Current runner version: '2.300.2'
    Dec 28 17:10:23 start-tehnicka runsvc.sh[8971]: 2022-12-28 17:10:23Z: Listening for Jobs

  ```
- Now go and trigger Action on GitHub (GH).

### Configuring gunicorn server
- It has to be run from `application` folder
```
$ gunicorn --bind 0.0.0.0:8000 myEnrollment.wsgi
```

Have found that yt is creating the socket `/etc/systemd/system/gunicorn.socket`
```bash
[Unit]
Description=gunicorn socket
[Socket]
ListenStream=/run/gunicorn.socket

[Install]
wantedBy=sockets.target
```
Don't know why ^^^
After that created `/etc/systemd/service`
```bash
[Unit]
Description=gunicorn daemon for django project
Requires=gunicorn.socket
After=network.target

[Service]
User=anel
Group=www-data
WorkingDirectory=/home/anel/..
ExecStart=/home/.../bin/gunicorn \
          --access-logfile - \
          --workers  3\
          --bind unix:/run/gunicorn.sock \
          mysite.wsgi:application

[Install]
WantedBy=multi-user.target
```

Run status
```bash
$ sudo systemctl status gunicorn.socket
```

`$ sudo ufw status`

### Stoping already existing processes

We have ports already occupied 8000,5000,9000, let's see services and release them
```bash
$ netstat -tulpn
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:2807            0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:3000            0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:8000            0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:5000            0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:9000            0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -                   
tcp6       0      0 :::2807                 :::*                    LISTEN      -                   
tcp6       0      0 :::80                   :::*                    LISTEN      -                   
udp        0      0 127.0.0.53:53           0.0.0.0:*                           -                   
udp        0      0 0.0.0.0:68              0.0.0.0:*                           -     
```

With root we have more info
```bash
$ sudo netstat -tulpn
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      28845/systemd-resol 
tcp        0      0 0.0.0.0:2807            0.0.0.0:*               LISTEN      27324/sshd          
tcp        0      0 0.0.0.0:3000            0.0.0.0:*               LISTEN      11173/nginx: master 
tcp        0      0 0.0.0.0:8000            0.0.0.0:*               LISTEN      11173/nginx: master 
tcp        0      0 0.0.0.0:5000            0.0.0.0:*               LISTEN      11173/nginx: master 
tcp        0      0 0.0.0.0:9000            0.0.0.0:*               LISTEN      11173/nginx: master 
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      18419/mariadbd      
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      11173/nginx: master 
tcp6       0      0 :::2807                 :::*                    LISTEN      27324/sshd          
tcp6       0      0 :::80                   :::*                    LISTEN      11173/nginx: master 
udp        0      0 127.0.0.53:53           0.0.0.0:*                           28845/systemd-resol 
udp        0      0 0.0.0.0:68              0.0.0.0:*                           731/dhclient
```

Indeed
```bash
$ cat /etc/nginx/sites-enabled/
default         mojezagadjenje  scada           test            tscze         

$ ps aux|grep 11173
root     11173  0.0  0.2 141268  2272 ?        S    Nov16   0:00 nginx: master process /usr/sbin/nginx -g daemon on; master_process on;
```
Culprit is `nginx`
How to remove
```bash
$ sudo netstat -tulpn|grep 8000
tcp        0      0 0.0.0.0:8000            0.0.0.0:*               LISTEN      11173/nginx: master 
$ sudo rm /etc/nginx/sites-enabled/test
$ sudo netstat -tulpn|grep 8000
tcp        0      0 0.0.0.0:8000            0.0.0.0:*               LISTEN      11173/nginx: master 
# Use reload
$ sudo nginx -s reload
$ sudo netstat -tulpn|grep 8000

```

### About systemd 


About systemd
https://www.digitalocean.com/community/tutorials/systemd-essentials-working-with-services-units-and-the-journal
https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units
https://www.digitalocean.com/community/tutorials/how-to-use-journalctl-to-view-and-manipulate-systemd-logs
https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files

```bash

$ timedatectl list-timezones
$ sudo timedatectl set-timezone zone
$ timedatectl status
                      Local time: Thu 2022-12-29 13:56:03 CET
                  Universal time: Thu 2022-12-29 12:56:03 UTC
                        RTC time: Thu 2022-12-29 12:56:04
                       Time zone: Europe/Sarajevo (CET, +0100)
       System clock synchronized: yes
systemd-timesyncd.service active: yes
                 RTC in local TZ: no


$ journalctl -b -u nginx -o json-pretty
$ journalctl --utc # display timestamp in utc
$ journalctl _PID=8088
$ journalctl _UID=33 --since today
$ journalctl -F _GID
# With binaries
$ sudo journalctl home/anel/actions-runner/_work/school_enrollment/school_enrollment/env/bin/gunicorn
$ journalctl --disk-usage
```


About systemd service of gunicorn
https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units

NOt good ^ unknown how socket is created
From [understanding-systemd-units](https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files)

path `/lib/systemd/system1` stores also copies of units when system install unit files
/etc/systemd/system - takes precedence 
Override with `.d` folder adn file with `.conf`
Runtime units definitiosn services /run/systemd/system - priority less than /etc/ but more than /lib

Man pages
```bash
man systemd.journal-fields
man systemd.directive
man systemd.service
```