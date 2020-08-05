from flask import Flask, request, render_template
from app.db import *
from app.nmea import parse_messages
from flask import jsonify

def init():
    init_db();

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
        datapoint = get_last_datapoint()

        return jsonify(
            seen_at=datapoint['created_at'],
            latitude=datapoint['latitude'],
            longitude=datapoint['longitude'],
            ground_speed=datapoint['ground_speed'],
            heading=datapoint['heading']
        )

    @app.teardown_appcontext
    def cleanup(exception):
        close_connection(exception)

    return app