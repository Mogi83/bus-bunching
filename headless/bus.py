class Bus:
    def __init__(self, bus_id,  env):
        self.env = env
        self.action = env.process(self.run())

    def run(self):
        while True:
            pass