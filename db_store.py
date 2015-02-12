import datetime
import sqlite3

DELIM = '|'

class DBStore:
    def __init__(self):
        self._conn = sqlite3.connect('times.db')

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

    def _get_now(self):
        return int(datetime.datetime.now().strftime('%s'))
