import math
import time

# Functions
def findD(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def findAngSide(a, b, c):
    cos_value = (a**2 + b**2 - c**2) / (2 * a * b)
    cos_value = max(min(cos_value, 1), -1)
    return math.degrees(math.acos(cos_value))

def get_omegas(arms_size, separation, target_x, target_y):
    L0 = separation / 2

    k = math.sqrt((target_x + L0)**2+target_y**2)
    s = math.sqrt((target_x - L0)**2+target_y**2)
    return [math.degrees(math.acos((arms_size[0]**2-arms_size[1]**2+k**2)/(2*arms_size[0]*k))),math.degrees(math.acos((arms_size[0]**2-arms_size[1]**2+s**2)/(2*arms_size[0]*s)))]

def get_beta(separation, max_point, min_point, center_1, center_2, target_x, target_y):
    L0 = separation/2
    if( min_point[0] <= target_x < center_1[0] and min_point[1] <= target_y <= max_point[1] ):
        return [math.degrees(math.atan(target_y/abs(L0+target_x))),math.degrees(math.atan(target_y/abs(L0 - target_x)))]
    elif ( center_1[0] <= target_x < center_2[0] and min_point[1] <= target_y <= max_point[1] ):
        return [math.degrees(math.atan(target_y/abs(L0+target_x))),math.degrees(math.pi - math.atan(target_y/abs(L0 - target_x)))]
    elif ( center_2[0] <= target_x <= max_point[0] and min_point[1] <= target_y <= max_point[1] ):
        return [math.degrees(math.pi - math.atan(target_y/abs(L0+target_x))),math.degrees(math.pi - math.atan(target_y/abs(L0 - target_x)))]
    return []

def get_x_max(y, R, h, k):
    return [round(math.sqrt(R**2-(y-k)**2)+h), round(-math.sqrt(R**2-(y-k)**2)+h)]

def gcd(a,b):

    n = min(a,b)

    while(n > 0):
        if(a % n == 0 and b % n == 0):
            break
        n-=1

    return n

def largest_divisor(n):

    i = int(math.sqrt(n))

    while(i >= 1):
        if n % i == 0:
            return i
        i-=1
        
    return math.sqrt(n)

def intersection_points(size, center_1, center_2):

    distance = findD(center_1[0], center_1[1], center_2[0], center_2[1])

    if distance < size*2:
        distance_a = (size**2 - size**2 + distance**2) / (2*distance)
        distance_b = distance_a

        distance_h = round(math.sqrt(size**2-distance_a**2), 1)

        point_5 = [0,0]

        point_5[0] = center_1[0] + (distance_a/distance) * (center_2[0] - center_1[0])
        point_5[1] = center_1[1] + (distance_a/distance) * (center_2[1] - center_1[1])

        perpendicular_1 = [center_2[1] - center_1[1], center_1[0] - center_2[0]]
        perpendicular_2 = [center_1[1] - center_2[1], center_2[0] - center_1[0]]

        return [[round(point_5[0] + (distance_h * (perpendicular_1[0]))/(distance)), round(point_5[1] + (distance_h * (perpendicular_1[1]))/(distance))],[round(point_5[0] + (distance_h * (perpendicular_2[0]))/(distance)), round(point_5[1] + (distance_h * (perpendicular_2[1]))/(distance))]]
    else:
        print("There are not interseccioned points")
        return []