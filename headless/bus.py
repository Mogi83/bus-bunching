#
# Handles the entirety of the bus logic
#
import simpy
import random

class Bus:
    def __init__(self, env):
        self.env = env
        self.board_proc = self.env.process(self.travel())
        self.loading_proc = self.env.process(self.load())
        self.loading_completed = self.env.event()
        self.bus_stopping = self.env.event()

    def travel(self):
        while True:
            print("Leaving stop at time %d" % self.env.now)
            yield self.env.timeout(random.randint(5,11))
            print("Arriving at a stop at time %d" % self.env.now)
            self.bus_stopping.succeed()
            self.bus_stopping = self.env.event()
            yield self.loading_completed

    def load(self):
        while True:
            yield self.bus_stopping
            print("Passengers hopping on at time %d" % self.env.now)
            yield self.env.timeout(random.randint(2,5))
            print("Passengers loaded at time %d" % self.env.now)
            self.loading_completed.succeed()
            self.loading_completed = self.env.event()