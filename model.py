import general
import find_points

angles_per_step = 1.8

duration_total_ms = 6000

size_whole_arm= [76.34, 94.66]

base_arm_1 = [-20.5, 0.0]
base_arm_2 = [20.5, 0.0]

height_of_the_base = 35.0

distance_between_motors = general.get_distance_between_points(base_arm_1, base_arm_2)

init_position = [0.0, height_of_the_base + 3.0]

min_point_y = init_position[1]
error, max_point_y = find_points.intersection_points(size_whole_arm[0] + size_whole_arm[1], [base_arm_1, base_arm_2])
error, max_point_x = find_points.find_x_max(size_whole_arm[0] + size_whole_arm[1], 0.0, base_arm_1)
max_point_y = max_point_y[1][1]
max_point_x = max_point_x[0]
min_point_x = -max_point_x

min_point = [ min_point_x, min_point_y ]
max_point = [ max_point_x, max_point_y ]

simple_or_each = False

distance_height = general.get_distance_between_points(min_point, [min_point[0], max_point[1]])
distance_width = general.get_distance_between_points(min_point, [max_point[0], min_point[1]])

num_large_h = general.largest_divisor(distance_height)
num_large_w = general.largest_divisor(distance_width)

if(simple_or_each == True):
    error, new_num_large_h = general.gcd(distance_height, distance_width)
    new_num_large_w = new_num_large_h
    if(error):
        num_large_h = new_num_large_h
        num_large_w = new_num_large_h

size_segments = [num_large_w, num_large_h]