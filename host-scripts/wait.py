import os
import time
import serial
import sys


# add the line init_uart_clock=13020833 to change 115200 into .5Mbs 
serialport = serial.Serial("/dev/ttyAMA0", 115200)


# flush serial port
serialport.flushInput()

buf = ''
line = ''

def parse_line(line) : 
    array = line.split(',')
    if len(array) == 1:
        if array[0] == "sd" :
            os.system('shutdown -h now')

    if len(array) == 1:
        if array[0] == "rst" :
            return True
        else :
            return False
    else :
        return False
 
print "Insert USB disk and press button."
while 1:
    #print serialport.inWaiting()    
    if serialport.inWaiting() > 0:
        buf = buf + serialport.read(serialport.inWaiting())
        if '\n' in buf :
            lines = buf.split('\n')
            for l in lines :
                if parse_line(l):
                    time.sleep(1)
                    sys.exit()
            buf = lines[-1]


time.sleep(1)
sys.exit()

