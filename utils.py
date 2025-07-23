def distance(x1, y1, x2, y2):
    return ( ((x1 - x2) ** 2) + ( (y1 - y2) ** 2) ) ** (1/2)

def get_stop_near(pos, stops, threshold=25):
    for stop in stops:
        dx = stop.location[0] - pos[0]
        dy = stop.location[1] - pos[1]
        if dx * dx + dy * dy < threshold * threshold:
            return stop
        
def is_road_near(point, road, threshold = 25):
    (ax, ay), (bx, by) = road
    px, py = point

    vx, vy = bx-ax, by-ay
    wx, wy = px-ax, py-ay

    proj = (vx*wx + vy*wy) / (vx*vx + vy*vy)
    proj = max(0.0, min(1.0, proj))


    cx, cy = ax + proj*vx, ay + proj*vy

    dx, dy = px-cx, py-cy
    return dx*dx + dy*dy <= threshold ** 2