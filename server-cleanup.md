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
