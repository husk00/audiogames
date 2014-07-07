# Player.py

import bge
from mathutils import Vector
import Game, Level
import math, mathutils
from ObjectBase import ObjectBase
import GameLogic as gl
from OSC import OSCClient, OSCMessage, OSCBundle
from SoundObject import SoundObject

gl.send_to = ('localhost', 9000 )  # envio al soundengine

class Player(ObjectBase):
    def __init__(self):
        ObjectBase.__init__(self, 'player')
        self['player'] = True
        self.hp = 100
        self.is_alive = True
        self.sens = 0.8
        self.speed = 0.05 
        self['bpm'] = Game.bpm_base
        self['state'] = "NORMAL"   # 'NORMAL', 'BONUS', 'DEAD'
        self['location'] = "IN"    # 'IN', 'OUT', 'BORDER'
        self['IN'] = True
        self['OUT'] = False
        self['BORDER'] = False
        self['points_cnt'] = 0
        self['bonus_cnt'] = 0
        self['malus_cnt'] = 0
        self['last_collision_id'] = None  
        self["oriinicial"] = Game.ori_adj
        self['ori'] = None
        self['tracker_n'] = None
        self['tracker_s'] = None
    
    def handle_movement(self):
        keyboard = bge.logic.keyboard.events
        events = bge.events
        # to move the player with arrow keys
        if keyboard[events.UPARROWKEY]:
            self.applyMovement([0,self.speed,0], True)
        if keyboard[events.DOWNARROWKEY]:
            self.applyMovement([0,-self.speed,0], True)
        if keyboard[events.LEFTARROWKEY]:
            self.applyRotation([0,0,self.speed*self.sens], True)
        if keyboard[events.RIGHTARROWKEY]:
            self.applyRotation([0,0,-self.speed*self.sens], True)
            
    def handle_tracker(self):
        
        def scale(val, src, dst):
                #Scale the given value from the scale of src to the scale of dst.
                scale = ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]
                return scale
            
        if Game.kinects == '2':
            if self['tracker_n'] and self['tracker_s'] != None:
                nx,ny = self['tracker_n']
                sx,sy = self['tracker_s']
                #print("------", round(ny, 3), round(sy, 3))
                #print("------", round(nx, 3), round(sx, 3))
                sinalfa = math.sin(math.radians(25.4))
                sinbeta = math.sin(math.radians(64.6))
                #mapeo y
                ny = round(scale (ny, (0.5,4.62),(4.12,0.0)),3)
                sy = round(scale (sy, (0.5,4.62),(-4.12,0.0)),3)
                # correccion y mapeo de la x
                scale_nx = sinalfa*(4.63-abs(ny))/sinbeta +0.3
                nx = round(scale (nx, (0.84,0.05),(-scale_nx,scale_nx)),3)
                scale_sx = sinalfa*(4.63-abs(sy))/sinbeta +0.3
                sx = round(scale (sx, (0.05,0.84),(-scale_sx,scale_sx)),3)
                vecy = ny+sy
                if vecy > 0: 
                    vecx = nx
                else:
                    vecx = sx
                #print(vecx,vecy)
                self.worldPosition = (vecx, vecy, self.worldPosition[2])
            else:
                #print("no detecto el tracker, usa las teclas")
                pass
               
        if Game.kinects == '1':
            if self['tracker_n'] != None:
                nx,ny = self['tracker_n']
                #print(nx,ny)
                sinalfa = math.sin(math.radians(25.4))
                sinbeta = math.sin(math.radians(64.6))
                # mapeo y
                ny = round(scale (ny, (0.3,4.63),(-0.5,-4.70)),3)
                # correccion y mapeo de la x
                scale_nx = sinalfa*(abs(ny))/sinbeta 
                nx = round(scale (nx, (0.89,0.015),(-scale_nx,scale_nx)),3)
                
                vecy = ny
                vecx = nx
                #print(vecx,vecy)
                self.worldPosition = (vecx, vecy, self.worldPosition[2])

            else:
                #print("no detecto el tracker, usa las teclas")
                pass
        
        
    def rotacion(self):
        if self['ori'] != None:
            #print("inicial :",self['oriinicial'],"  ori: ", self['ori'])
                            # orientacion inicial del movil, pasada a quaternions
            rot_ini_q = mathutils.Quaternion((0.0,0.0,1.0), math.radians(float(self['oriinicial'])))
                            # rotacion recibida del movil, pasada a quaternions
            rot_rec_q = mathutils.Quaternion((0.0,0.0,1.0), math.radians(float(self['ori'])))
                            # rotacion incremental del movil (remapeo)
            rot_q = rot_rec_q.rotation_difference(rot_ini_q)
                            # rotacion actual del objeto en quaternions
                            # rotob_q= player.localOrientation.to_quaternion()
                            # interpolacion
                            # rota_q = rotob_q.slerp(rot_q, 0.5)
                            # asignacion de la rotacion
            self.localOrientation = rot_q  * mathutils.Quaternion((0.0,0.0,1.0),math.radians(-9))
        else:
            #print("no detecto orientacion, usa las teclas")
            pass
            
    def detectposition(self):
        if self['IN'] and self['BORDER'] or self['OUT'] and self['BORDER'] :
            if self['location'] != 'BORDER':
                self['location'] = 'BORDER'
                self.send_osclocation()
        if self['OUT'] and not self['BORDER']:
            if self['location'] != 'OUT':
                self['location'] = 'OUT'
                self.send_osclocation()
        if self['IN'] and not self['BORDER']:
            if self['location'] != 'IN':
                self['location'] = 'IN'
                self.send_osclocation()
                
    def send_osclocation(self):
        #cuando hay un cambio de situacion se envia
        #           /player/in    /player/out      /player/border
        client = OSCClient()
        msg = OSCMessage()
        # gl.client is a tuple in gl with ip and port
        if self['location'] == 'IN':
            address = "/player/in"
        elif self['location'] == 'OUT':
            address = "/player/out"
        else:
            address = "/player/border"
        msg.setAddress(address)
        msg.append(1)
        client.sendto(msg, gl.send_to)
        print(msg)
        #print('Send message example =', msg, "to ", gl.send_to)
        return 
            
    def update_bonus_bpm(self):
        if self['bonus_cnt'] == 0 and self['state'] != 'NORMAL':
            self['state'] = 'NORMAL'
            #self.send_oscstate()
            self['bpm'] = Game.bpm_base
        elif self['bonus_cnt'] < Game.bonus_duration/4 and self['bonus_cnt'] != 0:
            #self['bpm'] -= ((Game.bpm_base)/(Game.bonus_duration/4))  # ARREGLAR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if self['bpm'] > Game.bpm_base:
                #self['bpm'] -= 0.01
                self['bpm'] -= Game.bpm_base/(Game.bonus_duration/4)
                pass

    def update_bonus_counter(self):
        if self['bonus_cnt'] > 0:
            self['bonus_cnt'] -= 1
            
    def updates(self):
        self.update_bonus_bpm()
        self.update_bonus_counter()
        self.detectposition()
        
    def main(self):
        self.handle_movement()
        self.updates()
        self.handle_tracker()
        self.rotacion()
        
        #check hit points
        if self.hp <= 0:
             self.is_alive = False
             
        

        