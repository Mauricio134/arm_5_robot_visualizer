import create_angles
import general
import points

def find_path(init_position, target, size_whole_arm_array, size_between_motors, min_point, max_point, base_arm_1, base_arm_2, segment_x, segment_y, angles_per_step, radius):
    path = []
    degrees = []

    if min_point[1] > target[1] or target[1] > max_point[1] or min_point[0] > target[0] or target[0] > max_point[0]:
        return path, degrees

    if create_angles.get_motor_angles_1(size_whole_arm_array, min_point, max_point, base_arm_1, base_arm_2, target, init_position, size_between_motors) == [] :
        return path, degrees
    
    angles, new_position_init = points.convert_positions(size_whole_arm_array, min_point, max_point, base_arm_1, base_arm_2, init_position, init_position, size_between_motors, angles_per_step)

    if angles == [] or new_position_init == []:
        return [], []

    new_position_init = new_position_init[1]
    
    count = 0

    while general.get_euclidean_distance(new_position_init, target) > radius:
        init_x = init_position[0] - segment_x
        init_y = init_position[1] + segment_y

        distance = 99999.0

        new_pos_init_x = 0
        new_pos_init_y = 0

        new_point = []
        new_angles = []

        for i in range(0,3):
            for j in range(0,3):

                pos_x = init_x + j * segment_x
                pos_y = init_y - i * segment_y

                if pos_y < min_point[1] or pos_y > max_point[1] or pos_x < min_point[0] or pos_x > max_point[0]:
                    continue
                
                if pos_x == init_position[0] and pos_y == init_position[1]:
                    continue

                angles, new_positions = points.convert_positions(size_whole_arm_array, min_point, max_point, base_arm_1, base_arm_2, [pos_x, pos_y], init_position, size_between_motors, angles_per_step)

                if angles == [] or new_position_init == []:
                    continue

                new_positions = new_positions[1]

                new_distance = general.get_euclidean_distance(new_position_init, new_positions) + general.get_euclidean_distance(new_positions, target)
                if new_distance < distance:
                    distance = new_distance
                    new_pos_init_x = pos_x
                    new_pos_init_y = pos_y
                    new_point = new_positions
                    new_angles = angles
            
        init_position[0] = new_pos_init_x
        init_position[1] = new_pos_init_y

        angles, new_position_init = points.convert_positions(size_whole_arm_array, min_point, max_point, base_arm_1, base_arm_2, init_position, init_position, size_between_motors, angles_per_step)

        new_position_init = new_position_init[1]

        path.append(new_point)
        degrees.append(new_angles)

        count+=1

    return path, degrees