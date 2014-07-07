# PlayerSpot.py

import bge
from mathutils import Vector
import Game, Level
import math, mathutils
from ObjectBase import ObjectBase
import GameLogic as gl

class PlayerSpot(ObjectBase):
    def __init__(self):
        ObjectBase.__init__(self, 'spot-player')
        
    def handle_movement(self, player):
        vecx = player.worldPosition[0]
        vecy = player.worldPosition[1]
        self.worldPosition = (vecx, vecy, 2)

    def updates(self, player, spot):
        
        if player['IN']:
            if player.state == "BONUS":
                spot.energy = 10
            else:        
                spot.energy = 3
        else:
            spot.energy = 0
            
        #print("luz",spot.energy)
        #print("luz position",self.worldPosition)
        
    def main(self):
        scn = bge.logic.getCurrentScene()
        player = scn.objects["player"]
        spot = scn.objects["spot-player"]
        self.handle_movement(player)
        self.updates(player, spot)
        
             
        

        