CREATE TABLE measurements
(property TEXT, value REAL, date TEXT);

CREATE TABLE properties
(name TEXT, unit TEXT);

INSERT INTO properties
VALUES ('Temperature', 'C');

INSERT INTO properties
VALUES ('Humidity', '%');
