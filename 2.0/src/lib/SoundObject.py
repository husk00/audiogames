# SoundObject.py

import bge, bpy
from mathutils import Vector

import Game, Level
from ObjectBase import ObjectBase

class SoundObject(ObjectBase):
    def __init__(self):
        id = 'soundobject'+ str(Level.id_ball)
        ObjectBase.__init__(self, id)
        
        self['soundobject'] = True
        self.is_alive = True
        
        snd = Game.snd_objs[int(Level.id_ball)]
        
        self['id'] = Level.count
        self.puntoscomer = snd[0] 
        self.puntoschocar = snd [1]
        self.rol = snd[2]
        self.bpm = snd[3]
        self.hexcolor = snd[4]
        self.octava = snd[5]
        self.nota = snd[6]
        self.alcance = snd[7]
        
        self['is_out'] = False
        self['out_cnt'] = Game.out_cnt
            
    def main(self):
        pass