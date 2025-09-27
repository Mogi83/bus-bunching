#
# Designed to serve as the overall
# controller of the simulation
#
import simpy
import pandas as pd
import random
from bus import Bus
from bunching import detect_bunching


event_log = []
env = simpy.Environment()
#control
#buses = [Bus(env, bus_id=i, stops=["Stop " + str(i) for i in range(1, 6)], collector=event_log, interval=10, start_offset=5, mode="control") for i in range(3)]
#random
buses = [Bus(env, bus_id=i, stops=["Stop " + str(i) for i in range(1, 6)], collector=event_log, interval=10, start_offset=5, mode="random", seed=random.randint(0, 1000)) for i in range(3)]

env.run(until=120)
df = pd.DataFrame(event_log)
df = df[df["time"] <= 120]
print(df)
print()
detect_bunching(event_log)

