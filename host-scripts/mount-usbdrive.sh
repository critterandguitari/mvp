#!/bin/bash 
cd /home/pi
python wait.py
echo "Mounting usb drive.."
if [ ! -d "/media/usbdrive" ]; then
    sudo mkdir /media/usbdrive
fi
sudo mount -t vfat -o uid=pi,gid=pi /dev/usbdrive /media/usbdrive
