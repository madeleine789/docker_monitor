__author__ = 'mms'

import time
from docker import Client
client = Client(base_url='unix://var/run/docker.sock', timeout=10)

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


def containers_with_status(status='Running'):
	result = []
	containers = client.containers(filters={'status': status})
	for cont in containers:
		container = {'id': cont['Id'], 'cmd': cont['Command'], 'status': cont['Status'], 'name': cont['Name']}
		# print "ID: %s CMD: %s STATUS: %s".format(container['Id'], container['Command'], container['Status'])
		result.append(container)
	return result


def containers():
	all_conatiners = {}
	containers = client.containers() #(filters={'status': status})
	for cont in containers:
		container = {'id': cont['Id'], 'cmd': cont['Command'], 'status': cont['Status'], 'name': cont['Names'][0]}
		# print "ID: %s CMD: %s STATUS: %s".format(container['Id'], container['Command'], container['Status'])
		all_conatiners[cont['Id']] = container
	return all_conatiners


def images():
	imgs = client.images()
	images = []
	for img in imgs:
		image = {}
		image['created'] = time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime(img[u'Created']))
		image['name'] = img['RepoTags'][0]
		image['virtual_size'] = img[u'VirtualSize']
		image['size'] = img[u'Size']
		image['id'] = img[u'Id']
		images.append(image)
	return images