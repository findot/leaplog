# -*- coding: utf-8 -*-

# Bits of directory magic to get python to add platform specific leap libs path
# to the current path

from os.path import realpath, dirname
import platform, sys, os, json

top = dirname(dirname(realpath(__file__)))
os = platform.system().lower()
sys.path.insert(0, '{0}/leaplog'.format(top))
sys.path.insert(0, '{0}/lib/{1}'.format(top, os))

# "Standard" module starts here

from multiprocessing import Process, Queue
from .tracking import Tracker, Logger
from .tracking.data import Subject
from .System import System
from flask import Flask, request, render_template, jsonify, abort

system = System()
app = Flask(__name__)

OK = json.dumps({'success': True}), 200, {'ContentType': 'application/json'} 


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/subject', methods=['POST'])
def register_subject():
    if not request.form:
        abort(400)
    
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    system.subject = Subject(firstname, lastname)
    system.start_experiment()

    return OK


@app.route('/experiment/status')
def status_experiment():
    return jsonify(system.status)

@app.route('/experiment/start', methods=['POST'])
def start_experiment():
    system.start_experiment()
    return OK

@app.route('/experiment/stop', methods=['POST'])
def stop_experiment():
    system.stop_experiment()
    return OK


@app.route('/action/start', methods=['POST'])
def start_action():
    system.start_action()
    return OK

@app.route('/action/stop', methods=['POST'])
def stop_action():
    system.stop_action()
    return OK

@app.route('/action/remake')
def remake_action():
    system.remake_action()
    return  OK

@app.route('/action/next')
def next_action():
    system.next_action()
    return OK
