from flask import Flask, request, render_template
from app.db import *
from app.nmea import parse_messages
from flask import jsonify
from datetime import datetime, timedelta

def init():
    init_db();

def format_record(record):
    return {
        'seen_at': record['created_at'],
        'latitude': record['latitude'],
        'longitude': record['longitude'],
        'ground_speed': record['ground_speed'],
        'heading': record['heading']
    }


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route("/")
    def index():
        return render_template('map.html')

    @app.route("/data", methods=['POST'])
    def data_points():
        messages = parse_messages(request.data.decode("utf8"))

        if 'GPGGA' in messages:
            latLon = messages['GPGGA'][0].get_decimal_lat_lng()
            args = [latLon['latitude'],latLon['longitude']]

            if 'GPVTG' in messages:
                gpvtg = messages['GPVTG'][0]
                args.append(gpvtg.get_true_heading())
                args.append(gpvtg.get_kilometers_per_hour())
            
            insert_data_point(*args)

            return "Datapoint inserted!" 
        else:
            return "No GPGGA message found."

    @app.route("/data/current", methods=['GET'])
    def current_data_point():
        return jsonify(format_record(get_last_datapoint()))

    @app.route("/data/last_five_minutes", methods=['GET'])
    def datapoints_since():
        now = datetime.utcnow()
        five_minutes = timedelta(minutes=5)
        datapoints = []
        five_minutes_ago = (now - five_minutes).strftime('%Y-%m-%d %H:%M:%S')
        records = get_datapoints_since(five_minutes_ago)

        if records != None:
            for record in records:
                datapoints.append(format_record(record))

        return jsonify(datapoints)

    @app.teardown_appcontext
    def cleanup(exception):
        close_connection(exception)

    return app