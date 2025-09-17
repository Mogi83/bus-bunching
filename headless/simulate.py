#
# Designed to serve as the overall
# controller of the simulation
#
import simpy
from bus import Bus


env = simpy.Environment()
bus = Bus(env)
env.run(until=30)