import math
import general

def get_base_point_upper_arm(point_position_base_lower_arm, size_lower_arm, angle_lower_arm):
    try:

        extremo_x = point_position_base_lower_arm[0] + size_lower_arm * math.cos(math.radians(angle_lower_arm))

        extremo_y = point_position_base_lower_arm[1] + size_lower_arm * math.sin(math.radians(angle_lower_arm))

        return False, [extremo_x, extremo_y]
    
    except:
        return True, []

def intersection_points(size_upper_arm, centers_rotation):

    distance = general.get_distance_between_points(centers_rotation[0], centers_rotation[1])

    if distance < size_upper_arm * 2:

        distance_a = (size_upper_arm**2 - size_upper_arm**2 + distance**2) / (2*distance)
        distance_b = distance_a

        distance_h = math.sqrt(size_upper_arm**2-distance_a**2)

        point_5 = [0,0]

        point_5[0] = centers_rotation[0][0] + (distance_a/distance) * (centers_rotation[1][0] - centers_rotation[0][0])
        point_5[1] = centers_rotation[0][1] + (distance_a/distance) * (centers_rotation[1][1] - centers_rotation[0][1])

        perpendicular_1 = [centers_rotation[1][1] - centers_rotation[0][1], centers_rotation[0][0] - centers_rotation[1][0]]
        perpendicular_2 = [centers_rotation[0][1] - centers_rotation[1][1], centers_rotation[1][0] - centers_rotation[0][0]]

        return False , [[point_5[0] + (distance_h * (perpendicular_1[0]))/(distance), point_5[1] + (distance_h * (perpendicular_1[1]))/(distance)],[point_5[0] + (distance_h * (perpendicular_2[0]))/(distance), point_5[1] + (distance_h * (perpendicular_2[1]))/(distance)]]
    
    else:

        return True , []

def find_x_max(radius, position_y, padding_k_h):
    try:

        return False, [ math.sqrt(radius**2 - (position_y - padding_k_h[0])**2) + padding_k_h[1] , -math.sqrt(radius**2 - (position_y - padding_k_h[0])**2) + padding_k_h[1] ]
    
    except:

        return True, []
    
def kinematic(base_arm, size_whole_arm, angles):

    error, center_1 = get_base_point_upper_arm(base_arm[0], size_whole_arm[0], angles[0])
    
    if error :
        return True, [1]
    
    error, center_2 = get_base_point_upper_arm(base_arm[1], size_whole_arm[0], angles[1])

    if error :
        return True, [0]

    error, result = intersection_points(size_whole_arm[1], [center_1, center_2])

    if error :
        return True, [-1]

    return False, result[1]

def limitations(min_point, max_point, point):

    if point[1] < min_point[1] or point[1] > max_point[1] or point[0] < min_point[0] or point[0] > max_point[0]:

        return True
    
    return False