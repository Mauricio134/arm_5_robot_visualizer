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

target = [0.0, 38.0]

#whole_map, whole_degrees, exact_point, dimensions, separations = func.get_grid_movement(min_point, max_point, size_whole_arm_array, size_between_motors, base_arm_1, base_arm_2, angles_per_step, False, 38)

func.create_window(target, size_whole_arm_array, min_point, max_point, base_arm_1, base_arm_2, size_between_motors, angles_per_step, total_duration_ms, False, 38)

#path, _, l = func.reachibility_path(whole_map, exact_point, dimensions[0], dimensions[1], target,min(separations[0], separations[1]), size_whole_arm_array, size_between_motors, max_point, min_point, base_arm_1, base_arm_2, angles_per_step)