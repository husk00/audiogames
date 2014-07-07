#soundcollision.py

import bge

def main():
    cont = bge.logic.getCurrentController()
    obj = cont.owner
    
    touch = obj.sensors["Touch"]
    replace = obj.actuators["replacemesh"]
    
    if touch.positive:
        scn = bge.logic.getCurrentScene()
        player = scn.objects["player"]
        
        if player['last_collision_id'] != obj['id']: 
            player['last_collision_id'] = obj['id']
            print("last_col ",obj['id'])
            
        # change mesh    
        """cont.activate(replace)
        if int(replace.mesh.name) >= 9:
            nextmesh = str(3)
        else:
            nextmesh = str(int(replace.mesh.name)+1)
        replace.mesh = nextmesh"""

        
            
