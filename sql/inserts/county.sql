DROP TABLE IF EXISTS core.county;

CREATE TABLE IF NOT EXISTS core.county (county_id varchar PRIMARY KEY, county_name varchar, county_state varchar, create_date date, current_flag boolean, removed_flag boolean, etl_job varchar, update_date date);

INSERT INTO core.county(county_id, county_name, county_state) VALUES(10001, 'Saint Louis City County', 'MO');