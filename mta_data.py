import datetime
import time
import urllib2 as urllib

DIR = 'direction'
URL = 'http://apps.mta.info/trainTime/getTimesByStation.aspx?stationID=%d&time=%d'

def get_times(stations):
    now = int(datetime.datetime.now().strftime('%s'))
    station_times = {}
    for station in stations:
        times = _get_station_times(station, now)
        while len(times) == 0:
            time.sleep(1)
            print '== retrying for', station
            times = _get_station_times(station, now)
        station_times[station] = times
    return station_times

def _get_station_times(station, now):
    resp = urllib.urlopen(URL % (station, now))
    return _format_response(resp.read())

def _format_response(s):
    lines = s.split('\r\n')
    times = {}
    for line in lines:
        if not line.startswith(DIR):
            continue
        line = line[len(DIR):]
        direction = int(line[0])
        if not direction in times:
            times[direction] = {}

        line = line.replace("'", '')
        line = line[line.index('=') + 1:]
        parts = line.split(',')
        if len(parts) < 7:
            continue

        subway = parts[0]
        if not subway in times[direction]:
            times[direction][subway] = []

        time = int(parts[1])
        if not time:
            time = int(parts[2])
        times[direction][subway].append(time)
    return times

if __name__ == '__main__':
    print get_times([626, 629])
