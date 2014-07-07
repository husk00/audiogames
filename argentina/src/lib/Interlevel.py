# Interlevel.py

import bge

import time, Game

import GameLogic as gl
  
def main():
    
    #sendOSClevel()
    scn = bge.logic.getCurrentScene()
    text = scn.objects["levelnumber"]
    text.text = str(Game.currentlevel)
    
    keyboard = bge.logic.keyboard.events
    events = bge.events
    
    if keyboard[events.AKEY] or Game.start == True:
        # go to the default starting scene
        Game.start = False
        bge.logic.getCurrentScene().replace('level')