__author__ = 'mms'


#from docker import Client

#c = Client(base_url='unix://var/run/docker.sock', version='1.9', timeout=10)

from monitor import *


def system_wide_info():
	system_info = {}
	info = client.info()

	system_info['containers'] = info['Containers']
	system_info['images'] = info['Images']
	system_info['driver'] = info['Driver']
	system_info['mem'] = info['MemTotal']
	system_info['kernel'] = info['KernelVersion']
	system_info['ncpu'] = info['NCPU']
	system_info['os'] = info['OperatingSystem']
	system_info['index'] = info['IndexServerAddress']

	return system_info


def containers_with_status(status='running'):
	if status == 'ExitCode':

		# TODO

		pass
	else:
		containers = client.containers(filters={'status': status})
		result = []
		for cont in containers:
			container = {'id': cont['Id'], 'cmd': cont['Command'], 'status': cont['Status'], 'name': cont['Name']}
			# print "ID: %s CMD: %s STATUS: %s".format(container['Id'], container['Command'], container['Status'])
			result.append(container)
	return result