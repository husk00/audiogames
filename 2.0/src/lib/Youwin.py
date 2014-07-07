# Youwin.py

import bge
import Game
    
def main():
    keyboard = bge.logic.keyboard.events
    events = bge.events
    
    JUST_RELEASED = bge.logic.KX_INPUT_JUST_RELEASED

    
    if keyboard[events.SPACEKEY] == JUST_RELEASED or Game.user_presence == False:
        # go to the default starting scene
        bge.logic.getCurrentScene().replace('init')