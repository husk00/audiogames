#jaula-change.py

import bge, bpy
import Player
from Level import Level

def main():
    cont = bge.logic.getCurrentController()
    obj = cont.owner
    
    print("hola", obj.name)
    
    touch = obj.sensors["Touch"]
    replace = obj.actuators["replacemesh"]
    
    if touch.positive:
        scn = bge.logic.getCurrentScene()
        player = scn.objects["player"]
        
        if player['last_collision_id'] != obj['id']: 
            player['last_collision_id'] = obj['id']
            print("last_col ",obj['id'])
            print("hola", obj.name)
            
    if obj["kinects"] == True:
        print(obj["kinects"])   
        # change mesh  
        print("chage jaula")  
        cont.activate(replace)