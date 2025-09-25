#
# Handles the entirety of the bus logic
#
import simpy
import random

class Bus:
    def __init__(self, env, bus_id, stops, collector, interval):
        #var assignment
        self.env = env
        self.id = bus_id
        self.stops = stops
        self.collector = collector
        self.interval = interval
        self.last_arrival_time = None
        self.current_stop = None

        #processes
        self.board_proc = self.env.process(self.travel())
        self.loading_proc = self.env.process(self.load())
        self.loading_completed = self.env.event()
        self.bus_stopping = self.env.event()


    def travel(self):
        stop_idx = 0
        while True:
            if self.last_arrival_time == None:
                arrival_time = self.env.now
            else:
                arrival_time = self.last_arrival_time + self.interval + random.randint(5,11) #Magic number related to delay
            
            self.current_stop = self.stops[stop_idx]
            self.collector.append({
                "bus_id": self.id,
                "event": "arriving",
                "stop": self.current_stop,
                "time": arrival_time
            })

            self.last_arrival_time = arrival_time
            stop_idx = (stop_idx + 1 ) % len(self.stops)

            yield self.env.timeout(random.randint(5,11)) #Magic number related to dwell time.

            self.bus_stopping.succeed()
            self.bus_stopping = self.env.event()

            yield self.loading_completed

    def load(self):
        while True:
            yield self.bus_stopping

            yield self.env.timeout(random.randint(2,5)) #Magic number for loading time

            self.collector.append({
                "bus_id": self.id,
                "event": "departing",
                "stop": self.current_stop,
                "time": self.env.now
            })
            
            self.loading_completed.succeed()
            self.loading_completed = self.env.event()