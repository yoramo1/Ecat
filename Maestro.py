import sys
import os
import telnetlib
import click
import subprocess
import MmcResource
import settings


@click.group()
def cli():
	pass


def ExecTelnetCmd(cmd, tn, resp_trigger):
	print('Run->', cmd)
	tn.write(cmd.encode('ascii')+b'\n')
	rsp = tn.read_until(resp_trigger.encode('ascii')).decode('ascii')
	print('Responce->',rsp)

def ping(host='example.com', count=1, wait_sec=1):
	print('PING->',host)
	response =  subprocess.call(["ping",  host])
	if response == 0:
		return True
	return False
		
@click.command()
@click.argument('host',  type=str)
@click.argument('type',  type=str)
def factory_default(host,type):
	'''
	Reset Maestro to Factory Default
	'''

	settings1 = settings.settings()
	#host = '192.168.1.3'
	if type.upper()=='PMAS':
		resp_trigger ='~#'
	elif type.upper()=='GMAS':
		resp_trigger ='#'
	else:
		resp_trigger ='#'
		
	r = ping(host)
	
	if r== True:
		print('ping OK to ->',host)
		
		tn = telnetlib.Telnet(host)

		if tn!= None:
			tn.read_until(b"login: ")
			m = settings1.uid+'\n'

			tn.write(m.encode('ascii'))

			if settings1.pwd:
				tn.read_until(b'Password: ')
				m = settings1.pwd + '\n'
				tn.write(m.encode('ascii'))

			print('login OK')
			#print(tn.read_all().decode('ascii'))
			
			#tn.set_debuglevel(3)
			#ExecTelnetCmd('ps',tn)
			#rsp = tn.read_until(b'~#').decode('ascii')
			#print('Responce->',rsp)
			
			cmd='rm /mnt/jffs/MMC/config/Ethercat/cfg.xml'
			ExecTelnetCmd(cmd,tn,resp_trigger)
			cmd='rm /mnt/jffs/MMC/config/resources/MMCResources.xml'
			ExecTelnetCmd(cmd,tn,resp_trigger)
			
			ExecTelnetCmd('exit',tn, resp_trigger)
			tn.close()

			print('Close')
			print(tn.read_all().decode('ascii'))
		else:
			print('cannot open telnet on:', host)
	else:
		print ('Host not reacable')
		
@click.command()
@click.argument('res_file',  type=click.Path())
def maestro_resource(res_file):
	pass
	print('maestro_resource ->', res_file)
	res = MmcResource.MmcResource(res_file) 
	res.load()
	res.print()
		
cli.add_command(factory_default)
cli.add_command(maestro_resource)
	
if (__name__=='__main__'):
	cli()
