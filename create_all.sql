DROP TABLE IF EXISTS replies;
CREATE TABLE replies (
  rid SERIAL PRIMARY KEY,
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
  item_id SERIAL PRIMARY KEY,
  aid VARCHAR,
  date_text VARCHAR,
  url VARCHAR
);

DROP TABLE IF EXISTS archive_metadata;
CREATE TABLE archive_metadata (
  last_full_refresh_date TIMESTAMP,
  last_partial_refresh_date TIMESTAMP,
  refresh_in_progress BOOLEAN DEFAULT FALSE
);

INSERT INTO archive_metadata(last_full_refresh_date, last_partial_refresh_date) VALUES ('2010-01-01', now());

DROP TABLE IF EXISTS nugs_items;
CREATE TABLE nugs_items(
  item_id SERIAL PRIMARY KEY,
  date_text VARCHAR,
  url VARCHAR
);

DROP TABLE IF EXISTS nugs_metadata;
CREATE TABLE nugs_metadata (
  last_refresh_date   TIMESTAMP,
  refresh_in_progress BOOLEAN DEFAULT FALSE
);

INSERT INTO nugs_metadata(last_refresh_date) VALUES ('2010-01-01');