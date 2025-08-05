import pygame as pyg
from stop import Stop
from utils import *
import numpy as np


pyg.init()
screen = pyg.display.set_mode((800,800))
clock = pyg.time.Clock()
running = True

connected = False

drag_start = None
stops = []
edges = []

moving = False
move_target = None
move_offset = (0,0)
mode = "idle"

while running:
	for event in pyg.event.get():
		if event.type == pyg.QUIT:
			running = False

		#stopsV2
		if event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
			mouse_pos = pyg.mouse.get_pos()
			mods = pyg.key.get_mods()
			selected = get_stop_near(mouse_pos, stops)

			if (mods & pyg.KMOD_SHIFT) and selected:
				mode = "moving" 
				mode_target = selected
				mode_offset = (mouse_pos[0] - selected.location[0], mouse_pos[1] - selected.location[1])
			
			elif selected:
				mode = "connecting"
				drag_start = selected
			
			else:
				stops.append(Stop(mouse_pos[0], mouse_pos[1]))
				mode = "idle"

		#move a stop
		if event.type == pyg.MOUSEMOTION and mode == "moving":
			mx, my = event.pos
			mode_target.location = np.array([mx - mode_offset[0], my - mode_offset[1]])
		
		if event.type == pyg.MOUSEBUTTONUP and event.button == 1 and mode == "moving":
			mode = "idle"
			mode_target = None
			mode_offset = (0, 0)

		#road drawing
		if event.type == pyg.MOUSEBUTTONUP and event.button == 1 and mode == "connecting":
			mouse_pos = pyg.mouse.get_pos()
			target = get_stop_near(mouse_pos, stops)
			
			if target is not None and target is not drag_start:
				mods = pyg.key.get_mods()
				
				if (drag_start, target) not in edges:
					edges.append((drag_start, target))
					drag_start.connections.append(target)
					print(f"Connected {drag_start.location} to {target.location}" + (" (one-way)" if (mods & pyg.KMOD_CTRL) else ""))

				
				if not (mods & pyg.KMOD_CTRL):
					if (target, drag_start) not in edges:
						edges.append((target, drag_start))
						target.connections.append(drag_start)
						print(f"Connected {target.location} to {drag_start.location}")
			
			mode = "idle"
			drag_start = None

		#delete a stop
		if event.type == pyg.MOUSEBUTTONDOWN and event.button == 3:
			mouse_pos = pyg.mouse.get_pos()
			mods = pyg.key.get_mods()
			target = get_stop_near(mouse_pos, stops, threshold=25)
			if target:
				stops.remove(target)
				edges[:] = [(a, b) for (a, b) in edges if target is not a and target is not b]
			for s in stops:
				if target in s.connections:
					s.connections.remove(target)
		
		#delete a road
			if mods & pyg.KMOD_CTRL:
				for edge in edges[:]:
					a, b = edge

					if is_road_near(mouse_pos, (a.location, b.location), threshold=30):
						edges.remove(edge)
						if b in a.connections:
							a.connections.remove(b)
							print(a.connections)
						if (b,a) in edges:
							edges.remove((b,a))
							if a in b.connections:
								b.connections.remove(a)
								print(b.connections)


	screen.fill((0, 0, 0))
	
	for stop in stops:
		stop.draw(screen)

	for a, b in edges:
		if (b, a) in edges:               # now true for a real two-way road
			pyg.draw.line(screen, (255,255,255), a.location, b.location, 2)
		else:
			draw_arrow(screen, a.location, b.location, (255,255,255))
	

		
	


	if mode == "connecting" and drag_start:
		pyg.draw.line(screen, (150, 150, 150), drag_start.location, pyg.mouse.get_pos(), 2)


	# flip() the display to put your work on screen
	pyg.display.flip()

	clock.tick(144)  # limits FPS to 144

pyg.quit()