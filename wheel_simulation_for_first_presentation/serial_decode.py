import serial
import time
# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = '/dev/tty.usbmodem1101'
# SERIAL_PORT = 'COM6'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 115200

def bytes_to_int(bytes):
    # bytes.remove(b'\r\n')
    try:
        res = b''
        for i in bytes:
            if i != b'\n' and i != b'\r' and chr(i).isnumeric():
                res += i.to_bytes(1, 'big')
        if res == b'\n' or res == b'\r' or res == b'':
            return 0    
        print(res)
        return int(res.decode('utf-8'))
    except:
        return 0

dataset_x = []
dataset_y = []

def main():
    flag = True
    ser = serial.Serial(SERIAL_PORT, SERIAL_RATE, bytesize=8, parity=serial.PARITY_NONE)
    while True:
        # using ser.readline() assumes each line contains a single reading
        # sent using Serial.println() on the Arduino
        reading = ser.readline()

        # reading is a string...do whatever you want from here
        res = bytes_to_int(reading)
        print(res)
        if flag:
            dataset_x.append(res)
            flag = False
        else:
            dataset_y.append(res)
            flag = True

        if len(dataset_x) == 5000:
            break

    ser.close()

    with open('data_x.txt', 'w') as f:
        for item in dataset_x:
            f.write("%s\n" % item)

    with open('data_y.txt', 'w') as f:
        for item in dataset_y:
            f.write("%s\n" % item)

def normalise_data():
    with open('data_x.txt', 'r') as f:
        data_x = f.readlines()
    with open('data_y.txt', 'r') as f:
        data_y = f.readlines()
    
    data_x = [int(x.strip()) for x in data_x]
    data_y = [int(y.strip()) for y in data_y]

    max_x = max(data_x)
    min_x = min(data_x)
    max_y = max(data_y)
    min_y = min(data_y)

    data_x = [(x - min_x) / (max_x - min_x) for x in data_x]
    data_y = [(y - min_y) / (max_y - min_y) for y in data_y]

    with open('data_x_normalised.txt', 'w') as f:
        for item in data_x:
            f.write("%s\n" % item)

    with open('data_y_normalised.txt', 'w') as f:
        for item in data_y:
            f.write("%s\n" % item)

MIN_X = -4095
MAX_X = 4095
FLAG = True
timer = time.time()
def live_transmission():
    global FLAG, timer, last_iter
    if time.time() - timer < 0.1:
        timer = time.time()
        return 0
    ser = serial.Serial(SERIAL_PORT, SERIAL_RATE, bytesize=8, parity=serial.PARITY_NONE)
    reading = ser.readline()
    print(reading)
    if FLAG:
        FLAG = False
        return 0
    res = bytes_to_int(reading)
    return ((res - MIN_X) / (MAX_X - MIN_X)) - 0.35

if __name__ == "__main__":
    print(live_transmission())