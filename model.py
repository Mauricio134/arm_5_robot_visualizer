import func

angles_per_step = 1.8
total_duration_ms = 1000

size_lower_arm = 76.34
size_upper_arm = 94.66
size_whole_arm = size_lower_arm + size_upper_arm

size_whole_arm_array = [size_lower_arm, size_upper_arm]

base_arm_1 = [-20.5, 0]
base_arm_2 = [20.5, 0]

size_between_motors = func.get_euclidean_distance(base_arm_1, base_arm_2)

minimum_y = base_arm_1[1]
maximum_y = func.intersection_points(size_whole_arm, base_arm_1, base_arm_2)[1][1]
maximum_x = func.get_x_max(0, size_whole_arm, base_arm_1[0], base_arm_1[1])[0]
minimum_x = -maximum_x

max_point = [maximum_x, maximum_y]
min_point = [minimum_x, minimum_y]

target = [14.0, 38.0]

angles_1 = func.get_motor_angles_1(size_whole_arm_array,min_point, max_point, base_arm_1, base_arm_2, target, size_between_motors)

if angles_1[0] % angles_per_step != 0:
    angles_1[0] = round(angles_1[0]/angles_per_step) * angles_per_step

if angles_1[1] % angles_per_step != 0:
    angles_1[1] = round(angles_1[1]/angles_per_step) * angles_per_step

center_1 = func.get_extremes(size_whole_arm_array[0], base_arm_1, angles_1[0])
center_2 = func.get_extremes(size_whole_arm_array[0], base_arm_2, angles_1[1])

intersections_1 = func.intersection_points(size_whole_arm_array[1], center_1, center_2)

print(angles_1)
print(intersections_1[1])

angles_2 = func.get_motor_angles_2(size_whole_arm_array, base_arm_1, base_arm_2, target, size_between_motors)

if angles_2[0] % angles_per_step != 0:
    angles_2[0] = round(angles_2[0]/angles_per_step) * angles_per_step

if angles_2[1] % angles_per_step != 0:
    angles_2[1] = round(angles_2[1]/angles_per_step) * angles_per_step

center_1 = func.get_extremes(size_whole_arm_array[0], base_arm_1, angles_2[0])
center_2 = func.get_extremes(size_whole_arm_array[0], base_arm_2, angles_2[1])

intersections_2 = func.intersection_points(size_whole_arm_array[1], center_1, center_2)

print(angles_2)
print(intersections_2[1])


angles_1 = func.get_motor_angles_1(size_whole_arm_array,min_point, max_point, base_arm_1, base_arm_2, intersections_1[1], size_between_motors)

if angles_1[0] % angles_per_step != 0:
    angles_1[0] = round(angles_1[0]/angles_per_step) * angles_per_step

if angles_1[1] % angles_per_step != 0:
    angles_1[1] = round(angles_1[1]/angles_per_step) * angles_per_step

print(angles_1)

angles_2 = func.get_motor_angles_2(size_whole_arm_array, base_arm_1, base_arm_2, intersections_2[1], size_between_motors)

if angles_2[0] % angles_per_step != 0:
    angles_2[0] = round(angles_2[0]/angles_per_step) * angles_per_step

if angles_2[1] % angles_per_step != 0:
    angles_2[1] = round(angles_2[1]/angles_per_step) * angles_per_step


print(angles_2)