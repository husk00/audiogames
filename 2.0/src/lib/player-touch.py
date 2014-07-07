# player-touch.py

import bge

def main():
    print("hola")
    cont = bge.logic.getCurrentController()
    obj = cont.owner
    
    scn = bge.logic.getCurrentScene()
    player = scn.objects["player"]
    
    interior = obj.sensors["interior"]
    exterior = obj.sensors["exterior"]
    borde = obj.sensors["borde"]
    
    if interior.positive:
        print("interior")
        obj['posi'] = "int"
    if exterior.positive:
        print("exterior")
        obj['posi'] = "ext"
    if borde.positive:
        print("borde")
        obj['posi'] = "borde"
        
        
        
            