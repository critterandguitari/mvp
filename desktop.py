import os
import pygame
import time
import random
import serial
import fullfb
import glob
import hardware
import imp
import sys

from pygame.locals import *

def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]


# add the line init_uart_clock=13020833 to change 115200 into .5Mbs 
#print "init serial port"
#serialport = serial.Serial("/dev/ttyAMA0", 115200)

pygame.init()
 
# Set the height and width of the screen
print "opening frame buffer"
size=[656,416]
screen=pygame.display.set_mode(size)
 

print "loading patches..."
patches = []
patch_folders = get_immediate_subdirectories('../patches/')

for patch_folder in patch_folders :
    patch_name = str(patch_folder)
    patch_path = '../patches/'+patch_name+'/'+patch_name+'.py'
    print patch_path
    patches.append(imp.load_source(patch_name, patch_path))

# set initial patch
patch = None 
num = 4
patch = patches[num]

# run setup functions if patches have them
for patch in patches :
    try :
        patch.setup()
    except AttributeError :
        print "no setup found"
        continue 

# flush serial port
#serialport.flushInput()

#create mvp object
mvp = hardware.HardwareInput()

buf = ''
line = ''

#mvp.clear_flags()

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
OSDBG = (0,0,255, 100)

font = pygame.font.SysFont(None, 24)
notemsg = font.render('...', True, WHITE, OSDBG)

while 1:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if pygame.key.get_pressed()[K_ESCAPE]:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[K_RETURN]:
                mvp.note_on = True
            if pygame.key.get_pressed()[K_SPACE]:
                mvp.clear_screen = True
            if pygame.key.get_pressed()[K_RIGHT]:
                mvp.next_patch = True
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #print serialport.inWaiting()    
    # get serial line and parse it, TODO hmmm could this miss lines?  (only parses most recent, but there could be more in serial buffer)

    if mvp.next_patch: 
        num += 1
        if num == len(patches) : num = 0
        patch = patches[num]

    if mvp.clear_screen:
        screen.fill( (random.randint(0,255), random.randint(0,255), random.randint(0,255))) 
        #screen.fill( (0,0,0)) 
        pygame.display.flip()


    patch.draw(screen, mvp)
    
    #osd
    pygame.draw.rect(screen, OSDBG, (0, screen.get_height() - 40, screen.get_width(), 40))
    font = pygame.font.SysFont(None, 24)
    text = font.render('patch: ' + str(patch.__name__), True, WHITE, OSDBG)
    text_rect = text.get_rect()
    text_rect.x = 50
    text_rect.centery = screen.get_height() - 20
    screen.blit(text, text_rect)
   
    if mvp.note_on :
        notemsg = font.render('note on', True, WHITE, OSDBG)
    
    text_rect = notemsg.get_rect()
    text_rect.x = screen.get_width() - 100
    text_rect.centery = screen.get_height() - 20
    screen.blit(notemsg, text_rect)

    
    pygame.display.flip()

    # clear all the events
    mvp.clear_flags()
    time.sleep(.01)

time.sleep(1)


print "Quit"
