import serial

MEASUREMENT_COMMAND = b'm'
SERIAL_DEVICE = '/dev/ttyUSB0'

def read_measurements():
    conn = serial.Serial(SERIAL_DEVICE, baudrate=9600, timeout=0)
    
    if not conn.isOpen():
        raise IOError("Could not open serial connection for interface: %s" % SERIAL_DEVICE)

    conn.write(MEASUREMENT_COMMAND)
    response = str(conn.read(7))

    measurements = response.split(' ')

