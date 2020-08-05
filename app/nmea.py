
def parse_messages(str, separator='\n'):
    raw_messages = str.split(separator)
    messages = {}

    for index, message in enumerate(raw_messages):
        parts = message.strip().split(',')

        sentance_type = parts[0][1:]

        if sentance_type not in messages:
            messages[sentance_type] = []

        if sentance_type == 'GPGGA':
            messages[sentance_type].append(GPGGAMessage(
                message_string = message,
                timestamp = parts[1],
                latitude = parts[2],
                latitude_direction = parts[3],
                longitude = parts[4],
                longitude_direction = parts[5],
                quality = parts[6],
                satellites = parts[7],
                hdop = parts[8],
                altitude = parts[9],
                altitude_units = parts[10],
                geoidal_separation = parts[11],
                geoidal_separation_units = parts[12],
                correction_age = parts[13],
                correction_station_id = parts[14],
                checksum = '123',
            ))
        elif sentance_type == 'GPVTG':
            messages[sentance_type].append(GPVTGMessage(
                message_string = message, 
                track_made_good_one = parts[1], 
                track_made_good_one_relativity = parts[2], 
                track_made_good_two = parts[3], 
                track_made_good_two_relativity = parts[4], 
                speed_over_ground_one = parts[5], 
                speed_over_ground_one_units = parts[6], 
                speed_over_ground_two = parts[7], 
                speed_over_ground_two_units = parts[8], 
                checksum = parts[9]
            ))
        else:
            messages[sentance_type].append(NMEAMessage(message))

    return messages

class NMEAMessage:
    def __init__(self, message_string):
        self.message_string = message_string

    def __repr__(self):
        return self.message_string

class GPGGAMessage(NMEAMessage):
    def __init__(self, message_string, timestamp, latitude, latitude_direction, longitude, 
        longitude_direction, quality, satellites, hdop, altitude, altitude_units, 
        geoidal_separation, geoidal_separation_units, correction_age, 
        correction_station_id, checksum):

        NMEAMessage.__init__(self, message_string)

        self.timestamp = timestamp
        self.latitude = latitude
        self.latitude_direction = latitude_direction
        self.longitude = longitude
        self.longitude_direction = longitude_direction
        self.quality = quality
        self.satellites = satellites
        self.hdop = hdop
        self.altitude = altitude
        self.altitude_units = altitude_units
        self.geoidal_separation = geoidal_separation
        self.geoidal_separation_units = geoidal_separation_units
        self.correction_age = correction_age
        self.correction_station_id = correction_station_id
        self.checksum = checksum

    def get_decimal_lat_lng(self):

        latitude = {
            'degrees': int(self.latitude[0:2]),
            'minutes': int(self.latitude[2:4]),
            'seconds': float(self.latitude[4:])
        }

        latitude['decimal'] = sum([
            latitude['degrees'],
            latitude['minutes'] / 60,
            (latitude['seconds'] * 60) / 3600
        ])

        if self.latitude_direction == 'S':
            latitude['decimal'] = -1 * latitude['decimal']

        longitude = {
            'degrees': int(self.longitude[0:3]),
            'minutes': int(self.longitude[3:5]),
            'seconds': float(self.longitude[5:])
        }   

        longitude['decimal'] = sum([
            longitude['degrees'],
            longitude['minutes'] / 60,
            (longitude['seconds'] * 60) / 3600
        ])

        if self.longitude_direction == 'W':
            longitude['decimal'] = -1 * longitude['decimal']

        return { 'latitude': latitude['decimal'], 'longitude': longitude['decimal'] }

class GPVTGMessage(NMEAMessage):
    def __init__(self, message_string, track_made_good_two, track_made_good_two_relativity,
        track_made_good_one, track_made_good_one_relativity, speed_over_ground_one, 
        speed_over_ground_one_units, speed_over_ground_two, speed_over_ground_two_units, 
        checksum):

        NMEAMessage.__init__(self, message_string)

        self.track_made_good_one = track_made_good_one 
        self.track_made_good_one_relativity = track_made_good_one_relativity 
        self.track_made_good_two = track_made_good_two 
        self.track_made_good_two_relativity = track_made_good_two_relativity 
        self.speed_over_ground_one = speed_over_ground_one 
        self.speed_over_ground_one_units = speed_over_ground_one_units
        self.speed_over_ground_two = speed_over_ground_two 
        self.speed_over_ground_two_units = speed_over_ground_two_units
        self.checksum = checksum

    def get_knots_per_hour(self):
        if self.speed_over_ground_one_units == 'N':
            return self.speed_over_ground_one
        elif self.speed_over_ground_two_units == 'N':
            return self.speed_over_ground_two

        return None

    def get_kilometers_per_hour(self):
        if self.speed_over_ground_one_units == 'K':
            return self.speed_over_ground_one
        elif self.speed_over_ground_two_units == 'K':
            return self.speed_over_ground_two

        return None

    def get_magnetic_heading(self):
        if self.track_made_good_one_relativity == 'M':
            return self.track_made_good_one
        elif self.track_made_good_two_relativity == 'M':
            return self.track_made_good_two

        return None

    def get_true_heading(self):
        if self.track_made_good_one_relativity == 'T':
            return self.track_made_good_one
        elif self.track_made_good_two_relativity == 'T':
            return self.track_made_good_two

        return None