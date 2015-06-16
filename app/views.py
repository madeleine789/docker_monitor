__author__ = 'mms'

from app import app
from flask import render_template
from monitor import stats, docker_stats


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')


@app.route('/system-info')
def system_info():
	info = docker_stats.system_wide_info()

	return render_template('system-info.html', info=info)


@app.route('/containers')
def containers():
	running = docker_stats.containers_with_status(status='Running')
	paused = docker_stats.containers_with_status(status='Paused')
	exited = docker_stats.containers_with_status(status='ExitCode')
	containers = docker_stats.containers()

	return render_template('containers.html', running=running, paused=paused, exited=exited, containers=containers)


@app.route('/containers/<id>')
def container(id):
	general = stats.general_info(id)
	cpu = stats.cpu_stats(id)
	memory = stats.memory_stats(id)
	network = stats.network_stats(id)
	processes = stats.processes_running(id)
	blkio = stats.blkio_stats(id)

	return render_template('container.html', id=id, general=general, cpu=cpu, blkio=blkio, memory=memory, network=network, processes=processes)

@app.route('/images')
def images():
	images = docker_stats.images()
	return render_template('images.html', images = images)