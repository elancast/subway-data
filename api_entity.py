import nyct_subway_pb2

RELEVANT_LINES = ['4', '5', '6']
STOP_ENDPOINTS = ['86 St', 'Astor Pl']

STOPS_FILE = 'data/stops.txt'

class StopsMetadata:
    def __init__(self):
        f = open(STOPS_FILE, 'r')
        lines = f.read().split('\n')
        f.close()

        # Index all stops by their names and ids
        # NOTE: This assumes all the stops I care about are numbers only
        self._by_name = {}
        self._by_id = {}
        for line in lines[1:-1]:
            parts = line.split(',')
            (id, name) = (parts[0], parts[2])

            if self._is_south_or_north(id):
                continue
            try:
                id = int(id)
            except:
                continue

            self._by_name[name] = int(id)
            self._by_id[str(id)] = name

    def print_relevant_stops(self):
        ids = map(lambda i: int(i), self._by_id.keys())
        ids.sort()
        for id in ids:
            print '(%d)  %s' % (id, self._by_id[str(id)])

    def is_relevant_stop(self, stop_id):
        if self._is_south_or_north(stop_id):
            stop_id = stop_id[:-1]
        return stop_id in self._by_id

    def get_stop_name(self, stop_id):
        dir = ''
        if self._is_south_or_north(stop_id):
            dir = '(' + stop_id[-1] + ') '
            stop_id = stop_id[:-1]
        name = self._by_id[stop_id]
        return dir + name

    def _is_south_or_north(self, id):
        return id[-1] == 'N' or id[-1] == 'S'

stops_metadata = StopsMetadata()

class APIStop:
    def __init__(self, stop):
        self.id = stop.stop_id
        stop_time = stop.departure if stop.departure.time else stop.arrival
        self.time = stop_time.time

    def is_relevant(self):
        return stops_metadata.is_relevant_stop(self.id)

    def __str__(self):
        return '%s\t%d' % (self.id, self.time)

class APIEntity:
    def __init__(self, entity):
        self._entity = entity

    def get_line(self):
        return self._entity.trip_update.trip.route_id

    def get_train_id(self):
        trip = self._entity.trip_update.trip
        extension = trip.Extensions[nyct_subway_pb2.nyct_trip_descriptor]
        return extension.train_id

    def is_relevant(self):
        return self.get_line() in RELEVANT_LINES

    """ Filters out any of the ones we don't care about - above 86 or below astor """
    def get_stops(self):
        all_stops = self._entity.trip_update.stop_time_update
        stops = map(lambda stop: APIStop(stop), all_stops)
        stops = filter(lambda stop: stop.is_relevant(), stops)
        stops.sort(lambda a, b: int(a.time - b.time))
        return stops
