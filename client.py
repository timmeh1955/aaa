from time import sleep
import os.path, time
import os
import datetime
import subprocess
import sys


def replaceline(ffile, oldsting, newstring):
	os.system('sudo chmod 777 ' + ffile)
	f = open(ffile, 'r')
	sstr = ''
	for line in f:
		sstr += line.replace(oldsting, newstring)
	f = open(ffile, 'w')
	f.write(sstr)
	f.close()

def ossystem(sstr):
	os.system(sstr)
	writelog(sstr)

def writelog(sstr):
	now = datetime.datetime.now()
	f = open('/home/pi/l', 'a')
	f.write(now.strftime("%Y %m %d %H:%M ") + sstr + "\n")
	f.close()
	print sstr

if True:
	ossystem('sudo apt-get update')
	ossystem('sudo apt-get -y upgrade')

if True:
	f = open("/home/pi/log.txt", 'w')
	f.write('New system.')
	f.close()
	writelog('/home/pi/log.txt')
if False:
	ossystem('sudo apt-get -y install python3-requests') # could be installed by default
if True:
	ossystem('sudo apt-get -y install apache2')
	ossystem('sudo apt-get install -y python3-pygame')
	ossystem('sudo apt-get -y install git')
	ossystem('sudo apt-get -y install sshpass')
	os.system('sudo cp /usr/share/zoneinfo/Europe/Amsterdam /etc/localtime')
	writelog('time zone')
	f = open("/home/pi/config.txt", 'w')
	sstr = '{"reverse_ssh_server": "31.20.182.94", "version":"00000"}'
	f.write(sstr)
	f.close()
	writelog('config.txt')
	f = open("/home/pi/ssh_port", 'w')
	f.write('12345')
	f.close()
	f = open("/home/pi/ipaddress", 'w')
	f.write('31.20.182.94')
	f.close()
	f = open("/bin/l", 'w')
	f.write('ls -l $1')
	f.close()
	os.system('sudo chmod 777 /bin/l')
	writelog('/home/pi/ipaddress')
	sstr = "* * * * * sudo python3 /home/pi/m.py >/dev/null 2>&1 &"
	sstr += "\n" + '*/5 * * * * sshpass -p roma2- ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -fNTR $(cat "/home/pi/ssh_port"):localhost:22 pi@$(cat \"/home/pi/ipaddress\") -p 9212'
	sstr = "cat <(crontab -l) <(echo '"+sstr+"') | crontab -"
	subprocess.call(['bash', '-c', sstr])
	writelog('crontab')

	ossystem('cd /home/pi/ && git clone "https://github.com/timmeh1955/aaa.git"')
	files = ['a.py','ffunctions.py','m.py']
	for ffile in files:
		ossystem('sudo mv /home/pi/aaa/' + ffile + ' /home/pi')
	ossystem('sudo mv aaa /dev/shm')
	ossystem('sudo rm /home/pi/client.py')