import math
import time

# Functions
def findD(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def findAngSide(a, b, c):
    cos_value = (a**2 + b**2 - c**2) / (2 * a * b)
    cos_value = max(min(cos_value, 1), -1)
    return math.degrees(math.acos(cos_value))

def get_extreme_point(angle, a, init_position):
    extreme_x = init_position[0] + a * math.cos(math.radians(angle))
    extreme_y = init_position[1] + a * math.sin(math.radians(angle))

    return [extreme_x, extreme_y]

def intersection_points(size, center_1, center_2):

    distance = findD(center_1[0], center_1[1], center_2[0], center_2[1])

    if distance < size*2:
        distance_a = (size**2 - size**2 + distance**2) / (2*distance)
        distance_b = distance_a

        distance_h = math.sqrt(size**2-distance_a**2)

        point_5 = [0,0]

        point_5[0] = center_1[0] + (distance_a/distance) * (center_2[0] - center_1[0])
        point_5[1] = center_1[1] + (distance_a/distance) * (center_2[1] - center_1[1])

        perpendicular_1 = [center_2[1] - center_1[1], center_1[0] - center_2[0]]
        perpendicular_2 = [center_1[1] - center_2[1], center_2[0] - center_1[0]]

        return [[round(point_5[0] + (distance_h * (perpendicular_1[0]))/(distance)), round(point_5[1] + (distance_h * (perpendicular_1[1]))/(distance))],[round(point_5[0] + (distance_h * (perpendicular_2[0]))/(distance)), round(point_5[1] + (distance_h * (perpendicular_2[1]))/(distance))]]
    else:
        print("There are not intersectional points")
        return []