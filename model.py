import general
import points
import motion
import create_angles
import time

angles_per_step = 1.8
total_duration_ms = 1000

size_lower_arm = 76.34
size_upper_arm = 94.66
size_whole_arm = size_lower_arm + size_upper_arm

size_whole_arm_array = [size_lower_arm, size_upper_arm]

base_arm_1 = [-20.5, 0]
base_arm_2 = [20.5, 0]

init_position = [0.0, 38.0]

size_between_motors = general.get_euclidean_distance(base_arm_1, base_arm_2)

minimum_y = base_arm_1[1] + init_position[1]
maximum_y = points.intersection_points(size_whole_arm, base_arm_1, base_arm_2)[1][1]
maximum_x = general.get_x_max(0, size_whole_arm, base_arm_1[0], base_arm_1[1])[0]
minimum_x = -maximum_x

max_point = [maximum_x, maximum_y]
min_point = [minimum_x, minimum_y]

simple_or_each = False

distance_height = general.get_euclidean_distance([min_point[0], min_point[1]], [min_point[0], max_point[1]])
distance_width = general.get_euclidean_distance([min_point[0], min_point[1]], [max_point[0], min_point[1]])

num_large_h = general.largest_divisor(distance_height)
num_large_w = general.largest_divisor(distance_width)

if(simple_or_each == True):
    num_large_h = general.gcd(distance_height, distance_width)
    num_large_w = num_large_h

separations = [num_large_w, num_large_h]

while True:
    x = float(input("X: "))
    y = float(input("Y: "))

    target = [x, y]

    inicio = init_position

    path, degrees = motion.find_path(init_position, target, size_whole_arm_array, size_between_motors, min_point, max_point, base_arm_1, base_arm_2, separations[0], separations[1], angles_per_step, min(separations[0], separations[1]))

    print("Leer path")
    if path == [] :
        continue

    amount_angles = len(path)

    time_per_step = total_duration_ms / amount_angles

    init_time = time.time() * 1000.0

    first = 0
    while first < len(path):

        current_time = time.time() * 1000.0

        if(current_time - init_time >= time_per_step):
            angles_init = create_angles.get_motor_angles_1(size_whole_arm_array, min_point, max_point, base_arm_1, base_arm_2, path[first], init_position, size_between_motors)
            if angles_init == []:
                print("Fallaste")
                break
            if angles_init[0] % angles_per_step != 0:
                angles_init[0] = round(angles_init[0]/angles_per_step) * angles_per_step

            if angles_init[1] % angles_per_step != 0:
                angles_init[1] = round(angles_init[1]/angles_per_step) * angles_per_step

            print("==============")
            print(inicio)
            print(path)
            print(path[first])
            print(degrees[first])
            print(angles_init)
            print(init_position)

            init_time = current_time

            first += 1