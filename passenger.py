class Passenger:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.x1 = 1
        self.y1 = 1
        self.current_stop = [self.x, self.y]
        self.desired_stop = [self.x1, self.y1]
        self.time_waited = 0.0