import numpy as np

class Stop:
    def __init__(self, world):
        self.world = world
        self.location = np.array([0.0, 0.0])
        self.passengers_waiting = 0 
        self.loading = False #are we loading passengers?
        self.bus = False #is a bus here?
        self.rng = np.random.default_rng()
        
    def update(self):
        if self.rng.random() < 0.1:
            self.world.passengers.append(Passenger())
            self.passengers_waiting += 1
            print("New passenger spawned!")