# -*- coding: utf-8 -*-

import click
import sqlite3
import sys

from utils import db_path
from os.path import dirname, realpath, exists
from . import app, system

def assert_initialized():
    if not exists(db_path):
        print('Please initialize the database before to proceed.')
        sys.exit(1)

@click.group()
def cli():
    pass


@cli.command()
@click.option('--interface', default='0.0.0.0', help='The interface on which the server shall listen')
@click.option('--port', default=8000, help='The port on which the server shall listen')
def serve(interface, port):
    assert_initialized()
    system.start()
    app.run(host=interface, port=port)


@cli.command()
def initdb():
    '''Prepair the database for logging'''
    pwd = dirname(__file__)
    db = sqlite3.connect(db_path)
    with open('{0}/tracking/data/sql/schema.sql'.format(pwd), 'r') as schema:
        statements = schema.read()
        for statement in statements.split(';'):
            db.execute(statement)
    db.commit()


@cli.command()
@click.option('--format', default='csv', help='The destination format')
@click.option('--destination', default='data', help='The destination file')
def export(format):
    assert_initialized()
    raise NotImplementedError()


@cli.command()
def analyse():
    assert_initialized()
    print("pass")


if __name__ == '__main__':
    cli()
