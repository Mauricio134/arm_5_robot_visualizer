import math
import time
from tkinter import *

# Functions
def findD(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def findAngSide(a, b, c):
    cos_value = (a**2 + b**2 - c**2) / (2 * a * b)
    cos_value = max(min(cos_value, 1), -1)
    return math.degrees(math.acos(cos_value))

def get_motor_angles(sizes, arm_left, arm_right, target, size_between_motors):
    # Faces
    face_1 = findD(arm_left[0], arm_left[1], target[0], target[1])
    face_2 = findD(arm_right[0], arm_right[1], target[0], target[1])

    # Angles in motor 1
    theta_2 = findAngSide(sizes[0], face_1, sizes[1])
    theta_3 = findAngSide(face_1, size_between_motors, face_2)
    theta_total = theta_2 + theta_3

    # Angles in motor 2
    beta_2 = findAngSide(sizes[0], face_2, sizes[1])
    beta_3 = findAngSide(face_2, size_between_motors, face_1)
    beta_1 = 180.0 - (beta_3 + beta_2)

    return [theta_total, beta_1]

def convert_to_canvas(x, y, canvas):
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    canvas_x = (x + 200) / 400 * width
    canvas_y = (200 - y) / 400 * height

    return canvas_x, canvas_y

def create_frame(root, color, relx, rely, relwidth, relheight):
    frame = Frame(root, background=color)
    frame.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)

    return frame

def create_canva(root, color):
    canva = Canvas(root, bg=color)
    canva.pack(fill=BOTH, expand=True, padx=10, pady=10)
    return canva

def create_grid(canvas):
    # Get size of the Canvas
    canvas.update()
    ancho = canvas.winfo_width()
    alto = canvas.winfo_height()
    
    # Clean Canvas
    canvas.delete("all")
    
    # Center Canvas
    centro_x = ancho // 2
    centro_y = alto // 2
    
    # Draw axis (X=0 e Y=0)
    canvas.create_line(0, centro_y, ancho, centro_y, fill="black", width=2)  # Eje X
    canvas.create_line(centro_x, 0, centro_x, alto, fill="black", width=2)   # Eje Y
    
    # Draw coordinates lines in the axis
    espaciado = min(ancho, alto) / 30
    
    for i in range(1, 20):
        x_pos = centro_x + (i * espaciado)
        canvas.create_line(x_pos, 0, x_pos, alto, fill="gray", width=1)
        x_neg = centro_x - (i * espaciado) 
        canvas.create_line(x_neg, 0, x_neg, alto, fill="gray", width=1)

        y_pos = centro_y + (i * espaciado)
        canvas.create_line(0, y_pos, ancho, y_pos, fill="gray", width=1)
        y_neg = centro_y - (i * espaciado)
        canvas.create_line(0, y_neg, ancho, y_neg, fill="gray", width=1)
    
    # Draw the numbers
    canvas.create_text(centro_x + 20, centro_y + 20, text="(0,0)", font=("Arial", 10))
    canvas.create_text(ancho - 30, centro_y + 20, text="+200", font=("Arial", 10))
    canvas.create_text(30, centro_y + 20, text="-200", font=("Arial", 10))
    canvas.create_text(centro_x + 20, 20, text="+200", font=("Arial", 10))
    canvas.create_text(centro_x + 20, alto - 20, text="-200", font=("Arial", 10))

    return canvas

def create_down_arm(canvas, arm, size, angle, tag):
    canvas.delete(tag)

    base_canvas = convert_to_canvas(arm[0], arm[1], canvas)

    extremo_x = arm[0] + size * math.cos(math.radians(angle))
    extremo_y = arm[1] + size * math.sin(math.radians(angle))

    extremo_canvas = convert_to_canvas(extremo_x, extremo_y, canvas)

    canvas.create_line(base_canvas[0], base_canvas[1], extremo_canvas[0], extremo_canvas[1], fill="red", width=3, tags=tag)
    canvas.update()
    return canvas, [extremo_x, extremo_y]

def intersection_points(size, center_1, center_2):

    distance = findD(center_1[0], center_1[1], center_2[0], center_2[1])

    if distance < size*2:
        distance_a = (size**2 - size**2 + distance**2) / (2*distance)
        distance_b = distance_a

        distance_h = math.sqrt(size**2-distance_a**2)

        point_5 = [0,0]

        point_5[0] = center_1[0] + (distance_a/distance) * (center_2[0] - center_1[0])
        point_5[1] = center_1[1] + (distance_a/distance) * (center_2[1] - center_1[1])

        perpendicular_1 = [center_2[1] - center_1[1], center_1[0] - center_2[0]]
        perpendicular_2 = [center_1[1] - center_2[1], center_2[0] - center_1[0]]

        return [[round(point_5[0] + (distance_h * (perpendicular_1[0]))/(distance)), round(point_5[1] + (distance_h * (perpendicular_1[1]))/(distance))],[round(point_5[0] + (distance_h * (perpendicular_2[0]))/(distance)), round(point_5[1] + (distance_h * (perpendicular_2[1]))/(distance))]]
    else:
        print("There are not intersectional points")
        return []

def create_upper_arm(canvas, center, extremes, tag):
    canvas.delete(tag)

    base_canvas = convert_to_canvas(center[0], center[1], canvas)

    extremo_canvas = convert_to_canvas(extremes[0], extremes[1], canvas)

    canvas.create_line(base_canvas[0], base_canvas[1], extremo_canvas[0], extremo_canvas[1], fill="blue", width=3, tags=tag)
    canvas.update()
    return canvas

def create_entry(root):
    entry = Entry(root, font=("Arial", 12))
    entry.pack(pady=5)
    return entry

