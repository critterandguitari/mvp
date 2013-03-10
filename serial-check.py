import os
import time
import serial




# add the line init_uart_clock=13020833 to change 115200 into .5Mbs 
print "init serial port"
serialport = serial.Serial("/dev/ttyAMA0", 115200)


# flush serial port
serialport.flushInput()

buf = ''
line = ''
error = ''

while 1:
    #print serialport.inWaiting()    
    if serialport.inWaiting() > 0:
        buf = buf + serialport.read(serialport.inWaiting())
        if '\n' in buf :
            lines = buf.split('\n')
            for l in lines :
                print l
            buf = lines[-1]

time.sleep(1)


print "Quit"
