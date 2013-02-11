import os
import pygame
import time
import random
import serial
import fullfb
import glob

def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]


#add the line init_uart_clock=2441406  to /boot/config.txt to make 38400 into 31250
# or add the line init_uart_clock=13020833 to change 115200 into .5Mbs 
print "init serial port"
serialport = serial.Serial("/dev/ttyAMA0", 115200)

print "opening frame buffer"
screen = fullfb.init()

print "loading patches..."
import imp
patches = []
patch_folders = get_immediate_subdirectories('../patches/')

for patch_folder in patch_folders :
    patch_name = str(patch_folder)
    patch_path = '../patches/'+patch_name+'/'+patch_name+'.py'
    print patch_path
    patches.append(imp.load_source(patch_name, patch_path))

# run setup functions if patches have them
for patch in patches :
    try :
        patch.setup()
    except AttributeError :
        print "not setup found"
        continue 


# set initial patch
patch = None 
patch = patches[0]
print len(patches)
num = 0

serialport.flushInput()

class HardwareInput:
    def parse_serial(self, line):
        return

    def clear_flags(self):
        return 

mvp = HardwareInput()

mvp.size = 1

while 1:

    time.sleep(.02)
    mvp.size += 1
    if mvp.size > 250 :
        mvp.size = 0
        num += 1
        if num == len(patches) : num = 0
        patch = patches[num]



    patch.draw(screen, mvp)
    pygame.display.flip()
   

time.sleep(1)


print "Quit"
