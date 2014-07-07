# Interlevel.py

import bge, bpy
import Game

import GameLogic as gl
from OSC import OSCClient, OSCMessage, OSCBundle

gl.send_to = ('localhost', 7777 )

        
def sendOSClevel():
    # envia el level
    client = OSCClient()
    msg = OSCMessage()
    # gl.client is a tuple in gl with ip and port
    address = "/game/level"
    msg.setAddress(address)
    msg.append(Game.currentlevel)
    client.sendto(msg, gl.send_to)
    #print('Send message example =', msg, "to ", gl.send_to)
    return

    
def main():
    
    sendOSClevel()
        
    scn = bge.logic.getCurrentScene()
    text = scn.objects["levelnumber"]
    text.text = str(Game.currentlevel)
    
    keyboard = bge.logic.keyboard.events
    events = bge.events
    
    if keyboard[events.SPACEKEY] or Game.start:
        # go to the default starting scene
        Game.start = False
        bge.logic.getCurrentScene().replace('level')