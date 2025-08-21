import math
import general

def get_base_point_upper_arm(point_position_base_lower_arm, size_lower_arm, angle_lower_arm):

    extremo_x = point_position_base_lower_arm[0] + size_lower_arm * math.cos(math.radians(angle_lower_arm))

    extremo_y = point_position_base_lower_arm[1] + size_lower_arm * math.sin(math.radians(angle_lower_arm))

    return [extremo_x, extremo_y]

def intersection_points(size_upper_arm, point_position_base_lower_arm):

    distance = general.get_distance_between_points(point_position_base_lower_arm[0], point_position_base_lower_arm[1])

    if distance < size_upper_arm*2:
        distance_a = (size_upper_arm**2 - size_upper_arm**2 + distance**2) / (2*distance)
        distance_b = distance_a

        distance_h = math.sqrt(size_upper_arm**2-distance_a**2)

        point_5 = [0,0]

        point_5[0] = point_position_base_lower_arm[0][0] + (distance_a/distance) * (point_position_base_lower_arm[1][0] - point_position_base_lower_arm[0][0])
        point_5[1] = point_position_base_lower_arm[0][1] + (distance_a/distance) * (point_position_base_lower_arm[1][1] - point_position_base_lower_arm[0][1])

        perpendicular_1 = [point_position_base_lower_arm[1][1] - point_position_base_lower_arm[0][1], point_position_base_lower_arm[0][0] - point_position_base_lower_arm[1][0]]
        perpendicular_2 = [point_position_base_lower_arm[0][1] - point_position_base_lower_arm[1][1], point_position_base_lower_arm[1][0] - point_position_base_lower_arm[0][0]]

        return True , [[point_5[0] + (distance_h * (perpendicular_1[0]))/(distance), point_5[1] + (distance_h * (perpendicular_1[1]))/(distance)],[point_5[0] + (distance_h * (perpendicular_2[0]))/(distance), point_5[1] + (distance_h * (perpendicular_2[1]))/(distance)]]
    else:
        return False , []

def find_x_max(radius, position_y, padding_k_h):
    try:    
        return True, [ math.sqrt(radius**2 - (position_y - padding_k_h[0])**2) + padding_k_h[1] , -math.sqrt(radius**2 - (position_y - padding_k_h[0])**2) + padding_k_h[1] ]
    except:
        return False, []