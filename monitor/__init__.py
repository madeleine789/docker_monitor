__author__ = 'mms'

from monitor import docker_stats
from monitor import stats

from docker import Client
client = Client(base_url='unix://var/run/docker.sock', version='1.9', timeout=10)