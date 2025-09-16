import numpy as np
import pygame as pyg

class Stop:
    def __init__(self, x, y, world=None):
        self.location = np.array([x, y], dtype=float)
        self.passengers_waiting = 0
        self.loading = False
        self.bus = False
        self.rng = np.random.default_rng()
        self.world = world
        self.connections = []

    def update(self):
        #Am I handling passenger spawnning here or within the passenger class?
        if self.rng.random() < 0.1:
            self.world.passengers.append(None) #should be a new passenger.
            self.passengers_waiting += 1
            print("New passenger spawned!")

    def connect(self, target_stop):
        if target_stop not in self.connections:
            self.connections.append(target_stop)

    def disconnect(self, target_stop):
        if target_stop in self.connections:
            self.connections.remove(target_stop)

    
    def draw(self, screen):
        pyg.draw.circle(screen, (255, 255, 255), self.location.astype(int), 10)
