#groundcollisionborder.py

import bge

def main():
    cont = bge.logic.getCurrentController()
    obj = cont.owner
    
    touch = obj.sensors["Touch"]
    
    scn = bge.logic.getCurrentScene()
    player = scn.objects["player"]
    
    if touch.positive:
        player['BORDER'] = True
    else:
        player['BORDER'] = False 