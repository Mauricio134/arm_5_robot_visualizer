import math
import matplotlib.pyplot as plt

def get_euclidean_distance(init, fin):
    delta_x = (fin[0] - init[0])**2
    delta_y = (fin[1] - init[1])**2
    return math.sqrt(delta_x + delta_y)

def get_omegas(arms_size, separation, target_x, target_y):
    L0 = separation / 2

    k = math.sqrt((target_x + L0)**2+target_y**2)
    s = math.sqrt((target_x - L0)**2+target_y**2)
    return [math.degrees(math.acos((arms_size[0]**2-arms_size[1]**2+k**2)/(2*arms_size[0]*k))),math.degrees(math.acos((arms_size[0]**2-arms_size[1]**2+s**2)/(2*arms_size[0]*s)))]

def get_beta(separation, max_point, min_point, center_1, center_2, target_x, target_y):
    L0 = separation/2
    if( center_2[0] <= target_x <= max_point[0] and min_point[1] <= target_y <= max_point[1] ):
        return [math.degrees(math.atan(target_y/abs(L0+target_x))),math.degrees(math.atan(target_y/abs(L0 - target_x)))]
    elif ( center_1[0] <= target_x < center_2[0] and min_point[1] <= target_y <= max_point[1] ):
        return [math.degrees(math.atan(target_y/abs(L0+target_x))),math.degrees(math.pi - math.atan(target_y/abs(L0 - target_x)))]
    elif ( min_point[0] <= target_x < center_1[0] and min_point[1] <= target_y <= max_point[1]):
        return [math.degrees(math.pi - math.atan(target_y/abs(L0+target_x))),math.degrees(math.pi - math.atan(target_y/abs(L0 - target_x)))]
    return []

def intersection_points(size, center_1, center_2):

    distance = get_euclidean_distance(center_1, center_2)

    if distance < size*2:
        distance_a = (size**2 - size**2 + distance**2) / (2*distance)
        distance_b = distance_a

        distance_h = round(math.sqrt(size**2-distance_a**2), 1)

        point_5 = [0,0]

        point_5[0] = center_1[0] + (distance_a/distance) * (center_2[0] - center_1[0])
        point_5[1] = center_1[1] + (distance_a/distance) * (center_2[1] - center_1[1])

        perpendicular_1 = [center_2[1] - center_1[1], center_1[0] - center_2[0]]
        perpendicular_2 = [center_1[1] - center_2[1], center_2[0] - center_1[0]]

        return [[point_5[0] + (distance_h * (perpendicular_1[0]))/(distance), point_5[1] + (distance_h * (perpendicular_1[1]))/(distance)],[point_5[0] + (distance_h * (perpendicular_2[0]))/(distance), point_5[1] + (distance_h * (perpendicular_2[1]))/(distance)]]
    else:
        print("There are not interseccioned points")
        return []
    
def get_x_max(y, R, h, k):
    return [math.sqrt(R**2-(y-k)**2)+h, -math.sqrt(R**2-(y-k)**2)+h]

def gcd(a,b):

    n = min(a,b)

    while(n > 0):
        if(a % n == 0 and b % n == 0):
            break
        n-=1

    return n

def largest_divisor(n):

    i = int(math.sqrt(n))

    while(i >= 1):
        if n % i == 0:
            return i
        i-=1
        
    return math.sqrt(n)

def get_extremes(size, arm, angle):
    extremo_x = arm[0] + size * math.cos(math.radians(angle))
    extremo_y = arm[1] + size * math.sin(math.radians(angle))

    return [extremo_x, extremo_y]

