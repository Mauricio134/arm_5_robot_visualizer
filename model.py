import time
import func
import tkinter as tk
import math

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
init_target_x, init_target_y = -36, 30
fin_target_x, fin_target_y = 30, 30

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
minimim_x = -maximum_x

max_point = [maximum_x, maximum_y]
min_point = [minimim_x, minimum_y]

omegas = func.get_omegas([size_a, size_b], size_between_motors, fin_target_x, fin_target_y,)
betas = func.get_beta(size_between_motors, max_point, min_point, [base_arm_1_x, base_arm_1_y], [base_arm_2_x, base_arm_2_y], fin_target_x, fin_target_y)

theta_1 = betas[0] + omegas[0]
theta_2 = betas[1] - omegas[1]

print(fin_theta_total, theta_1)
print(fin_beta_1, theta_2)

omegas = func.get_omegas([size_a, size_b], size_between_motors, init_target_x, init_target_y)
betas = func.get_beta(size_between_motors, max_point, min_point, [base_arm_1_x, base_arm_1_y], [base_arm_2_x, base_arm_2_y], init_target_x, init_target_y)

theta_1 = betas[0] + omegas[0]
theta_2 = betas[1] - omegas[1]

print(init_theta_total, theta_1)
print(init_beta_1, theta_2)


