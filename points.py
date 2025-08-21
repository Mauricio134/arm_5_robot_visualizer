import math
import general
import create_angles

def get_extremes(size, arm, angle):
    try:
        extremo_x = arm[0] + size * math.cos(math.radians(angle))
        extremo_y = arm[1] + size * math.sin(math.radians(angle))

        return [extremo_x, extremo_y]
    except:
        print("Error in points.py, get_extremes")
        return []

def intersection_points(size, center_1, center_2):

    distance = general.get_euclidean_distance(center_1, center_2)

    if distance < size*2:
        distance_a = (size**2 - size**2 + distance**2) / (2*distance)
        distance_b = distance_a

        distance_h = math.sqrt(size**2-distance_a**2)

        point_5 = [0,0]

        point_5[0] = center_1[0] + (distance_a/distance) * (center_2[0] - center_1[0])
        point_5[1] = center_1[1] + (distance_a/distance) * (center_2[1] - center_1[1])

        perpendicular_1 = [center_2[1] - center_1[1], center_1[0] - center_2[0]]
        perpendicular_2 = [center_1[1] - center_2[1], center_2[0] - center_1[0]]

        return [[point_5[0] + (distance_h * (perpendicular_1[0]))/(distance), point_5[1] + (distance_h * (perpendicular_1[1]))/(distance)],[point_5[0] + (distance_h * (perpendicular_2[0]))/(distance), point_5[1] + (distance_h * (perpendicular_2[1]))/(distance)]]
    else:
        print("Error in points.py, intersection_points")
        return []
    
def convert_positions(size_whole_arm_array, min_point, max_point, base_arm_1, base_arm_2, target, init_position, size_between_motors, angles_per_step):

    angles = create_angles.get_motor_angles_1(size_whole_arm_array, min_point, max_point, base_arm_1, base_arm_2, target, init_position, size_between_motors)

    if angles[0] % angles_per_step != 0:
        angles[0] = round(angles[0]/angles_per_step) * angles_per_step

    if angles[1] % angles_per_step != 0:
        angles[1] = round(angles[1]/angles_per_step) * angles_per_step

    center_1 = get_extremes(size_whole_arm_array[0], base_arm_1, angles[0])

    center_2 = get_extremes(size_whole_arm_array[0], base_arm_2, angles[1])

    intersections = intersection_points(size_whole_arm_array[1], center_1, center_2)

    return angles, intersections