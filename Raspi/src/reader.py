import serial
import sqlite3
import time

MEASUREMENT_COMMAND = b'm'
SERIAL_DEVICE = '/dev/ttyUSB0'
DB_FILE = 'measurements.db'
DB_SCHEMA = 'src/schema.sql'
DB_INSERT = 'src/insert.sql'

def read_measurements():
    conn = serial.Serial(SERIAL_DEVICE, baudrate=9600, timeout=1)
    
    if not conn.isOpen():
        raise IOError("Could not open serial connection for interface: %s" % SERIAL_DEVICE)

    time.sleep(2.5)  # Make sure the connection is ready for use

    conn.write(MEASUREMENT_COMMAND)
    response = conn.read(7)

    conn.close()

    return response.decode().split(' ')


def create_db(db=None):
    with open(DB_SCHEMA, 'r') as schema_file:
        schema = schema_file.read()

    if db is None:
        db = sqlite3.connect(DB_FILE)
    cur = db.cursor()

    cur.executescript(schema)
    db.commit()
    db.close()


def save_measurement(name, value, date, db=None):
    with open(DB_INSERT, 'r') as insert_file:
        insert = insert_file.read()

    if db is None:
        db = sqlite3.connect(DB_FILE)
    cur = db.cursor()

    cur.execute(insert, (name, value, date))
    db.commit()
    db.close()

