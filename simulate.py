game = world()
bus1 = bus(game)
stop1 = stop(game)

game.buses.append(bus1)
game.stops.append(stop1)

game.run(90)