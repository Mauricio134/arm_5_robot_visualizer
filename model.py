import general

angles_per_step = 1.8
total_duration_ms = 1000

size_lower_arm = 76.34
size_upper_arm = 94.66
size_whole_arm = size_lower_arm + size_upper_arm

size_whole_arm_array = [size_lower_arm, size_upper_arm]

base_arm_1 = [-20.5, 0]
base_arm_2 = [20.5, 0]

size_between_motors = general.get_euclidean_distance(base_arm_1, base_arm_2)

minimum_y = base_arm_1[1]
maximum_y = general.intersection_points(size_whole_arm, base_arm_1, base_arm_2)[1][1]
maximum_x = general.get_x_max(0, size_whole_arm, base_arm_1[0], base_arm_1[1])[0]
minimum_x = -maximum_x

max_point = [maximum_x, maximum_y]
min_point = [minimum_x, minimum_y]

init_position = [0.0, 38.0]