def get_grid_movement(min_point, max_point, size_whole_arm_array, size_between_motors, base_arm_1, base_arm_2, angles_per_step,simple_or_each, padding_y):
    whole_map = []
    whole_degrees = []

    row = 0
    column = 0

    exact_row = 0
    exact_column = 0

    min_point = [min_point[0], min_point[1] + padding_y]

    distance_height = get_euclidean_distance([min_point[0], min_point[1]], [min_point[0], max_point[1]])
    distance_width = get_euclidean_distance([min_point[0], min_point[1]], [max_point[0], min_point[1]])

    num_large_h = largest_divisor(distance_height)
    num_large_w = largest_divisor(distance_width)

    if(simple_or_each == True):
        num_large_h = gcd(distance_height, distance_width)
        num_large_w = num_large_h

    total_row = (-min_point[1]+max_point[1])/num_large_h + 1
    total_column = (-min_point[0]+max_point[0])/num_large_w + 1

    actual_distance = 999999

    for i in range(int(min_point[1]), int(max_point[1])+1, int(num_large_h)):
        fila_1 = []
        fila_2 = []
        for j in range(int(min_point[0]), int(max_point[0]) +1,int(num_large_w)):
            try:
                omegas = get_omegas(size_whole_arm_array, size_between_motors, j, i)
                betas = get_beta(size_between_motors, max_point, min_point, base_arm_1, base_arm_2, j, i)

                theta_1 = betas[0] + omegas[0]
                theta_2 = betas[1] - omegas[1]

                if theta_1 % angles_per_step != 0:
                    theta_1 = round(theta_1/angles_per_step) * angles_per_step

                if theta_2 % angles_per_step != 0:
                    theta_2 = round(theta_2/angles_per_step) * angles_per_step
                
                extremo_1 = get_extremes(size_whole_arm_array[0], base_arm_1, theta_1)
                extremo_2 = get_extremes(size_whole_arm_array[0], base_arm_2, theta_2)

                intersections = intersection_points(size_whole_arm_array[1], extremo_1, extremo_2)
                new_distance = get_euclidean_distance([0,min_point[1]],[intersections[1][0], intersections[1][1]])
                if actual_distance > new_distance:
                    actual_distance = new_distance
                    exact_row = row
                    exact_column = column
                fila_1.append(intersections[1])
                fila_2.append([theta_1, theta_2])
            except:
                fila_1.append([-999,-999])
                fila_2.append([])
            
            column += 1
        whole_map.append(fila_1)
        whole_degrees.append(fila_2)
        row += 1
        column = 0
    return whole_map, whole_degrees, [exact_row, exact_column], [total_row, total_column], [num_large_h, num_large_h]

def reachibility_path(whole_map, init_position, total_row, total_column, target, radius, sizes, size_between_motors, max_point, min_point, arm_1, arm_2, angles_per_step):
    path = []
    angles = []
    distances = []
    while(get_euclidean_distance(whole_map[init_position[0]][init_position[1]], target) > radius):
        min_y = init_position[0] - 1
        max_y = init_position[0] + 2
        min_x = init_position[1] - 1
        max_x = init_position[1] + 2

        if init_position[0] - 1 < 0:
            min_y = init_position[0]
        
        if init_position[0] + 2 >= total_row:
            max_y = init_position[0] + 1

        if init_position[1] - 1 < 0:
            min_x = init_position[1]

        if init_position[1] + 2 >= total_column:
            max_x = init_position[1] + 1
        
        distance = 9999
        new_row = -999
        new_column = -999
        for i in range(min_y, max_y):
            for j in range(min_x, max_x):
                if whole_map[i][j][0] == -999 or (whole_map[i][j][0] == whole_map[init_position[0]][init_position[1]][0] and whole_map[i][j][1] == whole_map[init_position[0]][init_position[1]][1]):
                    continue

                new_distance = get_euclidean_distance(whole_map[init_position[0]][init_position[1]], whole_map[i][j]) + get_euclidean_distance(whole_map[i][j], target)
                if new_distance < distance:
                    distance = new_distance
                    new_row = i
                    new_column = j
        
        init_position[0] = new_row
        init_position[1] = new_column

        omegas = get_omegas(sizes, size_between_motors, whole_map[init_position[0]][init_position[1]][0], whole_map[init_position[0]][init_position[1]][1])
        betas = get_beta(size_between_motors, max_point, min_point, arm_1, arm_2, whole_map[init_position[0]][init_position[1]][0], whole_map[init_position[0]][init_position[1]][1])

        theta_1 = betas[0] + omegas[0]
        theta_2 = betas[1] - omegas[1]

        theta_1 = round(theta_1/angles_per_step) * angles_per_step
        theta_2 = round(theta_2/angles_per_step) * angles_per_step

        path.append(whole_map[init_position[0]][init_position[1]])
        angles.append([theta_1, theta_2])
        distances.append([init_position[0], init_position[1]])
    
    return path, angles, distances