import pygame as pyg
from stop import Stop
from utils import *
import numpy as np


pyg.init()
screen = pyg.display.set_mode((800,800))
clock = pyg.time.Clock()
running = True

connected = False
dragging = False
drag_start = None
stops = []
edges = []
mods = pyg.key.get_mods()
moving = False
move_target = None
move_offset = (0,0)


while running:
	# poll for events
	# pygame.QUIT event means the user clicked X to close your window
	for event in pyg.event.get():
		if event.type == pyg.QUIT:
			running = False

		
		#move stops
		if event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
			mouse_pos = pyg.mouse.get_pos()
			selected = get_stop_near(mouse_pos, stops)


			mods = pyg.key.get_mods()
			if mods & pyg.KMOD_SHIFT:
				target = get_stop_near(mouse_pos, stops, threshold=10)
				if target:
					moving = True
					move_target = target
					move_offset = (mouse_pos[0] - target.location[0], mouse_pos[1] - target.location[1])

			if selected:
				dragging = True
				drag_start = selected
			else:
				new_stop = Stop(mouse_pos[0], mouse_pos[1])
				stops.append(new_stop)

			



		#road drawing
		if event.type == pyg.MOUSEBUTTONUP and event.button == 1 and dragging:
			mouse_pos = pyg.mouse.get_pos()
			target = get_stop_near(mouse_pos, stops)

			if target and target is not drag_start:
				mods = pyg.key.get_mods()
				
			if (drag_start, target) not in edges:
				edges.append((drag_start, target))
				drag_start.connections.append(target)
				print(f"Connected {drag_start.location} → {target.location}"
						+ (" (one-way)" if mods & pyg.KMOD_CTRL else ""))

			
			if not (mods & pyg.KMOD_CTRL):
				if (target, drag_start) not in edges:
					edges.append((target, drag_start))
					target.connections.append(drag_start)
					print(f"Connected {target.location} → {drag_start.location}")


			
			
			dragging = False
			drag_start = None

		#delete a stop
		if event.type == pyg.MOUSEBUTTONDOWN and event.button == 3:
			mouse_pos = pyg.mouse.get_pos()
			target = get_stop_near(mouse_pos, stops, threshold=25)
			if target:
				stops.remove(target)
				edges[:] = [(a, b) for (a, b) in edges if target is not a and target is not b]
			for s in stops:
				if target in s.connections:
					s.connections.remove(target)
			
			# for edge in edges:
			# 	a, b = edge
			# 	if mods & pyg.KMOD_CTRL and is_road_near(mouse_pos, edge, threshold=25):
			# 		edges.remove(edge)
			# 		if b in a.connections:
            #         	a.connections.remove(b)
		
		if moving and event.type == pyg.MOUSEMOTION:
				mx, my = event.pos
				move_target.location = np.array([mx - move_offset[0], my - move_offset[1]])

		if moving and event.type == pyg.MOUSEBUTTONUP and event.button == 1:
			moving = False
			move_target = None




	screen.fill((0, 0, 0))
	
	for stop in stops:
		stop.draw(screen)

	for a, b in edges:
		pyg.draw.line(screen, (255, 255, 255), a.location, b.location, 2)
		


	if dragging and drag_start:
		pyg.draw.line(screen, (150, 150, 150), drag_start.location, pyg.mouse.get_pos(), 2)


	# flip() the display to put your work on screen
	pyg.display.flip()

	clock.tick(144)  # limits FPS to 144

pyg.quit()