#!/bin/bash 
while : 
do 
    clear
    cd /home/pi
    python wait.py
    echo "Mounting usb drive.."
    if [ ! -d "/media/usbdrive" ]; then
        sudo mkdir /media/usbdrive
    fi
    sudo mount -t vfat -o uid=pi,gid=pi /dev/usbdrive /media/usbdrive
    echo "Loading MVP"
    if [ -d "/media/usbdrive/mvp/web" ]; then
        cd /media/usbdrive/mvp/web
        ./run.sh &
        cd ../
        sudo python main.py
    fi
    cd /home/pi
    echo "Stopping web server..."
    sudo killall -w python
    echo "Unmounting USB drive..."
    sudo umount /media/usbdrive
done
