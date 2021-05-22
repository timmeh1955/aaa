import os.path, time
import os
import datetime
import subprocess
import glob
import json
import sys

now = datetime.datetime.now()
# check that this job is started with python3; not with python:
try:
	subprocess.run(['iwgetid'], capture_output=True, text=True).stdout
except:
	print('You should start this job with python3.')
	sys.exit()

class configtxt:
	def __init__(self):
		f = open('/home/pi/config.txt', 'r')
		sstr = f.read()
		if len(sstr) < 5:
			f.close()
			f = open('/home/pi/configres.txt', 'r')
			sstr = f.read()
		self.cf = json.loads(sstr)
		f.close()

	def read(self, sstr):
		now = datetime.datetime.now()
		if not sstr in self.cf:
			return ''
		else:
			return(self.cf[sstr])

	def check_update_config(self, parm, value):
		if value is not None and self.read(parm) != value:
			self.cf[parm] = value
			f = open('/home/pi/config.txt', 'w')
			f.write(json.dumps(self.cf))
			f.close()
			return 'updated'
		else:
			return 'done nothing'

class system_info:
	def __init__(self):
	# computernr
		with open('/proc/cpuinfo') as f:
			for line in f:
				line = line.replace('\n', '')
				line = line.replace('\r', '')
				if line[:6] == 'Serial':
					line = line.split(':')
					line = line[1]
					while line[:1] == ' ':
						line = line[1:]
					self.computernr = line
		if now.strftime('%Y%m%d%H%M') < '202103140000':
			self.computernr = '100000000d2944e1'
		tteller = 0
		self.comp_nr_only_dec = '' # comp_nr_only_dec contains only numbers but it is a string
		while tteller < len(self.computernr):
			if self.computernr[tteller:tteller+1] in '0123456789':
				self.comp_nr_only_dec += self.computernr[tteller:tteller+1]
			tteller += 1
	# wifi networks near the rpi
		self.wifiCurrentNetwork = 'I didnt find any'
		if os.path.isfile('/dev/shm/wifinet.txt') and now.strftime('%Y%m%d%H%M') > '202008310000':
			f = open("/dev/shm/wifinet.txt","r")
			ff = f.readlines()
			sstr = ''
			for row in ff:
				if sstr != '':
					sstr += ','
				sstr += row.replace("\n","")
			self.wifilist = sstr
		else:
			self.wifilist = ''
	# which wifi are we currently using?
		ps = subprocess.run(['iwgetid'], capture_output=True, text=True).stdout
		processes = ps.split('"')
		try:
			self.wifiCurrentNetwork = processes[1]
		except:
			self.wifiCurrentNetwork = 'no wifi'
	# IP numbers
		ps = subprocess.run(['ifconfig'], capture_output=True, text=True).stdout
		processes = ps.split("\n")
		readingnow = ''
		ethIPaddress = ''
		wlanIPaddress = ''
		for row in processes:
			findinet = ''
			while row[:1] == ' ':
				row = row[1:]
			row = row.replace('  ',' ')
			if row[:4] == 'eth0':
				readingnow = 'eth0'
			elif row[:4] == 'wlan':
				readingnow = 'wlan'
			elif row[:10] == 'RX packets' or row[:3] == 'lo:':
				readingnow = ''
			if row[:5] == 'inet ':
				row = row.split(' ')
				if readingnow == 'eth0':
					ethIPaddress = row[1]
				elif readingnow == 'wlan':
					wlanIPaddress = row[1]
		if ethIPaddress != '' and wlanIPaddress != '':
			self.ipAddress = ethIPaddress + 'x' + wlanIPaddress
		elif ethIPaddress != '' and wlanIPaddress == '':
			self.ipAddress = ethIPaddress
		elif ethIPaddress == '' and wlanIPaddress != '':
			self.ipAddress = wlanIPaddress
		else:
			self.ipAddress = ''
		self.ethIPaddress = ethIPaddress
		self.wlanIPaddress = wlanIPaddress
	# known wifi networks
		wifiKnownNetworks = ''
		os.system('sudo chmod 777 /etc/wpa_supplicant/wpa_supplicant.conf')
		with open('/etc/wpa_supplicant/wpa_supplicant.conf') as f:
			for line in f:
				if line[:6] == '  ssid':
					sstr = line.split('"')
					if wifiKnownNetworks != '':
						wifiKnownNetworks += ','
					wifiKnownNetworks += sstr[1]
		self.wifiKnownNetworks = wifiKnownNetworks
		# screen sizes
		self.screenwidth = 1366
		self.screenheight = 768
		# ps = str(subprocess.Popen(["tvservice","-s"], stdout=subprocess.PIPE).communicate()[0])
		# sstr = ps.split('\n')
		# sstr = sstr[0]
		# sstr = sstr.split(' ')
		# tteller = len(sstr) - 1
		# while tteller > 0:
			# if 'x' in sstr[tteller]:
				# res = sstr[tteller]
				# res = res.split('x')
				# self.screenwidth = int(res[0])
				# self.screenheight = int(res[1])
				# tteller = 0
			# tteller -= 1

		# used space of SD card
		ps = subprocess.run(['df'], capture_output=True, text=True).stdout
		sstr = ps.split('\n')
		sstr = sstr[1]
		sstr = sstr.replace('         ',' ')
		sstr = sstr.replace('     ',' ')
		sstr = sstr.replace('   ',' ')
		sstr = sstr.replace('  ',' ')
		sstr = sstr.split(' ')
		self.sd_info = 'Size:' + str(round(float(sstr[2])/1000000,1)) + ' Gb used: ' + sstr[4]

	def write_wifi_networks(self):
		wifi_list = ''
	# make a list of all wifi that we see near the rpi, including the wifi from the neighbours
		ps = subprocess.run(['sudo','iwlist','wlan0','scan'], capture_output=True, text=True).stdout
		processes = ps.split('\n')
		for row in processes:
			row = str(row)
			tteller =	row.find('ESSID')
			if tteller > 0:
				row = row[tteller:]
				row = row.replace('"','')
				row = row.replace('ESSID:','')
				if wifi_list == '':
					wifi_list = row
				else:
					wifi_list = wifi_list + '\n' + row
		if len(wifi_list) > 4:
			wifinet = open('/dev/shm/wifinet.txt', 'w')
			wifinet.write(wifi_list)
			wifinet.close()

	def update(self, current_version, gitlabaddress):
		sstr = gitlabaddress.split('/')
		sstr = sstr[-1]
		foldername = sstr.replace('.git','')
		os.system('sudo rm -r /tmp/' + foldername + ' &')
		time.sleep(1)
		os.system('cd /tmp && sudo git clone "https://oauth2:' + gitlabaddress + '"')
		if os.path.isfile('/tmp/' + foldername + '/version.txt'):
			f = open('/tmp/' + foldername + '/version.txt', 'r')
			sstr = f.read()
			downloaded_version = sstr[:5]
			f.close()
			if downloaded_version > current_version:
				os.system('sudo cp /tmp/' + foldername + '/*.py /home/pi &')
				addtopermlog('Installed new version. Old: ' + current_version + '. Downloaded:' + downloaded_version)
				return downloaded_version
			else:
				addtopermlog('You have the latest version already. Current: ' + current_version + '. Downloaded:' + downloaded_version)
				return False
		else:
			addtopermlog('Can not download new version.')
			return False

