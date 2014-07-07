# Level.py
import bge, math, random
import Game
from Player import Player
from SoundObject import SoundObject
import GameLogic as gl
from OSC import OSCClient, OSCMessage, OSCBundle
import math, mathutils

from PlayerSpot import PlayerSpot

import readOSCori

gl.send_to = ('localhost', 7777 )
id_ball = 0  #para circular por las bolas que se crean
count = 0

class Level():
    def __init__(self):
        # setup jaula
        scn = bge.logic.getCurrentScene()
        tablero = scn.objects["Empty-tableros"]
        if Game.kinects == "1":
            tablero.worldPosition = (0,0,-0.15)
        else:
            tablero.worldPosition = (0,12,-0.15)
            
        # create player
        self.player = Player()
        if Game.kinects == "1":
            self.player.worldPosition = (0,0,0)
        else:
            self.player.worldPosition = (0,-4.6,0)
            
        self.playerspot = PlayerSpot() 
        self.playerspot.worldPosition = self.player.worldPosition
        self.playerspot.worldPosition[2] = 2
           
        self.soundobjects = []
            
        #while not player['IN']:
        self.handle_player() # to refresh player position before adding soundobjects 
        print(self.player.worldPosition)
        # Populate the level with soundobjects acording to current level dictionary
        #ll = {"1":[(1,2),(2,1)], "2":[(3,3),(5,2)],"3":[(5,1),(6,1),(4,1),(3,1)], "4":[(6,3),(3,3)]}
        global count
        count = 0
        self.soundobjects = []
        #print(Game.ll)
        for j in Game.ll[str(Game.currentlevel)]:
            #print("bola ", j[0]," repetida: ", j[1]," veces") 
            for i in range(int(j[1])):
                global id_ball
                id_ball = j[0]
                self.soundobjects.append(SoundObject())
                obj = self.soundobjects[count]
                #get random position
                pos = self.getemptyposition()
                obj.worldPosition = pos
                obj.worldLinearVelocity = (0.0,0.0,0.0)
                print("obj id ",count," id_ball", id_ball)
                #print(r, theta, pos)
                count = count + 1
                print("count",count)

        # avisos pd
        self.send_init()
        self.enumerateSndObjs()
        
    def getemptyposition(self):
        # function to get an empty position to deploy balls without collisions
        
        #def getpos():
        def getpos_argentina():
            center=4.62207  # board center (distance from kinect_N)
            
            ## un cuadrado desde la posicion de esq2-1 hasta esq5-1
            ## restandoles 30cm de ancho de las bolas
            
            esq2 = bpy.data.objects["esq2-1"].worldPosition
            esq5 = bpy.data.objects["esq5-1"].worldPosition
            pos = random.randrange(esq2[0],esq5[0]), random.randrange(esq2[1],esq5[1])
                
            return pos
        
        # function to get an empty position to deploy balls without collisions
        def getpos():
            center=4.62207  # board center (distance from kinect_N)
            if Game.kinects == "1":
                theta = random.randrange(1,180)
                r = random.randrange(10,120)/100
                pos = mathutils.Vector((r * math.cos(math.radians(theta)), r * math.sin(math.radians(theta)) - center, 0))
                if pos[1] < 0.5-center:
                    pos[1] = 0.5-center
                #print("pos ",pos)
            else:
                theta = random.randrange(1,360)
                r = random.randrange(50,160)/100
                pos = mathutils.Vector((r * math.cos(math.radians(theta)), r * math.sin(math.radians(theta)) - center, 0))
                #print("pos ",pos)
            return pos
        
        list = []   #lista de todos los objetos en el tablero
        for obj in self.soundobjects:
            list.append(obj) 
        list.append(self.player)  
        emptypos = False
        
        while emptypos == False:
            pos = getpos()
            emptypos = True
            for i in list:
                if (i.worldPosition - pos).magnitude < 0.4:
                    print("recolocando")
                    emptypos = False
        return pos
        
    def check_collision(self): 
        
        for soundobject in self.soundobjects:
            if soundobject['id'] == self.player['last_collision_id']:
                id_obj = soundobject
        
        if id_obj['soundobject']:
            if id_obj.rol == 'BONUS':
                self.player['state'] = 'BONUS'
                self.player['points_cnt'] += id_obj.puntoscomer
                self.player['bonus_cnt'] = Game.bonus_duration
                self.player['bpm'] += Game.bpm_bonus
                self.player["last_collision_id"] = None
                id_obj['is_out'] = True
                id_obj.worldPosition = (19000,-1,0)
                id_obj.worldLinearVelocity = (0,0,0)
            if id_obj.rol == 'MALUS':
                if self.player['state'] == 'NORMAL':
                    self.player['points_cnt'] += id_obj.puntoscomer
                    self.player.is_alive = False
                    self.player['state'] = 'DEAD'                     
                if self.player['state'] == 'BONUS':
                    self.player['points_cnt'] += id_obj.puntoschocar
                    self.player['state'] = 'NORMAL'
                    self.player['bpm'] = Game.bpm_base
                    self.player['bonus_cnt'] =  0
                    id_obj['is_out'] = True
                    id_obj.worldPosition = (19000,-1.5,0)
                    id_obj.worldLinearVelocity = (0,0,0)
                    # bring bonus back to game
                    for i in self.soundobjects:
                        #print("eo ",i.name) 
                        if i.name == 'soundobject8': 
                            i['out_cnt'] = 1
                            #print("changed")
                self.player["last_collision_id"] = None
            if id_obj.rol == 'NEUTRA':
                if self.player['state'] == 'BONUS':
                    self.player['points_cnt'] += id_obj.puntoscomer
                    self.player["last_collision_id"] = None
                    id_obj.endObject()
                    self.send_destroy(id_obj['id'])
                    
                    self.soundobjects.remove(id_obj)
                    if self.checkwin():
                        Game.currentlevel += 1
                        if Game.currentlevel > len(Game.ll):
                            Game.currentlevel = 1
                            print("YOU WIN---------")
                            self.sendOSCwin()
                            bge.logic.getCurrentScene().replace('youwin')
                        else:
                            print("level-up----------------------------", Game.currentlevel)
                            self.sendOSCnextlevel()
                            bge.logic.getCurrentScene().replace('interlevel')
                if self.player['state'] == 'NORMAL':
                    self.player['points_cnt'] += id_obj.puntoschocar  
                    self.send_choque()
                    self.player["last_collision_id"] = None
                    
    def handle_soundobjects(self):
        # update or delete mob entities
        for soundobject in self.soundobjects:
            #print("queda un obj ",soundobject['id'])
            if soundobject.is_alive:
                soundobject.main()
            else:
                soundobject.endObject()
                self.soundobjects.remove(soundobject)
            if soundobject['is_out']:
                soundobject['out_cnt'] -= 1
                if soundobject['out_cnt'] == 0:
                    soundobject['is_out'] = False
                    if soundobject.name == "soundobject0":
                        pos = self.getemptyposition()
                        soundobject.worldPosition = pos
                        soundobject.worldLinearVelocity = (0.0,0.0,0.0)
                    if soundobject.name == "soundobject8":
                        pos = self.getemptyposition()
                        soundobject.worldPosition = pos
                        soundobject.worldLinearVelocity = (0.0,0.0,0.0)
                    soundobject['out_cnt'] = Game.out_cnt                    
                    
    
    def enumerateSndObjs(self):
        #print(self.soundobjects[2].bpm)
        #print(Game.ll[str(Game.currentlevel)] )
        cont=0
        for j in self.soundobjects :
            id =j['id']
            nota= j.nota    
            octava = j.octava
            bpm = j.bpm
            alcance = j.alcance
            cr = id, nota, octava, bpm, alcance
            self.send_osccreation(cr)
            self.send_play()
            cont +=1
     
    def send_osccreation(self, lista):
        # crea los objetos en el sound engine
        client = OSCClient()
        msg = OSCMessage()
        # gl.client is a tuple in gl with ip and port
        address = "/game/create"
        msg.setAddress(address)
        msg.append(lista)
        client.sendto(msg, gl.send_to)
        #print('Send message example =', msg, "to ", gl.send_to)
        return
    
    def send_play(self):
        # da play al soundengine
        client = OSCClient()
        msg = OSCMessage()
        # gl.client is a tuple in gl with ip and port
        address = "/game/play"
        msg.setAddress(address)
        msg.append(0)
        client.sendto(msg, gl.send_to)
        #print('Send message example =', msg, "to ", gl.send_to)
        return
    
    def send_stop(self):
        # da stop al soundengine
        client = OSCClient()
        msg = OSCMessage()
        # gl.client is a tuple in gl with ip and port
        address = "/game/stop"
        msg.setAddress(address)
        msg.append(0)
        client.sendto(msg, gl.send_to)
        #print('Send message example =', msg, "to ", gl.send_to)
        return
    
    def send_calambrazo(self):
        # envia el calambrazo
        client = OSCClient()
        msg = OSCMessage()
        # gl.client is a tuple in gl with ip and port
        address = "/player/calambrazo"
        msg.setAddress(address)
        msg.append(0)
        client.sendto(msg, gl.send_to)
        #print('Send message example =', msg, "to ", gl.send_to)
        return
    
    def send_init(self):
        #
        client = OSCClient()
        msg = OSCMessage()
        # gl.client is a tuple in gl with ip and port
        address = "/game/init"
        msg.setAddress(address)
        msg.append(0)
        client.sendto(msg, gl.send_to)
        #print('Send message example =', msg, "to ", gl.send_to)
        return
    
    def sendOSCwin(self):
        #
        client = OSCClient()
        msg = OSCMessage()
        # gl.client is a tuple in gl with ip and port
        address = "/game/win"
        msg.setAddress(address)
        msg.append(0)
        client.sendto(msg, gl.send_to)
        #print('Send message example =', msg, "to ", gl.send_to)
        return
        
    def sendOSCnextlevel(self):
        #
        client = OSCClient()
        msg = OSCMessage()
        # gl.client is a tuple in gl with ip and port
        address = "/game/nextlevel"
        msg.setAddress(address)
        msg.append(Game.currentlevel)
        client.sendto(msg, gl.send_to)
        #print('Send message example =', msg, "to ", gl.send_to)
        return
    
    def sendOSCgameover(self):
        #
        client = OSCClient()
        msg = OSCMessage()
        # gl.client is a tuple in gl with ip and port
        address = "/game/over"
        msg.setAddress(address)
        msg.append(0)
        client.sendto(msg, gl.send_to)
        #print('Send message example =', msg, "to ", gl.send_to)
        return
    
    def send_destroy(self,id):
        #
        client = OSCClient()
        msg = OSCMessage()
        # gl.client is a tuple in gl with ip and port
        address = "/game/sndobj/destroy"
        msg.setAddress(address)
        msg.append(id)
        client.sendto(msg, gl.send_to)
        #print('Send message example =', msg, "to ", gl.send_to)
        return    
    

    def send_choque(self):
        #
        client = OSCClient()
        msg = OSCMessage()
        # gl.client is a tuple in gl with ip and port
        address = "/player/choque"
        msg.setAddress(address)
        msg.append(0)
        client.sendto(msg, gl.send_to)
        #print('Send message example =', msg, "to ", gl.send_to)
        return
            
    def checkwin(self):
        win = True
        for i in self.soundobjects:
            if i.rol == 'NEUTRA':
                win = False
        print("win ",win)
        return win
    
    def handle_player(self):
        if self.player['location'] == 'OUT':
            Game.timewithoutplayer -= 1
            if Game.timewithoutplayer == 0:
                bge.logic.getCurrentScene().replace('game over')
        else:
            Game.timewithoutplayer = 1200
        
        # update the player, or call game over scene
        if self.player.is_alive:
            self.player.main()
            self.playerspot.main()
        else:
            bge.logic.getCurrentScene().replace('game over')
            self.sendOSCgameover()
   
    def send_oscbundle(self):
        # send a bundle with current bpm and polar coordinates of 
        # sound-objects relative to player
        #            /game/bpm
        client = OSCClient()
        bpm = OSCMessage()     
        bpm.setAddress("/game/bpm")
        bpm.append(self.player['bpm'])   
        bundle = OSCBundle()
        bundle.append(bpm)
        #            /game/sndobj/id-bola (ang, mod)  
        scn = bge.logic.getCurrentScene()
        play = scn.objects["player"]
        
        for ball in self.soundobjects:
            ballpos = ball.worldPosition
            vect = mathutils.Vector((0,1))
            dist = play.getVectTo(ballpos)[0]
            vect2 = play.getVectTo(ballpos)[2].to_2d()
            angle = math.degrees(-vect.angle_signed(vect2))
            #print("angle ", angle, "distancia ",dist)
            data = (angle, dist)
            # append data to bundle
            msg = OSCMessage()
            tag = "/game/sndobj/position/" + str(ball['id'])
            msg.setAddress(tag)
            msg.append(data)
            bundle.append(msg)
            #print(msg)
        #gl.client is a tuple in gl with ip and port
        client.sendto(bundle, gl.send_to)
        
    def main(self):
        marcador1 = "points {} bonus {} malus {} bpm {}".format(self.player['points_cnt'],self.player['bonus_cnt'],self.player['malus_cnt'],self.player['bpm'])
        #print(marcador1)
        scn = bge.logic.getCurrentScene()
        text = scn.objects["marcador"]
        text.text = marcador1

        marcador2 = "level {}".format(str(Game.currentlevel))
        text = scn.objects["marcador-level"]
        text.text = marcador2
        
        cam = scn.objects["Empty.camera"]
        cam.worldPosition = self.player.worldPosition
        cam.localOrientation = self.player.localOrientation
        
        if self.player['last_collision_id'] != None:
            #print("collision con id: ",self.player['last_collision_id'])
            self.check_collision()
        
        self.handle_player()
        self.handle_soundobjects()
        self.send_oscbundle()
            
      
def init(cont):
    cont.owner['time'] += Game.time
    Game.main()
    readOSCori.main()
    cont.owner['scene'] = Level()
    cont.script = 'Level.main'

def main(cont):
    Game.main()
    cont.owner['scene'].main()