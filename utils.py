import math

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

def draw_arrow(screen, start, end , color=(255,255,255), arrow_length=15, arrow_angle=45):
    sx, sy = start
    ex, ey = end

    mid_x = (sx + ex) / 2
    mid_y = (sy + ey) / 2


    dx, dy = ex - sx, ey - sy
    length = (dx**2 + dy**2) ** 0.5
    if length == 0:
        return

    norm_dx, norm_dy = dx / length, dy / length

    
    tip_x = mid_x + norm_dx * (arrow_length / 2)
    tip_y = mid_y + norm_dy * (arrow_length / 2)

    # Draw main line
    pyg.draw.line(screen, color, (sx, sy), (ex, ey), 2)


    dir_angle = math.atan2(norm_dy, norm_dx)
    angle_rad = math.radians(arrow_angle)


    left_angle = dir_angle + angle_rad
    left_x = tip_x - arrow_length * math.cos(left_angle)
    left_y = tip_y - arrow_length * math.sin(left_angle)
    pyg.draw.line(screen, color, (tip_x, tip_y), (left_x, left_y), 2)


    right_angle = dir_angle - angle_rad
    right_x = tip_x - arrow_length * math.cos(right_angle)
    right_y = tip_y - arrow_length * math.sin(right_angle)
    pyg.draw.line(screen, color, (tip_x, tip_y), (right_x, right_y), 2)

