__author__ = 'mms'

from flask import Flask
app = Flask(__name__)

from app import views

from docker import Client
client = Client(base_url='unix://var/run/docker.sock', version='1.9', timeout=10)
