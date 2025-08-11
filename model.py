import time
import func
import tkinter as tk
import math

# Features of NEMA 14 Stepper Motor
rpm = 5
angles_per_second = rpm * 6

angles_per_step = 1.8

duration = 6000

# Features of five arm parallel robot
size_a = 76.34
size_b = 94.66
base_arm_1_x, base_arm_1_y = -20.5, 0
base_arm_2_x, base_arm_2_y = 20.5, 0
size_between_motors = func.findD(base_arm_2_x, base_arm_2_y, base_arm_1_x, base_arm_1_y)

# Features of target
init_target_x, init_target_y = 0, 150

minimum_y = base_arm_1_y + 30
maximum_y = func.intersection_points(size_a + size_b, [base_arm_1_x, base_arm_1_y], [base_arm_2_x, base_arm_2_y])[1][1]

maximum_x = func.get_x_max(0, size_a + size_b, base_arm_1_x, base_arm_1_y)[0]
minimum_x = -maximum_x

max_point = [maximum_x, maximum_y]
min_point = [minimum_x, minimum_y]

distance_height = func.findD(0,minimum_y, 0, maximum_y)
distance_width = func.findD(minimum_x, minimum_y, maximum_x, minimum_y)

simple_or_each = False

num_large_h = func.largest_divisor(distance_height)
num_large_w = func.largest_divisor(distance_width)

if(simple_or_each == True):
    num_large_h = func.gcd(distance_height, distance_width)
    num_large_w = num_large_h

whole_map, exact_row, exact_column, total_row, total_column = func.reachibility_map(min_point,max_point, num_large_w, num_large_h,size_a, size_b, size_between_motors, [base_arm_1_x, base_arm_1_y], [base_arm_2_x, base_arm_2_y],angles_per_step)

func.create_window([init_target_x, init_target_y], angles_per_step, duration, [size_a, size_b], [base_arm_1_x, base_arm_1_y], [base_arm_2_x, base_arm_2_y], size_between_motors, whole_map, [exact_row, exact_column], [total_row, total_column], [num_large_w, num_large_h],max_point, min_point )

# Create point max and min

