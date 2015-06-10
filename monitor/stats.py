__author__ = 'mms'


from docker_stats import Client
import re
import os

c = Client(base_url='unix://var/run/docker.sock', version='1.9', timeout=10)


def general_info(container):

	general = {}
	detail = c.inspect_container(container)
	general['name'] = detail['Name']
	general['hostname'] = detail['Hostname']
	general['created'] = detail['Created']
	general['started_at'] = detail['State']['StartedAt']
	general['finished_at'] = detail['State']['FinishedAt']

	return general


def processes_running(container):
	processes = []
	for p in c.top(container)['Processes']:
		# print "PID: %d USER: %s CMD: %s".format(p[0], p[1], p[2])
		p = {}
		p['PID'] = p[0]
		p['USER'] = p[1]
		p['CMD'] = p[2]
		processes.append(p)
	return processes

def display_cpu(container, type): 				# system, user, all
	detail = c.inspect_container(container)
	if bool(detail["State"]["Running"]):
		container_id = detail['Id']
		cpu_usage = {}
		with open('/sys/fs/cgroup/cpuacct/docker/' + container_id + '/cpuacct.stat', 'r') as f:
			for line in f:
				m = re.search(r"(system|user)\s+(\d+)", line)
				if m:
					cpu_usage[m.group(1)] = int(m.group(2))
		if args.type == "all":
			cpu = cpu_usage["system"] + cpu_usage["user"]
		else:
			cpu = cpu_usage[type]
		user_ticks = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
		print(float(cpu) / user_ticks)
	else:
		print(0)


def display_ip(container):
	detail = c.inspect_container(container)
	print(detail['NetworkSettings']['IPAddress'])


def display_memory(container):
	detail = c.stats(container)
	mem_stats = detail['memory_stats']
	return mem_stats


def display_network(container):
	detail = c.stats(container)
	network_stats = detail['network']
	return network_stats

def display_status(container):
	detail = c.inspect_container(container)
	state = detail["State"]
	if bool(state["Paused"]):
		print(1)  # Paused
	elif bool(state["Running"]):
		print(0)  # Running
	elif int(state["ExitCode"]) == 0:
		print(2)  # Stopped
	else:
		print(3)  # Crashed