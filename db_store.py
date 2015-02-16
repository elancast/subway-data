import datetime
import sqlite3

DELIM = '|'
DB = 'api_times.db'

class DBStore:
    def __init__(self):
        self._conn = sqlite3.connect(DB)

    def save_train_times(self, station_id, line, direction, times):
        times = DELIM.join(times)
        self._conn.execute(
            'INSERT INTO raw_train_times ' +
            ' (station_id, line, direction, scheduled_timestamps, iteration_timestamp) ' +
            'VALUES (?, ?, ?, ?, ?) ',
            (station_id, line, direction, times, self._get_now())
            )
        self._conn.commit()

    def save_leaving_time(self, station_id, line, direction, train_id, arrival_timestamp):
        self._conn.execute(
            'INSERT INTO leaving_times ' +
            ' (station_id, line, direction, train_id, arrival_timestamp) ' +
            'VALUES (?, ?, ?, ?, ?)',
            (station_id, line, direction, train_id, arrival_timestamp)
            )
        self._conn.commit()

    def save_new_train(self, line, direction):
        cursor = self._conn.cursor()
        cursor.execute(
            'INSERT INTO trains ' +
            ' (direction, line, timestamp) ' +
            'VALUES (?, ?, ?)',
            (direction, line, self._get_now())
            )

        id = cursor.lastrowid
        self._conn.commit()
        return id

    def get_latest_train_id(self, station, line, direction):
        if station == None: return None
        cursor = self._conn.execute(
            'SELECT max(arrival_timestamp), train_id ' +
            'FROM leaving_times ' +
            'WHERE station_id=? AND line=? AND direction=? ',
            (station, line, direction)
            )
        results = cursor.fetchone()
        return None if results == None else results[1]

    def get_last_times(self, station_id, line, direction):
        cursor = self._conn.execute(
            'SELECT max(iteration_timestamp), scheduled_timestamps ' +
            'FROM raw_train_times ' +
            'WHERE station_id=? AND line=? AND direction=? ',
            (station_id, line, direction)
            )
        results = cursor.fetchone()
        if results == None:
            return None
        return [] if results[1] == None else results[1].split(DELIM)

    def write_stops(self, train_id, line, stops):
        stops = map(lambda stop: '%s,%d' % (stop.id, stop.time), stops)
        if len(stops) == 0:
            self._conn.execute(
                'DELETE FROM api_times ' +
                'WHERE train_id=? ',
                (train_id,)
                )
        else:
            self._conn.execute(
                'REPLACE INTO api_times ' +
                ' (train_id, line, remaining_stops) ' +
                'VALUES (?, ?, ?) ',
                (train_id, line, DELIM.join(stops)),
                )
        self._conn.commit()

    def write_missing_stop(self, train_id, line, stop, time):
        self._conn.execute(
            'INSERT INTO api_leaving_times ' +
            ' (train_id, line, stop, departure) ' +
            'VALUES (?, ?, ?, ?) ',
            (train_id, line, stop, time),
            )
        self._conn.commit()

    def get_api_prev_stops(self, train_id):
        cursor = self._conn.execute(
            'SELECT remaining_stops FROM api_times ' +
            'WHERE train_id=? ',
            (train_id, )
            )
        results = cursor.fetchone()
        results = None if results == None else results[0]
        if not results:
            return None
        stops = results.split(DELIM)
        return map(lambda stop: stop.split(','), stops)

    def _get_now(self):
        return int(datetime.datetime.now().strftime('%s'))