def addtopermlog(sstr):
	try:
		print('from addtopermlog:' + str(sstr))
	except:
		print('from addtopermlog: can not print')
	now = datetime.datetime.now()
	logf = []
	f = open('/home/pi/log.txt', 'r')
	logf.append(now.strftime("%Y %m %d %H:%M ") + sstr)
	tteller = 1
	for sstr in iter(lambda: f.readline(), ''):
		sstr = sstr.replace('\n', '', 1)
		sstr = sstr.replace('\r', '', 1)
		if tteller < 300:
			logf.append(sstr)
		tteller += 1
	sstr = ''
	for line in logf:
		if sstr != '':
			sstr += "\n"
		sstr += line
	f = open('/home/pi/log.txt', 'w')
	f.write(sstr)
	f.close()

def addtosessionlog(sstr):
	try:
		print('from addtosessionlog:' + str(sstr))
	except:
		print('from addtosessionlog: can not print')
	now = datetime.datetime.now()
	try:
		with open('/dev/shm/log.txt', 'r+') as f:
			content = f.read()
			f.seek(0, 0)
			f.write(now.strftime("%Y %m %d %H:%M ") + sstr + '\n' + content)
	except:
		f = open('/dev/shm/log.txt', 'a')
		f.write(now.strftime("%Y %m %d %H:%M ") + sstr)
	f.close()

def findIP():
	ssstring = '- not available -'
	ps = subprocess.run(['ifconfig'], capture_output=True, text=True).stdout
	processes = ps.split('\n')
	for row in processes:
		steller = row.find('inet ')
		if steller > 0 and not '127.0.0.1' in row:
			if row.find('inet addr ') > 0:
			# this is for older debian versions
				sstr = row[steller + 10:]
			else:
				sstr = row[steller + 5:]
			steller = sstr.find(' ')
			sstr = sstr[:steller]
			if ssstring == '- not available -':
				ssstring = sstr
			else:
				ssstring += 'x' + sstr
	return ssstring

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

