import serial

# connect to Track
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = None)



def resetLanes():
    command = 'om0'+'\r\n'
    newcommand = command.encode('ascii')
    ser.write(newcommand)
    return ser.readline()

# toggle lanes   
def toggleLane(x):
    command = 'om' + str(x) +'\r\n'
    newcommand = command.encode('ascii')
    ser.write(newcommand)
    return ser.readline()

def laneStatus(x):
    return True



def getResults():
    command = 'rg'+'\r\n'
    newcommand = command.encode('ascii')
    ser.write(newcommand)
    return ser.readline().decode().split()

def forceEnd():
    command = 'ra'+'\r\n'
    newcommand = command.encode('ascii')
    ser.write(newcommand)
    return ser.readline().decode().split()

def prevResults():
    command = 'rp'+'\r\n'
    newcommand = command.encode('ascii')
    ser.write(newcommand)
    return ser.readline().decode().split()



# Turn on Set Place   indicatorto #
def setPlace():
    command = 'op2'+'\r\n'
    newcommand = command.encode('ascii')
    ser.write(newcommand)
    return True



# Reverse Lane order
def reverseLaneOrder():
    command = 'ov1'+'\r\n'
    newcommand = command.encode('ascii')
    ser.write(newcommand)
    return True
