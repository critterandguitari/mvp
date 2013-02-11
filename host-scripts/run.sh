#!/bin/bash 
while : 
do 
    clear
    cd /home/pi
    python wait.py
    echo "Mounting usb drive.."
    if [ ! -d "/media/usbstick" ]; then
        sudo mkdir /media/usbstick
    fi
    sudo mount -t vfat -o uid=pi,gid=pi /dev/sda1 /media/usbstick
    echo "Loading MVP"
    if [ -d "/media/usbstick/pythonpi/midio/system/web" ]; then
        cd /media/usbstick/pythonpi/midio/system/web
        ./run.sh &
        cd ../
        sudo python main.py
    fi
    cd /home/pi
    echo "Stopping web server..."
    sudo killall -w python
    echo "Unmounting USB drive..."
    sudo umount /media/usbstick
done
