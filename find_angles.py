import math

def get_omegas(arms_size, separation, target_x, target_y):
    try:

        L0 = separation / 2

        k = math.sqrt((target_x + L0)**2+target_y**2)

        s = math.sqrt((target_x - L0)**2+target_y**2)

        return False, [math.degrees(math.acos((arms_size[0]**2-arms_size[1]**2+k**2)/(2*arms_size[0]*k))),math.degrees(math.acos((arms_size[0]**2-arms_size[1]**2+s**2)/(2*arms_size[0]*s)))]
    
    except:

        return True, []

def get_beta(separation, max_point, min_point, center_1, center_2, target_x, target_y, reference):
    try:
        L0 = separation/2

        if( center_2[0] <= reference[0] <= max_point[0] and min_point[1] <= reference[1] <= max_point[1] ):

            return False, [math.degrees(math.atan(target_y/abs(L0 + target_x))),math.degrees(math.atan(target_y/abs(L0 - target_x)))]
        
        elif ( center_1[0] <= reference[0] < center_2[0] and min_point[1] <= reference[1] <= max_point[1] ):

            return False, [math.degrees(math.atan(target_y/abs(L0 + target_x))),math.degrees(math.pi - math.atan(target_y/abs(L0 - target_x)))]
        
        elif ( min_point[0] <= reference[0] < center_1[0] and min_point[1] <= reference[1] <= max_point[1]):

            return False, [math.degrees(math.pi - math.atan(target_y/abs(L0 + target_x))),math.degrees(math.pi - math.atan(target_y/abs(L0 - target_x)))]
        
        return True, []
    except:
        return True, []

def inverse_kinematic(size_whole_arm_array, min_point, max_point, base_arm_1, base_arm_2, target, reference, size_between_motors, angles_per_step):
    try:
        error, omegas = get_omegas(size_whole_arm_array, size_between_motors, target[0], target[1])
        if(error):
            print("There is an error in omegas function, find_angles")
            return True, [0]

        error, betas = get_beta(size_between_motors, max_point, min_point, base_arm_1, base_arm_2, target[0], target[1], reference)
        if(error):
            print("There is an error in betas function, find_angles")
            return True, [1]

        theta_1 = betas[0] + omegas[0]

        theta_2 = betas[1] - omegas[1]

        result = [theta_1, theta_2]

        if angles_per_step > 0.0:

            convert_angles(angles_per_step, result)

        return False, result
    
    except:
        return True, [-1]
    
def convert_angles(angles_per_step, angles):
    
    if angles[0] % angles_per_step != 0:

        angles[0] = round(angles[0]/angles_per_step) * angles_per_step

    if angles[1] % angles_per_step != 0:

        angles[1] = round(angles[1]/angles_per_step) * angles_per_step