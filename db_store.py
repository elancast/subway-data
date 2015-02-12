import datetime
import sqlite3

class DBStore:
    def __init__(self):
        self._conn = sqlite3.connect('times.db')

    def save_train_times(self, station_id, direction, times):
        self._conn.execute(
            'INSERT INTO raw_train_times ' +
            ' (station_id, direction, scheduled_timestamps, iteration_timestamp) ' +
            'VALUES (?, ?, ?, ?) ',
            (station_id, direction, times, self._get_now())
            )
        self._conn.commit()

    def save_leaving_time(self, station_id, direction, train_id, arrival_timestamp):
        self._conn.execute(
            'INSERT INTO leaving_times ' +
            ' (station_id, direction, train_id, arrival_timestamp) ' +
            'VALUES (?, ?, ?, ?)',
            (station_id, direction, train_id, arrival_timestamp)
            )
        self._conn.commit()

    def save_new_train(self, direction):
        cursor = self._conn.cursor()
        cursor.execute(
            'INSERT INTO trains ' +
            ' (direction, timestamp) ' +
            'VALUES (?, ?)',
            (direction, self._get_now())
            )

        id = cursor.lastrowid
        self._conn.commit()
        return id

    def get_last_times(self, station_id, direction):
        cursor = self._conn.execute(
            'SELECT max(iteration_timestamp), scheduled_timestamps ' +
            'FROM raw_train_times ' +
            'WHERE station_id=? AND direction=? ',
            (station_id, direction)
            )
        results = cursor.fetchone()
        return None if results == None else results[1]

    def _get_now(self):
        return int(datetime.datetime.now().strftime('%s'))
