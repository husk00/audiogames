# readpresence.py
import GameLogic
import socket
import OSC
import Game
import bge

def receive_osc(data, port):
    try:
        # getting first data value from buffer
        data, port = GameLogic.socket.recvfrom(1024)
 
        # keep trying to get new data until buffer is empty
        try:
            trash = data
            while True:
                data = trash
                trash, port = GameLogic.socket.recvfrom(1024)
                # print deleted values
                #print ("trash= ", trash)
        except:
            # we force this exception to happen
            # that way we know the buffer is empty
            pass
 
    except Exception as E:
        pass
 
    return data

def main():
    # Get controller and owner
    controller = GameLogic.getCurrentController()
    owner = controller.owner
    
    # Set init
    ip = '127.0.0.1'  ### escucha router
    
    if owner.name == "control_init":
        port = 8887
    else: 
        port = 8886
        
    data = 0
    
        # Connect Blender only one time
    if not owner['connected']:
        
        owner['connected'] = True
        print ("Blender Connected user_presence ", owner.name)
        print(port)
        GameLogic.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        GameLogic.socket.bind((ip, port))
        GameLogic.socket.setblocking(0)
        GameLogic.socket.settimeout(0.02)

     
    # If Blender connected, get osc 
    else:
        # Get hand wii osc from pd
        data = receive_osc(data, port)
        #print(data)
        if data != 0:
            d = OSC.decodeOSC(data)
            #print(" decoded: ",d)
            if d[0] == "/game/user_presence":
                print(d[2])
                if d[2] == 2:
                    Game.user_presence = True
            if d[0] == "/game/start":
                print (d[2])
                if d[2] == 1:
                    Game.start = True