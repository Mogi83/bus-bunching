
from .utils import distance
import numpy as np

class Bus:
    def __init__(self, world, start_stop):
        self.world = world
        self.position = np.array([0.0, 0.0])
        self.passengers = 0
        self.max_capacity = 10
        self.stopped = True
        self.current_speed = 0.0 #in m/s
        self.max_speed = 13.41 #30 mph
        self.acceleration = 0.7 #in m/s/s
        self.current_stop = start_stop
        self.braking_rng = np.random.default_rng()


    def move(self, stop):
        distance_to = distance(self.position[0], self.position[1], stop.location[0], stop.location[1])
        breaking_distance = (self.current_speed ** 2) / (2 * self.acceleration)
        buffer_distance = self.braking_rng.uniform(1.0, 5.0) #to add variaton between buses and drivers. in m.
        
        if (self.current_speed < self.max_speed) and (distance_to > (breaking_distance + buffer_distance)):
            self.current_speed += self.acceleration
        else:
            self.current_speed -= self.acceleration

        if (distance_to <= 0.05):
            unload_passengers(stop)

        

        #takes current x and y and increments them based on the target stop and in the future roads into consideration.
        #Use accleration above to make a speed ramp until max_speed then speed down until is stopped (when acceleration has made currentspeed 0)

    def load_passengers(self, stop):
        stop.loading = True
        stop.bus = True
        
    def unload_passengers(self):
        for passengers in self.passengers:
            if passenger.desired_stop == passenger.current_stop:
                #passenger.destory
                self.passenger -= 1

    def update(self):
        if self.passengers == 0:
            self.state = "idle"
        else:
            self.move()
            self.state = "motion"
        
            #set state to move!
        pass