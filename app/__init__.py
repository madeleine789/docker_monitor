__author__ = 'mms'

from flask import Flask

app = Flask(__name__)
from app import views
from monitor import docker_stats, stats
