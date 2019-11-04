# -*- coding: utf-8 -*-

import click
from . import app

@click.command
@click.option('--interface', default='0.0.0.0', help='The interface on which the server shall listen')
@click.option('--port', default=8000, help='The port on which the server shall listen')
def serve(host, port):
    app.run(host=host, port=port)


@click.command
@click.option('--format', default='csv', help='The destination format')
@click.option('--destination', default='data', help='The destination file')
def export(format):
    raise NotImplementedError()


@click.command
def analyse():
    pass
