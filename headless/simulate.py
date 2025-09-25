#
# Designed to serve as the overall
# controller of the simulation
#
import simpy
import pandas as pd
from bus import Bus


event_log = []
env = simpy.Environment()
buses = [Bus(env, bus_id=i, stops=["Stop 1", "Stop 2", "Stop 3", "Stop 4"], collector=event_log, interval=8) for i in range(3)]

env.run(until=30)

df = pd.DataFrame(event_log)
print(df)