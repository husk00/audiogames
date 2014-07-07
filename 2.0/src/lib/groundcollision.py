#groundcollision.py

import bge

def main():
    cont = bge.logic.getCurrentController()
    obj = cont.owner
    touch = obj.sensors["Touch"]
    
    scn = bge.logic.getCurrentScene()
    player = scn.objects["player"]
    
    if obj.name == "suelo-interior" or obj.name == "suelo-interior2":
        obj['id'] = 90
    if obj.name == "suelo-borde" or obj.name == "suelo-borde2":
        obj['id'] = 91
    if obj.name == "suelo-exterior" or obj.name == "suelo-exterior2":
        obj['id'] = 92
 
    if touch.positive:
        print("hola")
        if obj['id'] == 90:
            player['location'] = "IN"
            print(player['location'])
        if obj['id'] == 91:
            player['location'] = "OUT"
            print(player['location'])
        if obj['id'] == 92:
            player['location'] = "BORDER"
            print(player['location'])


        
            
