#
# Handles the entirety of the bus logic
#
import simpy
import random

class Bus:
    def __init__(self, env, bus_id, stops, collector, interval, start_offset=0, mode="random", seed=0):
        #var assignment
        self.env = env
        self.id = bus_id
        self.stops = stops
        self.collector = collector
        self.interval = interval
        self.last_arrival_time = None
        self.current_stop = None
        self.control_arrival_times = [i * interval for i in range(len(stops))] #setting up a control system
        self.distance_to_stop_score = 0
        self.mode = mode
        self.seed = seed
        random.seed = self.seed

        #processes
        self.board_proc = self.env.process(self.travel(start_offset))
        self.loading_proc = self.env.process(self.load())
        self.loading_completed = self.env.event()
        self.bus_stopping = self.env.event()


    def travel(self, start_offset):
        stop_idx = 0

        if start_offset > 0:
            yield self.env.timeout(start_offset)

        while True:
            if self.last_arrival_time == None:
                arrival_time = self.env.now
            else:
                if self.mode == "control":
                    arrival_time = self.last_arrival_time + self.interval
                
                elif self.mode == "random":
                    interval_variation = random.uniform(10,30)
                    arrival_time = self.last_arrival_time + self.interval + interval_variation
            
            self.current_stop = self.stops[stop_idx]


            control_time = self.control_arrival_times[stop_idx]
            distance_to_stop = arrival_time - control_time
            self.distance_to_stop_score += abs(distance_to_stop)


            self.collector.append({
                "bus_id": self.id,
                "event": "arrived",
                "stop": self.current_stop,
                "time": arrival_time
            })

            self.last_arrival_time = arrival_time
            stop_idx = (stop_idx + 1 ) % len(self.stops)
            
            if self.mode == "control":
                dwell_time = 5  #represents the bus waiting a stop regardless of passengers.
            elif self.mode == "random":
                dwell_time = random.uniform(3,7)
            
            yield self.env.timeout(dwell_time)

            self.bus_stopping.succeed()
            self.bus_stopping = self.env.event()

            yield self.loading_completed

    def load(self):
        while True:
            yield self.bus_stopping

            if self.mode == "random":
                yield self.env.timeout(random.randint(2,5)) #Magic number for loading time in min
            else:
                yield self.env.timeout(3)

            self.collector.append({
                "bus_id": self.id,
                "event": "departing",
                "stop": self.current_stop,
                "time": self.env.now
            })
            
            self.loading_completed.succeed()
            self.loading_completed = self.env.event()