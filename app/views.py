__author__ = 'mms'

from app import app
from flask import render_template
from monitor import stats, docker_stats


@app.route('/')
@app.route('/index')
def index():
	render_template('index.html')


@app.route('/system-info')
def system_info():
	info = docker_stats.system_wide_info()
	return render_template('system-info.html', info=info)


@app.route('/containers')
def containers():
	running = docker_stats.containers_with_status(status='Running')
	paused = docker_stats.containers_with_status(status='Paused')
	exited = docker_stats.containers_with_status(status='ExitCode')
	return render_template('containers.html', running=running, paused=paused, exited=exited)


@app.route('/container/<id>')
def container(id):
	general = stats.general_info(id)
	cpu = {}
	memory = {}
	status = {}
	processes = stats.processes_running(id)

	return render_template('container.html', id=id, general=general, cpu=cpu, memory=memory, status=status, processes=processes)