import click
from pathlib import Path, PurePath
from flask import g, current_app as app
from flask.cli import with_appcontext
import sqlite3

def init_app(app):
    app.teardown_appcontext(close_connection)
    app.cli.add_command(init_db)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE_PATH'])
    db.row_factory = sqlite3.Row
    return db

@click.command('init-db')
@with_appcontext
def init_db():
    path = Path(app.config['DATABASE_PATH'])
    if not path.parent.exists():
        path.parent.mkdir();

    path.touch()
    db = get_db()
    with app.open_resource(app.config['DATABASE_SCHEMA_PATH'], mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    click.echo('Initialized the database.')

def insert_data_point(latitude, longitude, heading = None, ground_speed = None):
    db = get_db()
    db.cursor().execute("INSERT INTO gps_data (`latitude`, `longitude`, `heading`, `ground_speed`) VALUES (?, ?, ?, ?)", (latitude, longitude, heading, ground_speed))
    db.commit()

def get_last_datapoint():
    db = get_db()
    cur = db.execute("SELECT * FROM gps_data ORDER BY id DESC LIMIT 1,1")
    rv = cur.fetchall()
    cur.close()
    return rv[0] if rv else None

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()