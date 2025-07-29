import time
import func
import tkinter as tk
import math

# Features of NEMA 14 Stepper Motor
rpm = 5
angles_per_second = rpm * 6

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

func.create_window([init_target_x, init_target_y], angles_per_step, duration, [size_a, size_b], [base_arm_1_x, base_arm_1_y], [base_arm_2_x, base_arm_2_y], size_between_motors)