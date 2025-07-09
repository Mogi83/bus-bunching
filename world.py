class World:
    def __init__(self):
        self.time = 0.0
        self.tick = 1.0
        self.minute = 60.0
        self.hour = 3600.0
        self.sim = False
        self.stops = []
        self.buses = []
        self.passengers = []
        self.buses_count = len(self.buses)
        
    def run(self, ticks):
        for tick in range(ticks):
            self.time += self.tick
            print(self.time)
            for bus in self.buses:
                bus.update()
            for stop in self.stops:
                stop.update()