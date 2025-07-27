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
base_arm_1_x, base_arm_1_y = -20.5, -30.0
base_arm_2_x, base_arm_2_y = 20.5, -30.0
size_between_motors = func.findD(base_arm_2_x, base_arm_2_y, base_arm_1_x, base_arm_1_y)

# Features of target
init_target_x, init_target_y = 0, 0
fin_target_x, fin_target_y = 0, 0

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


print("Before Init Angle in Motor 1:", init_theta_total)
print("Before Init Angle in Motor 2:", init_beta_1)
print()

# Movement
if(init_target_x != fin_target_x or init_target_y != fin_target_y):
    delta_angle_1, delta_angle_2 = fin_theta_total - init_theta_total, fin_beta_1 - init_beta_1

    direction_angle_1 = (delta_angle_1 > 0)
    direction_angle_2 = (delta_angle_2 > 0)

    angles_per_step_1 = angles_per_step
    angles_per_step_2 = angles_per_step

    if(direction_angle_1 == False): angles_per_step_1 = -angles_per_step_1
    if(direction_angle_2 == False): angles_per_step_2 = -angles_per_step_2

    angle_change_1, angle_change_2 = math.floor(abs(delta_angle_1 / angles_per_step)), math.floor(abs(delta_angle_2 / angles_per_step))

    delta_duration_1, delta_duration_2 = duration / angle_change_1, duration / angle_change_2

    last_time = time.time() * 1000.0

    while angle_change_1 > 0 or angle_change_2 > 0:

        current_time = time.time() * 1000.0
        elapsed_time = current_time - last_time

        if(angle_change_1 > 0 and elapsed_time >= delta_duration_1):
            init_theta_total += angles_per_step_1
            angle_change_1 -= 1

        current_time = time.time() * 1000.0
        elapsed_time = current_time - last_time

        if(angle_change_2 > 0 and elapsed_time >= delta_duration_2):
            init_beta_1 += angles_per_step_2
            angle_change_2 -= 1
    

print("After Init Angle in Motor 1:", init_theta_total)
print("After Init Angle in Motor 2:", init_beta_1)
print()
print("Fin Angle in Motor 1:", fin_theta_total)
print("Fin Angle in Motor 2:", fin_beta_1)
print()