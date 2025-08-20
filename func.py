import math
import matplotlib.pyplot as plt
from tkinter import *
import time
import numpy as np

def get_euclidean_distance(init, fin):
    delta_x = (fin[0] - init[0])**2
    delta_y = (fin[1] - init[1])**2
    return math.sqrt(delta_x + delta_y)

def get_omegas(arms_size, separation, target_x, target_y):
    L0 = separation / 2

    k = math.sqrt((target_x + L0)**2+target_y**2)
    s = math.sqrt((target_x - L0)**2+target_y**2)
    return [math.degrees(math.acos((arms_size[0]**2-arms_size[1]**2+k**2)/(2*arms_size[0]*k))),math.degrees(math.acos((arms_size[0]**2-arms_size[1]**2+s**2)/(2*arms_size[0]*s)))]

def get_beta(separation, max_point, min_point, center_1, center_2, target_x, target_y):
    L0 = separation/2
    if( center_2[0] <= target_x <= max_point[0] and min_point[1] <= target_y <= max_point[1] ):
        return [math.degrees(math.atan(target_y/abs(L0 + target_x))),math.degrees(math.atan(target_y/abs(L0 - target_x)))]
    elif ( center_1[0] <= target_x < center_2[0] and min_point[1] <= target_y <= max_point[1] ):
        return [math.degrees(math.atan(target_y/abs(L0 + target_x))),math.degrees(math.pi - math.atan(target_y/abs(L0 - target_x)))]
    elif ( min_point[0] <= target_x < center_1[0] and min_point[1] <= target_y <= max_point[1]):
        return [math.degrees(math.pi - math.atan(target_y/abs(L0 + target_x))),math.degrees(math.pi - math.atan(target_y/abs(L0 - target_x)))]
    return []

def intersection_points(size, center_1, center_2):

    distance = get_euclidean_distance(center_1, center_2)

    if distance < size*2:
        distance_a = (size**2 - size**2 + distance**2) / (2*distance)
        distance_b = distance_a

        distance_h = math.sqrt(size**2-distance_a**2)

        point_5 = [0,0]

        point_5[0] = center_1[0] + (distance_a/distance) * (center_2[0] - center_1[0])
        point_5[1] = center_1[1] + (distance_a/distance) * (center_2[1] - center_1[1])

        perpendicular_1 = [center_2[1] - center_1[1], center_1[0] - center_2[0]]
        perpendicular_2 = [center_1[1] - center_2[1], center_2[0] - center_1[0]]

        return [[point_5[0] + (distance_h * (perpendicular_1[0]))/(distance), point_5[1] + (distance_h * (perpendicular_1[1]))/(distance)],[point_5[0] + (distance_h * (perpendicular_2[0]))/(distance), point_5[1] + (distance_h * (perpendicular_2[1]))/(distance)]]
    else:
        print("There are not interseccioned points")
        return []
    
def get_x_max(y, R, h, k):
    return [math.sqrt(R**2-(y-k)**2)+h, -math.sqrt(R**2-(y-k)**2)+h]

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

def get_extremes(size, arm, angle):
    extremo_x = arm[0] + size * math.cos(math.radians(angle))
    extremo_y = arm[1] + size * math.sin(math.radians(angle))

    return [extremo_x, extremo_y]

def get_motor_angles_1(size_whole_arm_array, min_point, max_point, base_arm_1, base_arm_2, target, size_between_motors):
    try:
        omegas = get_omegas(size_whole_arm_array, size_between_motors, target[0], target[1])

        betas = get_beta(size_between_motors, max_point, min_point, base_arm_1, base_arm_2, target[0], target[1])

        theta_1 = betas[0] + omegas[0]

        theta_2 = betas[1] - omegas[1]

        return [theta_1, theta_2]
    except:
        return []
    
def findAngSide(a, b, c):
    cos_value = (a**2 + b**2 - c**2) / (2 * a * b)
    cos_value = max(min(cos_value, 1), -1)
    return math.degrees(math.acos(cos_value))

def get_motor_angles_2(sizes, arm_left, arm_right, target, size_between_motors):
    # Faces
    face_1 = get_euclidean_distance(arm_left, target)
    face_2 = get_euclidean_distance(arm_right, target)

    # Angles in motor 1
    theta_2 = findAngSide(sizes[0], face_1, sizes[1])
    theta_3 = findAngSide(face_1, size_between_motors, face_2)
    theta_total = theta_2 + theta_3

    # Angles in motor 2
    beta_2 = findAngSide(sizes[0], face_2, sizes[1])
    beta_3 = findAngSide(face_2, size_between_motors, face_1)
    beta_1 = 180.0 - (beta_3 + beta_2)

    return [theta_total, beta_1]
