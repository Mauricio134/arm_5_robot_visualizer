import math
import general

def get_omegas(arms_size, separation, target_x, target_y):
    print(target_x, target_y)
    try:
        L0 = separation / 2

        k = math.sqrt((target_x + L0)**2+target_y**2)

        s = math.sqrt((target_x - L0)**2+target_y**2)
        print("###### Omega ######")
        print((arms_size[0]**2-arms_size[1]**2+k**2)/(2*arms_size[0]*k))
        print((arms_size[0]**2-arms_size[1]**2+s**2)/(2*arms_size[0]*s))

        return [math.degrees(math.acos((arms_size[0]**2-arms_size[1]**2+k**2)/(2*arms_size[0]*k))),math.degrees(math.acos((arms_size[0]**2-arms_size[1]**2+s**2)/(2*arms_size[0]*s)))]
    except:
        print("Error in create_angles.py, get_omegas")
        return []

def get_beta(separation, max_point, min_point, center_1, center_2, target_x, target_y, real_position):
    print("##### Beta ######")
    print(target_x)
    print(min_point[0])
    print(center_1[0])
    print(center_2[0])
    print(max_point[0])
    print()
    print(target_y)
    print(min_point[1])
    print(max_point[1])
    try:
        L0 = separation/2

        if( center_2[0] <= real_position[0] <= max_point[0] and min_point[1] <= real_position[1] <= max_point[1] ):

            return [math.degrees(math.atan(target_y/abs(L0 + target_x))),math.degrees(math.atan(target_y/abs(L0 - target_x)))]
        
        elif ( center_1[0] <= real_position[0] < center_2[0] and min_point[1] <= real_position[1] <= max_point[1] ):

            return [math.degrees(math.atan(target_y/abs(L0 + target_x))),math.degrees(math.pi - math.atan(target_y/abs(L0 - target_x)))]
        
        elif ( min_point[0] <= real_position[0] < center_1[0] and min_point[1] <= real_position[1] <= max_point[1]):

            return [math.degrees(math.pi - math.atan(target_y/abs(L0 + target_x))),math.degrees(math.pi - math.atan(target_y/abs(L0 - target_x)))]
        
        return []
    except:
        print("Error in create_angles.py, get_beta")
        return []

def get_interior_angle(a, b, c):
    try:
        cos_value = (a**2 + b**2 - c**2) / (2 * a * b)
        
        cos_value = max(min(cos_value, 1), -1)

        return math.degrees(math.acos(cos_value))
    except:
        print("Error in create_angles.py, get_interior_angle")
        return []

def get_motor_angles_1(size_whole_arm_array, min_point, max_point, base_arm_1, base_arm_2, target, real_position, size_between_motors):
    try:
        omegas = get_omegas(size_whole_arm_array, size_between_motors, target[0], target[1])

        betas = get_beta(size_between_motors, max_point, min_point, base_arm_1, base_arm_2, target[0], target[1], real_position)

        theta_1 = betas[0] + omegas[0]

        theta_2 = betas[1] - omegas[1]

        return [theta_1, theta_2]
    except:
        print("Error in create_angles.py, get_motor_angles_1")
        return []

def get_motor_angles_2(sizes, arm_left, arm_right, target, size_between_motors):
    try:
        # Faces
        face_1 = general.get_euclidean_distance(arm_left, target)
        face_2 = general.get_euclidean_distance(arm_right, target)

        # Angles in motor 1
        theta_2 = get_interior_angle(sizes[0], face_1, sizes[1])
        theta_3 = get_interior_angle(face_1, size_between_motors, face_2)
        theta_total = theta_2 + theta_3

        # Angles in motor 2
        beta_2 = get_interior_angle(sizes[0], face_2, sizes[1])
        beta_3 = get_interior_angle(face_2, size_between_motors, face_1)
        beta_1 = 180.0 - (beta_3 + beta_2)

        return [theta_total, beta_1]
    except:
        print("Error in create_angles.py, get_motor_angles_2")
        return []