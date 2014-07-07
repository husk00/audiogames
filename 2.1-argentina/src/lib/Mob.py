# Mob.py

import bge
from mathutils import Vector

import Game, Level
from ObjectBase import ObjectBase

class Mob(ObjectBase):
    def __init__(self):
        id = 'mob'+ str(Level.id_ball)
        ObjectBase.__init__(self, id)
        self['mob'] = True
        self.is_alive = True

        self.last_direction_update = 0.0
        self.WALK_SPEED = 100.0
        self.DIRECTION_UPDATE_FREQUENCY = 0.05
        self.DIRECTION_UPDATE_STRENGTH = .2

    def handle_direction_update(self):
        if Game.time - self.last_direction_update > self.DIRECTION_UPDATE_FREQUENCY:
            self.applyRotation(Vector([0,0, bge.logic.getRandomFloat()*self.DIRECTION_UPDATE_STRENGTH-self.DIRECTION_UPDATE_STRENGTH/2])*self.worldOrientation)
            self.last_direction_update = Game.time
            
    def handle_collision_avoidance(self):
        ray = self.rayCastTo(self.worldPosition + Vector([0,1,0]) * self.worldOrientation)
        if ray:
            if ray.get('ground') or ray.get('mob'):
                self.applyRotation([0,0, 3.14], True)

    def handle_movement(self):
        self.worldLinearVelocity = Vector([0, -self.WALK_SPEED * Game.time_since_last_frame, 0]) * self.worldOrientation
        
    def handle_attack(self):
        ray = self.rayCastTo(self.worldPosition + Vector([0,0.5,0]) * self.worldOrientation)
        if ray:
            if ray.get('player'):
                ray.hp -= 10

    def main(self):
        self.handle_direction_update()
        #self.handle_collision_avoidance()
        #self.handle_movement()
        #self.handle_attack()
