game = World()
bus1 = Bus(game)
stop1 = Stop(game)

game.buses.append(bus1)
game.stops.append(stop1)

game.run(90)