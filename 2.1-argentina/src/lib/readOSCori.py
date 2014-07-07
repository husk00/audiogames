import GameLogic
import socket
import OSC
import Game, Level
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
    # Set init
    ip = '127.0.0.1'  ### escucha a routerOSC.pd
    port = 8888
    data = 0
    # Get controller and owner
    controller = GameLogic.getCurrentController()
    owner = controller.owner
        # Connect Blender only one time
    if not owner['connected']:
        
        owner['connected'] = True
        print ("Blender Connected Ori")
     
        GameLogic.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        GameLogic.socket.bind((ip, port))
        GameLogic.socket.setblocking(0)
        GameLogic.socket.settimeout(0.02)
     
    # If Blender connected, get osc 
    else:
        # Get hand wii osc from pd
        
        data = receive_osc(data, port)
        if data != 0:
            d = OSC.decodeOSC(data)
            #print(d)
            
            if Game.kinects == "1":
                    
                if d[2][12] == "/norte":
                    nx,ny =d[2][13],d[2][14]
                    #print("tracker norte",nx,ny)
                    scn = bge.logic.getCurrentScene()
                    player = scn.objects["player"]
                    player['tracker_n'] = nx,ny
                
                if d[2][8] == "/ori":
                    ori,ox,oz =d[2][9], d[2][10], d[2][11]
                    scn = bge.logic.getCurrentScene()
                    player = scn.objects["player"]
                    player['ori'] = ori
                   
            if Game.kinects == "2":
            
                if d[2][8] == "/ori":
                    ori,ox,oz =d[2][9], d[2][10], d[2][11]
                    scn = bge.logic.getCurrentScene()
                    player = scn.objects["player"]
                    player['ori'] = ori
                    
                if d[2][12] == "/norte":
                    nx,ny =d[2][13],d[2][14]
                    scn = bge.logic.getCurrentScene()
                    player = scn.objects["player"]
                    player['tracker_n'] = nx,ny
                
                if d[2][15] == "/sur":
                    sx,sy =d[2][16],d[2][17]
                    scn = bge.logic.getCurrentScene()
                    player = scn.objects["player"]
                    player['tracker_s'] = sx,sy
                    
                
                          