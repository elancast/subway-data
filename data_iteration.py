from constants import Direction, DirectionNames, Line, Station, StationNames, Subway
from db_store import DBStore
from mta_data import get_times

# The 6 stops everywhere, so just hard code to one of its lines XD
ALL_STATIONS = Line[Direction.UPTOWN][Subway.L6]

# Max amount of time the scheduled time can vary by for us to think it's the same
MAX_SIMILAR_TIME = 60

def print_departure(station, line, direction, train, time):
    print DirectionNames[direction], line, 'departed', StationNames[station],
    print '  (%d)' % train

def save_all_times(db, times):
    for station in times:
        for direction in times[station]:
            for line in times[station][direction]:
                its_times = times[station][direction][line]
                db.save_train_times(
                    station,
                    line,
                    direction,
                    map(lambda t: str(t), its_times),
                    )

"""
  Train has departed if the newest leaving time is closer to previous time #2
  compared to previous time #1. Assuming that times are sorted by recency.
"""
def has_departed(previous, current):
    # Probably missing some cases with this but w/e idc
    if len(current) < 1 or len(previous) < 1:
        return False

    newest = int(current[0])
    old_1 = int(previous[0])
    old_2 = 0 if len(previous) < 2 else int(previous[1])

    diff_1 = abs(old_1 - newest)
    diff_2 = abs(old_2 - newest)
    return diff_2 < diff_1 and diff_2 < MAX_SIMILAR_TIME

def get_previous_station(station, line, direction):
    ordering = Line[direction][line]
    for i in range(len(ordering)):
        if ordering[i] == station:
            break
    return None if i == 0 else ordering[i - 1]

def get_train_id(db, station, line, direction):
    prev_station = get_previous_station(station, line, direction)
    train_id = db.get_latest_train_id(prev_station, line, direction)
    if train_id == None:
        train_id = db.save_new_train(line, direction)
    return train_id

def handle_departure(db, station, line, direction, time):
    train_id = get_train_id(db, station, line, direction)
    print_departure(station,line, direction, train_id, time)
    db.save_leaving_time(station, line, direction, train_id, time)

def store_departed_trains(db, times):
    for direction in Line:
        for line in Line[direction]:
            for station in Line[direction][line]:
                try:
                    new_times = times[station][direction][line]
                except:
                    new_times = []
                old_times = db.get_last_times(
                    station,
                    line,
                    direction
                    )

                if has_departed(old_times, new_times):
                    handle_departure(
                        db,
                        station,
                        line,
                        direction,
                        old_times[1],
                        )


def main():
    db = DBStore()
    times = get_times(ALL_STATIONS)
    store_departed_trains(db, times)
    save_all_times(db, times)

main()
