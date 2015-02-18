-- raw train times:
--   [ station ID, train time, iteration timestamp ]
-- leaving times:
--   [ station ID, train ID, train time, direction ]
-- train IDs:
--   [ train ID, direction ]

CREATE TABLE if not exists raw_train_times (
  station_id INT NOT NULL,
  line TEXT NOT NULL,
  direction INT NOT NULL,
  scheduled_timestamps TEXT NOT NULL,
  iteration_timestamp INT NOT NULL
);

CREATE TABLE if not exists leaving_times (
  station_id INT NOT NULL,
  line TEXT NOT NULL,
  direction INT NOT NULL,
  train_id INT NOT NULL,
  arrival_timestamp INT NOT NULL
);

-- Everything in this table originates at 86 or astor depending on direction
CREATE TABLE if not exists trains (
  id INTEGER PRIMARY KEY,
  line TEXT NOT NULL,
  direction INT NOT NULL,
  timestamp INT NOT NULL
);

CREATE TABLE if not exists api_times (
  train_id TEXT NOT NULL PRIMARY KEY,
  line TEXT NOT NULL,
  remaining_stops TEXT NOT NULL -- stop_id,time|stop_id,time|...
);

CREATE TABLE if not exists api_leaving_times (
  id INT NOT NULL,
  mta_train_id TEXT NOT NULL,
  line TEXT NOT NULL,
  stop TEXT NOT NULL,
  departure INT NOT NULL
);

CREATE TABLE if not exists api_train_ids (
  id INTEGER PRIMARY KEY,
  train_id TEXT NOT NULL,
  timestamp INT NOT NULL
);
