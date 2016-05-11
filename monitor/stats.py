__author__ = 'mms'

import re
import os
import json 
import dateutil.parser

from docker import Client
client = Client(base_url='unix://var/run/docker.sock', timeout=10)

def general_info(container):

	general = {}
	detail = client.inspect_container(container)
	general['name'] = detail['Name']
	general['hostname'] = detail['Config']['Hostname']
	general['created'] = dateutil.parser.parse(detail['Created']).strftime("%d-%m-%Y %H:%M:%S")
	started = dateutil.parser.parse(detail['State']['StartedAt'])
	general['started_at'] = started.strftime("%d-%m-%Y %H:%M:%S")
	finished = dateutil.parser.parse(detail['State']['FinishedAt'])
	if started < finished:
		general['finished_at'] = finished.strftime("%d-%m-%Y %H:%M:%S")
	else : general['finished_at'] = ''
	general['ip'] = detail['NetworkSettings']['IPAddress']
	return general


def processes_running(container):
	processes = []
	print client.top(container)['Processes']
	for pr in client.top(container)['Processes']:
		# print "PID: %d USER: %s CMD: %s".format(p[0], p[1], p[2])
		p = {}
		p['PID'] = pr[1]
		p['USER'] = pr[0]
		p['CMD'] = pr[7]
		processes.append(p)
	return processes

def cpu_stats(container): 				# type  system, user, all
	stats = client.stats(container)
	for stat_obj in stats:
		cpu_stats = json.loads(stat_obj)['cpu_stats']
		print json.loads(stat_obj)['blkio_stats']
		break
	return cpu_stats


def memory_stats(container):
	stats = client.stats(container)
	for stat_obj in stats:
		mem_stats = json.loads(stat_obj)['memory_stats']
		break
	print mem_stats.keys()
	return mem_stats


def network_stats(container):
	stats = client.stats(container)
	for stat_obj in stats:
		print stat_obj
		network_stats = json.loads(stat_obj)['networks']
		break
	return network_stats


def blkio_stats(container):
	stats = client.stats(container)
	for stat_obj in stats:
		blkio = json.loads(stat_obj)['blkio_stats']
		break
	blkio_stats = {}
	for op in blkio[u'io_service_bytes_recursive']:
		if op['op'] == u'Read': blkio_stats['serviced_read_b'] = op['value']
		if op['op'] == u'Write': blkio_stats['serviced_write_b'] = op['value']
		if op['op'] == u'Sync': blkio_stats['serviced_sync_b'] = op['value']
		if op['op'] == u'Async': blkio_stats['serviced_async_b'] = op['value']
		if op['op'] == u'Total': blkio_stats['serviced_total_b'] = op['value']

	for op in blkio[u'io_serviced_recursive']:
		if op['op'] == u'Read': blkio_stats['serviced_read'] = op['value']
		if op['op'] == u'Write': blkio_stats['serviced_write'] = op['value']
		if op['op'] == u'Sync': blkio_stats['serviced_sync'] = op['value']
		if op['op'] == u'Async': blkio_stats['serviced_async'] = op['value']
		if op['op'] == u'Total': blkio_stats['serviced_total'] = op['value']

	return blkio_stats
'''
	for op in blkio[u'io_merged_recursive']:
		if op['op'] == u'Read': blkio_stats['merged_read'] = op['value']
		if op['op'] == u'Write': blkio_stats['merged_write'] = op['value']
		if op['op'] == u'Sync': blkio_stats['merged_sync'] = op['value']
		if op['op'] == u'Async': blkio_stats['merged_async'] = op['value']
		if op['op'] == u'Total': blkio_stats['merged_total'] = op['value']

	for op in blkio[u'io_queue_recursive']:
		if op['op'] == u'Read': blkio_stats['queue_read'] = op['value']
		if op['op'] == u'Write': blkio_stats['queue_write'] = op['value']
		if op['op'] == u'Sync': blkio_stats['queue_sync'] = op['value']
		if op['op'] == u'Async': blkio_stats['queue_async'] = op['value']
		if op['op'] == u'Total': blkio_stats['queue_total'] = op['value']

	for op in blkio[u'sectors_recursive']:
		if op['op'] == u'Read': blkio_stats['sectors_read'] = op['value']
		if op['op'] == u'Write': blkio_stats['sectors_write'] = op['value']
		if op['op'] == u'Sync': blkio_stats['sectors_sync'] = op['value']
		if op['op'] == u'Async': blkio_stats['sectors_async'] = op['value']
		if op['op'] == u'Total': blkio_stats['sectors_total'] = op['value']
'''
	


def display_status(container):
	detail = client.inspect_container(container)
	state = detail["State"]
	if bool(state["Paused"]):
		print(1)  # Paused
	elif bool(state["Running"]):
		print(0)  # Running
	elif int(state["ExitCode"]) == 0:
		print(2)  # Stopped
	else:
		print(3)  # Crashed
