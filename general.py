import math
import find_points
import find_angles

def get_distance_between_points(init_point, fin_point):

    delta_x = ( fin_point[0] - init_point[0] ) ** 2

    delta_y = ( fin_point[1] - init_point[1] ) ** 2

    return math.sqrt( delta_x + delta_y )

def gcd(a,b):

    n = min(round(a),round(b))

    while(n > 0):
        print(n)
        if(a % n == 0 and b % n == 0):
            return False, n
        n-=1

    return True, 0.0

def largest_divisor(n):

    i = int(math.sqrt(n))

    while(i >= 1):
        if n % i == 0:
            return i
        i-=1
        
    return math.sqrt(n)

def find_path(size_whole_arm, init_position, fin_position, min_point, max_point, base_arm_1, base_arm_2, segment_x, segment_y, distance_between_motors, angles_per_step, radius):
    
    if find_points.limitations(min_point, max_point, fin_position) :
        return True, [], []
    
    error, angles = find_angles.inverse_kinematic(size_whole_arm, min_point, max_point, base_arm_1, base_arm_2, fin_position, fin_position, distance_between_motors, angles_per_step)

    if error :
        return True, [], []
    
    error, new_position_fin = find_points.kinematic([base_arm_1, base_arm_2], size_whole_arm, angles)

    if error:
        return True, [], []
    
    error, angles = find_angles.inverse_kinematic(size_whole_arm,min_point, max_point, base_arm_1, base_arm_2, init_position, init_position, distance_between_motors, angles_per_step)

    if error : 
        return True, [], []
    
    error, new_position_init = find_points.kinematic([base_arm_1, base_arm_2], size_whole_arm, angles)

    if error:
        return True, [], []
    
    path = []
    reference = []
    while get_distance_between_points(new_position_init, new_position_fin) > radius:

        init_x = init_position[0] - segment_x
        init_y = init_position[1] + segment_y

        distance = 99999.0

        new_pos_init_x = 0
        new_pos_init_y = 0

        for i in range(0,3):
            for j in range(0,3):

                pos_x = init_x + j * segment_x
                pos_y = init_y - i * segment_y

                if pos_x == init_position[0] and pos_y == init_position[1]:
                    continue

                if find_points.limitations(min_point, max_point, [pos_x, pos_y]) :
                    continue

                error, angles = find_angles.inverse_kinematic(size_whole_arm,min_point, max_point, base_arm_1, base_arm_2,[pos_x, pos_y], [pos_x, pos_y], distance_between_motors, angles_per_step)

                if error :
                    continue

                error, new_position = find_points.kinematic([base_arm_1, base_arm_2], size_whole_arm, angles)

                if error :
                    continue

                new_distance = get_distance_between_points(new_position_init, new_position) + get_distance_between_points(new_position, new_position_fin)

                if new_distance < distance:
                    distance = new_distance
                    new_pos_init_x = pos_x
                    new_pos_init_y = pos_y
                    new_position_init = new_position

        init_position[0] = new_pos_init_x
        init_position[1] = new_pos_init_y

        print(reference)
        reference.append(init_position.copy())
        
        path.append(new_position_init)
    
    if len(path) > 0:
        if path[-1] != new_position_fin:
            print(reference)
            reference.append(init_position.copy())
            path.append(new_position_fin)
    
    return False, path, reference

