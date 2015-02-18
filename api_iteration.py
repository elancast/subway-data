import datetime
from google.transit import gtfs_realtime_pb2
import time
import urllib

from api_entity import APIEntity, stops_metadata
from db_store import DBStore
import nyct_subway_pb2

URL = 'http://datamine.mta.info/mta_esi.php?key=%s&feed_id=1'

db = DBStore()

def get_api_key():
    f = open('.secret.shh', 'r')
    key = f.read().strip()
    f.close()
    return key

def get_latest_feed():
    feed = gtfs_realtime_pb2.FeedMessage()
    response = urllib.urlopen(URL % get_api_key())
    feed.ParseFromString(response.read())
    print 'read feed with %d entities' % len(feed.entity)
    return feed

def get_latest_feed_aggressively():
    try:
        return get_latest_feed()
    except:
        print 'had exception! retrying...'
        time.sleep(2)
        return get_latest_feed_aggressively()

def write_leaving_times(curr):
    prev_stops = db.get_api_prev_stops(curr.get_train_id())
    if prev_stops == None:
        return

    curr_stops = curr.get_stops()
    if len(prev_stops) < len(curr_stops):
        print 'wtf? we gained a stop somehow?', curr.get_train_id()
        return
    if len(prev_stops) == len(curr_stops):
        return

    missing_stops = prev_stops[0 : len(prev_stops) - len(curr_stops)]
    missing_stops.reverse()

    train_id = db.get_api_train_id(curr.get_train_id())
    print ' ', curr.get_line(), 'departures for train %d:' % train_id
    for stop in missing_stops:
        db.write_missing_stop(
            curr.get_train_id(),
            curr.get_line(),
            stop[0],
            stop[1]
            )
        print ' ', '  ', stops_metadata.get_stop_name(stop[0])

def write_stops(entity):
    db.write_stops(
        entity.get_train_id(),
        entity.get_line(),
        entity.get_stops()
        )

def process_entity(entity):
    if not entity.is_relevant():
        return 0
    write_leaving_times(entity)
    write_stops(entity)
    return 1

def main():
    print '=== BEGINNING ITERATION %s ===' %  datetime.datetime.now().strftime('%d %b %H:%M')
    feed = get_latest_feed()
    num_wrote = 0
    for entity in feed.entity:
        ent = APIEntity(entity)
        num_wrote += process_entity(ent)
    print 'wrote %d trains' % num_wrote
    print ''

if __name__ == '__main__':
    main()
