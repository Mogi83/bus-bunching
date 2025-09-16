
from utils import distance
import numpy as np
import pygame as pyg
import math

meters_per_pixel = 0.2

# Missing Functionalty:
# Loading passengers
# Updating when a new stop is added
# Data output like time to stop, 
# A way of applying treatments (and introducing more chaos)
# Force busses to stick to roads instead of visually faking it.

class Bus:
    def __init__(self, start_stop):
        if start_stop != None:
            self.position = np.array(start_stop.location, dtype= float)
        else:
            self.position = np.array([0.0, 0.0], dtype= float)
        
        self.passengers = 0
        self.max_capacity = 10
        self.stopped = True
        self.current_speed = 0.0 # px/s
        self.max_speed = 13.41 / meters_per_pixel  #13.41 m/s == 30mph /p 
        self.acceleration = 0.7 / meters_per_pixel  #in m/s/s /p 
        self.current_stop = start_stop
        self.braking_rng = np.random.default_rng()
        self.brake_buffer = self.braking_rng.uniform(1.0, 5.0) #to add variaton between buses and drivers. in m. THis will need adjustment to match the meters/pixel standard.
        self.color1 = self.braking_rng.uniform(75,255)
        self.color2 = self.braking_rng.uniform(75,255)
        self.color3 = self.braking_rng.uniform(75,255)
        self.size = (25, 17)
        self.bus_color = (self.color1, self.color2, self.color3)
        self.route = []
        self.routeidx = 0
        self.dwell = 0.0  #how long a bus will wait after arrival


    def draw(self, screen):
        bus_surface = pyg.Surface(self.size, pyg.SRCALPHA)
        pyg.draw.rect(bus_surface, self.bus_color, (0, 0, self.size[0], self.size[1]))

        angle = 0
        if len(self.route) > 1:
            target_stop = self.route[self.routeidx]
            dx = target_stop.location[0] - self.position[0]
            dy = target_stop.location[1] - self.position[1]
            angle = math.degrees(math.atan2(dy, dx))
        
        rotated = pyg.transform.rotate(bus_surface, -angle)
        rect = rotated.get_rect(center=(self.position[0], self.position[1]))
        screen.blit(rotated, rect)

    def move(self, target_stop, dt):
        #print("original pos:", self.position)
        x, y = self.position[0], self.position[1]
        tx, ty = target_stop.location[0], target_stop.location[1]
        distance_to = distance(x,y,tx,ty)    
        braking_distance = (self.current_speed ** 2) / (2 * self.acceleration)
        
        should_accel = ((self.current_speed < self.max_speed) and (distance_to > braking_distance + self.brake_buffer))
        
        if should_accel:
            self.current_speed += self.acceleration * dt
        else:
            self.current_speed -= self.acceleration * dt

        if self.current_speed < 0.0:
            self.current_speed = 0.0
        
        if self.current_speed > self.max_speed:
            self.current_speed = self.max_speed


        step = self.current_speed * dt
        
        if step < distance_to:
            dx = (tx - x) / distance_to
            dy = (ty - y) / distance_to
            #print("dx:", dx, "dy:", dy, "step:", step)
            self.position[0] += dx * step
            self.position[1] += dy * step
            #print("new pos:", self.position)

    def set_route(self, stops):
        self.route = list(stops)
        self.routeidx = 0
        
       
        if len(self.route) > 1:
            self.position = np.array(self.route[0].location, dtype=float)
            self.routeidx = (self.routeidx + 1) % len(self.route)



    def load_passengers(self, stop):
        stop.loading = True
        stop.bus = True
        
    def unload_passengers(self):
        for passenger in self.passengers:
            if passenger.desired_stop == passenger.current_stop:
                #passenger.destory
                self.passenger -= 1

    def update(self, dt):
        if self.stopped and self.dwell <= 0.0:
            self.stopped = False

        if self.dwell > 0.0:
            self.dwell = max(0.0, self.dwell - dt)
            return

        if not len(self.route) > 1:
            return

        target_stop = self.route[self.routeidx]

        if not self.stopped:
            prev_dist = distance(self.position[0], self.position[1], target_stop.location[0], target_stop.location[1])
            self.move(target_stop, dt)
            new_dist = distance(self.position[0], self.position[1], target_stop.location[0], target_stop.location[1])
            within_distance_of = 5.0  

            # If we've passed the stop, or are within distance to snap to our stop then snap. Also starts dwell time.
            if new_dist < within_distance_of or new_dist > prev_dist:
                self.position[0], self.position[1] = target_stop.location[0], target_stop.location[1]
                self.current_speed = 0.0
                self.stopped = True
                self.dwell = 1.0
                self.routeidx = (self.routeidx + 1) % len(self.route)
                print(f"Arrived at stop {self.routeidx}, dwell, {self.dwell} started.")




