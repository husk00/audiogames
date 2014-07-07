# ENDsoundengine.py

import bge
import Game
import GameLogic as gl
from OSC import OSCClient, OSCMessage, OSCBundle

gl.send_to = ('localhost', 7777 )

def sendOSCend():
        #
        client = OSCClient()
        msg = OSCMessage()
        # gl.client is a tuple in gl with ip and port
        address = "/game/end"
        msg.setAddress(address)
        msg.append(1)
        client.sendto(msg, gl.send_to)
        print('Send message example =', msg, "to ", gl.send_to)
        return
    
sendOSCend()