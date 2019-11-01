# -*- coding: utf-8 -*-

# Bits of directory magic to get python to add platform specific leap libs path
# to the current path

from os.path import realpath, dirname
import platform, sys, os

top = dirname(dirname(realpath(__file__)))
os = platform.system().lower()
sys.path.insert(0, '{0}/lib/{1}'.format(top, os))

# "Standard" module starts here

from multiprocessing import Process, Queue
from .tracking import Tracker, Logger
from flask import Flask, escape, request, render_template

initialized = False
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def setup():
    # type: () -> Queue
    commander = Queue()
    messenger = Queue()
    
    tracker = Tracker(commander, messenger)
    tracker_process = Process(target=Tracker.track, args=(tracker,))

    logger = Logger(messenger)
    logger_process = Process(target=Logger.log, args=(logger,))

    return commander