def create_label(root, title):
    Label(root, text=title, font=("Arial", 12)).pack(pady=10)

def create_button(root, text, action):
    btn = Button(root, text=text, font=("Arial", 12), command=action)
    btn.pack(pady=20)

    return btn

def create_change_position(canva, arms, sizes, target, entries, angles_init, size_between_motors, duration, angles_per_step):

    print("Before Init Angle in Motor 1:", angles_init[0])
    print("Before Init Angle in Motor 2:", angles_init[1])
    print()

    new_entry_x = float(entries[0].get()) if entries[0].get() else 0
    new_entry_y = float(entries[1].get()) if entries[1].get() else 0
    
    if new_entry_x < -200 or new_entry_x > 200 or new_entry_y < -200 or new_entry_y > 200:
        print("Error: Los valores deben estar entre -200 y 200")
        return
    
    new_entries = [new_entry_x, new_entry_y]

    angles_end = get_motor_angles(sizes, arms[0], arms[1], new_entries, size_between_motors)

    print(angles_end[0])
    print(angles_end[1])
    # Movement
    if(target[0] != new_entry_x or target[1] != new_entry_y):
        delta_angle_1, delta_angle_2 = angles_end[0] - angles_init[0], angles_end[1] - angles_init[1]

        print(delta_angle_1)
        print(delta_angle_2)
        print(angles_per_step)

        direction_angle_1 = (delta_angle_1 > 0)
        direction_angle_2 = (delta_angle_2 > 0)

        angles_per_step_1 = angles_per_step
        angles_per_step_2 = angles_per_step

        if(direction_angle_1 == False): angles_per_step_1 = -angles_per_step_1
        if(direction_angle_2 == False): angles_per_step_2 = -angles_per_step_2

        angle_change_1, angle_change_2 = math.floor(abs(delta_angle_1 / angles_per_step)), math.floor(abs(delta_angle_2 / angles_per_step))

        print(abs(delta_angle_1 / angles_per_step))
        print(abs(delta_angle_2 / angles_per_step))

        if(angle_change_1 > 0):
            delta_duration_1 = duration / angle_change_1
            
        if(angle_change_2 > 0):
            delta_duration_2 =duration / angle_change_2

        last_time = time.time() * 1000.0

        while angle_change_1 > 0 or angle_change_2 > 0:

            current_time = time.time() * 1000.0
            elapsed_time = current_time - last_time

            if(angle_change_1 > 0 and elapsed_time >= delta_duration_1):
                angles_init[0] += angles_per_step_1
                angle_change_1 -= 1
                if angle_change_2 > 0:
                    angles_init[1] += angles_per_step_2
                    angle_change_2 -= 1
                canva, center_1 = create_down_arm(canva, arms[0], sizes[0], angles_init[0], "left_down_arm")
                canva, center_2 = create_down_arm(canva, arms[1], sizes[0], angles_init[1], "right_down_arm")
                intersections = intersection_points(sizes[1], center_1, center_2)
                canva = create_upper_arm(canva, center_1, intersections[1], "left_upper_arm")
                canva = create_upper_arm(canva, center_2, intersections[1], "right_upper_arm")
                last_time = time.time() * 1000.0

            current_time = time.time() * 1000.0
            elapsed_time = current_time - last_time

            if(angle_change_2 > 0 and elapsed_time >= delta_duration_2):
                if angle_change_1 > 0:
                    angles_init[0] += angles_per_step_1
                    angle_change_1 -= 1
                angles_init[1] += angles_per_step_2
                angle_change_2 -= 1
                canva, center_1 = create_down_arm(canva, arms[0], sizes[0], angles_init[0], "left_down_arm")
                canva, center_2 = create_down_arm(canva, arms[1], sizes[0], angles_init[1], "right_down_arm")

                intersections = intersection_points(sizes[1], center_1, center_2)
                canva = create_upper_arm(canva, center_1, intersections[1], "left_upper_arm")
                canva = create_upper_arm(canva, center_2, intersections[1], "right_upper_arm")
                last_time = time.time() * 1000.0
    
    target[0] = new_entry_x
    target[1] = new_entry_y

    print("After Init Angle in Motor 1:", angles_init[0])
    print("After Init Angle in Motor 2:", angles_init[1])
    print()
    print("Fin Angle in Motor 1:", angles_end[0])
    print("Fin Angle in Motor 2:", angles_end[1])
    print()

def create_window(target, angles_per_step, duration, arms_size, arm_left, arm_right, size_between_motors):
    root = Tk()
    root.title("Five Arm Parallel Robot")
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))

    left = create_frame(root, "lightyellow", 0, 0, 0.25, 1.0)

    right = create_frame(root, "lightblue", 0.25, 0, 0.75, 1.0)

    grid = create_canva(right, "ivory")

    grid = create_grid(grid)

    angles = get_motor_angles(arms_size, arm_left, arm_right, target, size_between_motors)

    grid, center_1 = create_down_arm(grid, arm_left, arms_size[0], angles[0], "left_down_arm")

    grid, center_2 = create_down_arm(grid, arm_right, arms_size[0], angles[1], "right_down_arm")

    intersections = intersection_points(arms_size[1], center_1, center_2)

    grid = create_upper_arm(grid, center_1, intersections[1], "left_upper_arm")

    grid = create_upper_arm(grid, center_2, intersections[1], "right_upper_arm")

    create_label(left, "Target X:")
    entry_x = create_entry(left)

    create_label(left, "Target Y:")
    entry_y = create_entry(left)

    arms = [arm_left, arm_right]
    entries = [entry_x, entry_y]

    button = create_button(left, "Send", lambda:create_change_position(grid, arms, arms_size, target, entries, angles, size_between_motors, duration, angles_per_step))

    root.mainloop()