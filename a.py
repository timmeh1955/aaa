from time import sleep
import os.path, time
import os
import datetime
import subprocess
import sys
import json
import requests
from ffunctions import *
import pygame

pygame.init()
pygame.mouse.set_visible(0)
screen = pygame.display.set_mode((0,0),pygame.RESIZABLE)
tteller = 0

try:
	sysargv = sys.argv[1]
except:
	sysargv = ''

ssm = system_info()
myfont = pygame.font.SysFont("Comic Sans MS", 50)

while True:
	try:
		cf = configtxt()
	except:
		sstr = 'do nothing'
	if cf.read('activation_code') == '':
		lable_id = 'ID'
		lable_act_code = ''
	else:
		lable_id = 'Temporary ID'
		lable_act_code = 'Activation Code:'
	screen.fill((0,0,0))
	label = myfont.render(lable_id, 1, (255, 255, 0))
	screen.blit(label, (210, 110))
	label = myfont.render(str(cf.read('id')), 1, (255, 255, 0))
	screen.blit(label, (230, 160))
	label = myfont.render("Computer: ", 1, (255, 255, 0))
	screen.blit(label, (210, 260))
	label = myfont.render(str(ssm.computernr), 1, (255, 255, 0))
	screen.blit(label, (230, 310))
	if cf.read('activation_code') != '':
		label = myfont.render(lable_act_code, 1, (255, 255, 0))
		screen.blit(label, (210, 410))
		label = myfont.render(cf.read('activation_code'), 1, (255, 255, 0))
		screen.blit(label, (230, 460))
	label = myfont.render("A product of:", 1, (255, 255, 0))
	screen.blit(label, (210, 560))
	label = myfont.render("www.waaromzomeilijk.nl", 1, (255, 255, 0))
	screen.blit(label, (230, 610))
	# show the whole thing
	pygame.display.flip()

	index_html = '''
<html>
<head>
	<title>WaaromZoMoeilijk</title>
	<meta http-equiv="refresh" content="3" />
	<style type="text/css">
body {
	font-size: 5px; font-family: Verdana, Arial, "sans-serif"; color: yellow; background-color: black;
}
table{
	font-size: 44px;
}
</style>
<body><br><br><br><br><br>
<table width=100%>
<tr>
	<td width=20%>
	<td width=30% align=left>Temporary ID: 
	<td width=50%>iiii
	<td width=20%>
</tr>
<tr>
	<td>
	<td align=left>Computernr: 
	<td>cccc
	<td>
</tr>
aaaa
<tr>
	<td>
	<td colspan=3><br><br>A product of www.waaromzomoeilijk.nl
</tr>
</table></body></html>
'''

	index_html = index_html.replace('iiii',str(cf.read('id')))
	index_html = index_html.replace('cccc',ssm.computernr)
	if cf.read('activation_code') == '':
		index_html = index_html.replace('Temporary ','')
		index_html = index_html.replace('aaaa','')
		index_html = index_html.replace('content="3"','content="60"')
		check_again = 60
	else:
		index_html = index_html.replace('aaaa','<tr><td><td align=left>Activation code: <td>' + cf.read('activation_code') + '<td></tr>')
		check_again = 1
	f=open('/var/www/html/index.html','w+')
	f.write(index_html)
	f.close()
	tteller += 1
	print('ppp: ' + str(tteller))
	sleep(check_again)
