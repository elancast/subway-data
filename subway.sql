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
