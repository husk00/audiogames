# marcador.py
import bge
import Game

def main():
    scn = bge.logic.getCurrentScene()
    
    marcador1 = Game.marcador1
    #print(marcador1)
    text = scn.objects["marcador"]
    text.text = marcador1
    
    marcador2 = "level {}".format(str(Game.currentlevel))
    #print(marcador2)
    text = scn.objects["marcador-level"]
    text.text = marcador2
    
main()
        