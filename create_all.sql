CREATE TABLE replies (
  rid INTEGER PRIMARY KEY AUTOINCREMENT,
  id VARCHAR,
  body VARCHAR,
  author VARCHAR,
  post_date TIMESTAMP,
  date_requested TIMESTAMP,
  reply_type VARCHAR
);

CREATE TABLE archive_items (
  item_id INTEGER PRIMARY KEY AUTOINCREMENT,
  aid VARCHAR,
  date_text VARCHAR,
  url VARCHAR
);

DROP TABLE IF EXISTS archive_metadata;
CREATE TABLE archive_metadata (
  last_full_refresh_date TIMESTAMP,
  last_partial_refresh_date TIMESTAMP
);

INSERT INTO archive_metadata(last_full_refresh_date, last_partial_refresh_date) VALUES ('2010-01-01', current_date);

