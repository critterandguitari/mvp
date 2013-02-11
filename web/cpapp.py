import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))
import time
import glob
import json
import cherrypy
import urllib

# setup UDP socket for sending data to mvp program
import time
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

def get_immediate_subdirectories(dir) :
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

class Root():

    # /patch/patch-name  loads patch
    def get_patch(self, p):
        patch_path = '../../patches/'+p+'/'+p+'.py'
        patch = open(patch_path, 'r').read()
        self.send_command("setpatch," + p + "\n")
        return patch
    get_patch.exposed = True

    def send_command(self, data):
        global sock
        sock.sendto(data, (UDP_IP, UDP_PORT))
    send_command.exposed = True

    def save(self, name, contents):
        #save the patch
        p = name
        patch_path = '../../patches/'+p+'/'+p+'.py'
        with open(patch_path, "w") as text_file:
            text_file.write(contents)
        #then send reload command
        self.send_command("rlp\n")
        return "SAVED " + name
    save.exposed = True

    # returns list of all the patches
    def index(self):
        
        print "loading patches..."
        patches = []
        patch_folders = get_immediate_subdirectories('../../patches/')

        for patch_folder in patch_folders :
            patch_name = str(patch_folder)
            patch_path = '../../patches/'+patch_name+'/'+patch_name+'.py'
            patches.append(urllib.quote(patch_name))

        return json.dumps(patches)

    index.exposed = True


