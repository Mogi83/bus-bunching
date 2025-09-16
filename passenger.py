import numpy as np

# needs a state machine, "waiting", "on bus", "arrived"

class Passenger:
    def __init__(self):
        self.stop_rng = np.random.default_rng()
        #setting their coordinates may not be necessary. 
        self.x = 0
        self.y = 0
        self.x1 = 1
        self.y1 = 1
        self.current_stop = [self.x, self.y] #shouldn just be the stop this passenger is spawned at, coords unnecessary. 
        self.desired_stop = [self.x1, self.y1] #refactor these so they go through all available stops (excluding the current stop) and make a choice based on avail stops. 
        self.time_waited = 0.0
    
    def update(self, dt):
        #Some type of update fucntion to count the time waited
        
        pass