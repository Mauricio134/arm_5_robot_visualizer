import time
import func
import tkinter as tk
import math
import matplotlib.pyplot as plt
import numpy as np

# Features of NEMA 14 Stepper Motor
rpm = 5
angles_per_second = rpm * 6

angles_per_second_pos = angles_per_second
angles_per_second_neg = -angles_per_second

angles_per_step = 1.8

duration = 6000

# Features of five arm parallel robot
size_a = 76.34
size_b = 94.66
base_arm_1_x, base_arm_1_y = -20.5, 0
base_arm_2_x, base_arm_2_y = 20.5, 0
size_between_motors = func.findD(base_arm_2_x, base_arm_2_y, base_arm_1_x, base_arm_1_y)

# Features of target
init_target_x, init_target_y = 0, base_arm_1_y + 150
fin_target_x, fin_target_y = 130, 72

# Init Angles
# Faces
init_face_1 = func.findD(base_arm_1_x, base_arm_1_y, init_target_x, init_target_y)
init_face_2 = func.findD(base_arm_2_x, base_arm_2_y, init_target_x, init_target_y)

# Angles in motor 1
init_theta_2 = func.findAngSide(size_a, init_face_1, size_b)
init_theta_3 = func.findAngSide(init_face_1, size_between_motors, init_face_2)
init_theta_total = init_theta_2 + init_theta_3

# Angles in motor 2
init_beta_2 = func.findAngSide(size_a, init_face_2, size_b)
init_beta_3 = func.findAngSide(init_face_2, size_between_motors, init_face_1)
init_beta_1 = 180.0 - (init_beta_3 + init_beta_2)

# End Angles
# Faces
fin_face_1 = func.findD(base_arm_1_x, base_arm_1_y, fin_target_x, fin_target_y)
fin_face_2 = func.findD(base_arm_2_x, base_arm_2_y, fin_target_x, fin_target_y)

# Angles in motor 1
fin_theta_2 = func.findAngSide(size_a, fin_face_1, size_b)
fin_theta_3 = func.findAngSide(fin_face_1, size_between_motors, fin_face_2)
fin_theta_total = fin_theta_2 + fin_theta_3

# Angles in motor 2
fin_beta_2 = func.findAngSide(size_a, fin_face_2, size_b)
fin_beta_3 = func.findAngSide(fin_face_2, size_between_motors, fin_face_1)
fin_beta_1 = 180.0 - (fin_beta_3 + fin_beta_2)

# New version of angles

minimum_y = base_arm_1_y + 30
maximum_y = func.intersection_points(size_a + size_b, [base_arm_1_x, base_arm_1_y], [base_arm_2_x, base_arm_2_y])[1][1]

maximum_x = func.get_x_max(0, size_a + size_b, base_arm_1_x, base_arm_1_y)[0]
minimum_x = -maximum_x

max_point = [maximum_x, maximum_y]
min_point = [minimum_x, minimum_y]

# omegas = func.get_omegas([size_a, size_b], size_between_motors, fin_target_x, fin_target_y)
# betas = func.get_beta(size_between_motors, max_point, min_point, [base_arm_1_x, base_arm_1_y], [base_arm_2_x, base_arm_2_y], fin_target_x, fin_target_y)

# theta_1 = betas[0] + omegas[0]
# theta_2 = betas[1] - omegas[1]

# if theta_1 % angles_per_step != 0:
#     theta_1 -= theta_1 % angles_per_step

# if theta_2 % angles_per_step != 0:
#     theta_2 -= theta_2 % angles_per_step

# extremo_1 = func.get_extremes(size_a, [base_arm_1_x, base_arm_1_y], theta_1)
# extremo_2 = func.get_extremes(size_a, [base_arm_2_x, base_arm_2_y], theta_2)

# intersections = func.intersection_points(size_b, extremo_1, extremo_2)

# fin_target_x = intersections[1][0]
# fin_target_y = intersections[1][1]

distance_height = func.findD(0,minimum_y, 0, maximum_y)
distance_width = func.findD(minimum_x, minimum_y, maximum_x, minimum_y)

simple_or_each = False

num_large_h = func.largest_divisor(distance_height)
num_large_w = func.largest_divisor(distance_width)

if(simple_or_each == True):
    num_large_h = func.gcd(distance_height, distance_width)
    num_large_w = num_large_h

# extremo_1 = func.get_extremes(size_a, [base_arm_1_x, base_arm_1_y], theta_1)
# extremo_2 = func.get_extremes(size_a, [base_arm_2_x, base_arm_2_y], theta_2)

# intersections = func.intersection_points(size_b, extremo_1, extremo_2)

# print(intersections[1])

mapped_x = []
mapped_y = []

whole_map = []

row = 0
column = 0

exact_row = 0
exact_column = 0

total_row = (-minimum_y+maximum_y)/num_large_h + 1
total_column = (-minimum_x+maximum_x)/num_large_w + 1

for i in range(minimum_y, maximum_y+1, num_large_h):
    fila = []
    for j in range(minimum_x, maximum_x +1, num_large_w):
        try:
            omegas = func.get_omegas([size_a, size_b], size_between_motors, j, i)
            betas = func.get_beta(size_between_motors, max_point, min_point, [base_arm_1_x, base_arm_1_y], [base_arm_2_x, base_arm_2_y], j, i)

            theta_1 = betas[0] + omegas[0]
            theta_2 = betas[1] - omegas[1]

            if theta_1 % angles_per_step != 0:
                theta_1 = round(theta_1/angles_per_step) * angles_per_step

            if theta_2 % angles_per_step != 0:
                theta_2 = round(theta_2/angles_per_step) * angles_per_step
            
            extremo_1 = func.get_extremes(size_a, [base_arm_1_x, base_arm_1_y], theta_1)
            extremo_2 = func.get_extremes(size_a, [base_arm_2_x, base_arm_2_y], theta_2)

            intersections = func.intersection_points(size_b, extremo_1, extremo_2)
            mapped_x.append(intersections[1][0])
            mapped_y.append(intersections[1][1])
            if intersections[1][0] == 0 and whole_map[exact_row][exact_column] > intersections[1][1]:
                exact_row = row
                exact_column = column
            fila.append(intersections[1])
        except:
            mapped_x = mapped_x
            mapped_y = mapped_y
            fila.append([-999,-999])
        
        column += 1
    whole_map.append(fila)
    row += 1
    column = 0
print(whole_map[exact_row][exact_column])
plt.plot(whole_map[exact_row][exact_column][0], whole_map[exact_row][exact_column][1], 'x')
plt.plot(mapped_x, mapped_y, 'o')
plt.plot([base_arm_1_x, base_arm_2_x], [base_arm_1_y, base_arm_2_y], 'x')
plt.plot(fin_target_x, fin_target_y, 'x')
plt.show()

accesability_path = func.reachibility_path(whole_map, exact_row, exact_column, total_row, total_column, fin_target_x, fin_target_y, min(num_large_h, num_large_w))

print(accesability_path)