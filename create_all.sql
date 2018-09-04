DROP TABLE IF EXISTS replies;
CREATE TABLE replies (
  rid INTEGER PRIMARY KEY AUTOINCREMENT,
  id VARCHAR,
  body VARCHAR,
  author VARCHAR,
  post_date TIMESTAMP,
  request_date TIMESTAMP,
  reply_type VARCHAR,
  reply_date TIMESTAMP
);

DROP TABLE IF EXISTS archive_items;
CREATE TABLE archive_items (
  item_id INTEGER PRIMARY KEY AUTOINCREMENT,
  aid VARCHAR,
  date_text VARCHAR,
  url VARCHAR
);

DROP TABLE IF EXISTS archive_metadata;
CREATE TABLE archive_metadata (
  last_full_refresh_date TIMESTAMP,
  last_partial_refresh_date TIMESTAMP,
  refresh_in_progress INTEGER DEFAULT 0
);

INSERT INTO archive_metadata(last_full_refresh_date, last_partial_refresh_date) VALUES ('2010-01-01', current_date);

DROP TABLE IF EXISTS nugs_items;
CREATE TABLE nugs_items(
  item_id INTEGER PRIMARY KEY AUTOINCREMENT,
  date_text VARCHAR,
  url VARCHAR
);

DROP TABLE IF EXISTS nugs_metadata;
CREATE TABLE nugs_metadata (
  last_refresh_date   TIMESTAMP,
  refresh_in_progress INTEGER DEFAULT 0
);

INSERT INTO nugs_metadata(last_refresh_date) VALUES ('2010-01-01');