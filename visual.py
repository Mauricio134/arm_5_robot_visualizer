from tkinter import *
import general
import math
import general
import find_angles
import find_points
import time

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

    # canvas.update()

    return canvas, [extremo_x, extremo_y]

def create_upper_arm(canvas, center, extremes, tag):
    canvas.delete(tag)

    base_canvas = convert_to_canvas(center[0], center[1], canvas)

    extremo_canvas = convert_to_canvas(extremes[0], extremes[1], canvas)

    canvas.create_line(base_canvas[0], base_canvas[1], extremo_canvas[0], extremo_canvas[1], fill="blue", width=3, tags=tag)

    # canvas.update()

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


def create_change_position(canva, init_position, size_segments, size_whole_arm_array, size_between_motors, max_point, min_point, base_arm_1, base_arm_2, angles_per_step, entries, duration):

    new_entry_x = float(entries[0].get()) if entries[0].get() else 0

    new_entry_y = float(entries[1].get()) if entries[1].get() else 0

    error, path, references = general.find_path(size_whole_arm_array, init_position, [new_entry_x, new_entry_y], min_point, max_point, base_arm_1, base_arm_2, size_segments[0], size_segments[1], size_between_motors, angles_per_step, min(size_segments[0], size_segments[1]))
    
    if path == []:
        return 
    
    amount_angles = len(path)

    time_per_step = duration / amount_angles

    init_time = time.time() * 1000.0

    first = 0
    while first < len(path):

        current_time = time.time() * 1000.0

        if(current_time - init_time >= time_per_step):
            print(len(path))
            print(references)
            print(first)
            print(path[first], references[first])

            error, angles_init = find_angles.inverse_kinematic(size_whole_arm_array, min_point, max_point, base_arm_1, base_arm_2, path[first], references[first], size_between_motors, angles_per_step)

            print(angles_init[0], angles_init[1])

            canva, center_1 = create_down_arm(canva, base_arm_1, size_whole_arm_array[0], angles_init[0], "left_down_arm")

            canva, center_2 = create_down_arm(canva, base_arm_2, size_whole_arm_array[0], angles_init[1], "right_down_arm")

            canva = create_upper_arm(canva, center_1, path[first], "left_upper_arm")

            canva = create_upper_arm(canva, center_2, path[first], "right_upper_arm")

            canva.update()

            init_time = current_time

            first += 1




def create_window(separations, init_position, size_whole_arm_array, min_point, max_point, base_arm_1, base_arm_2, size_between_motors, angles_per_step, total_duration_ms):

    root = Tk()

    root.title("Five Arm Parallel Robot")

    width = root.winfo_screenwidth()

    height = root.winfo_screenheight()

    root.geometry("%dx%d" % (width, height))

    left = create_frame(root, "lightyellow", 0, 0, 0.25, 1.0)

    right = create_frame(root, "lightblue", 0.25, 0, 0.75, 1.0)

    grid = create_canva(right, "ivory")

    grid = create_grid(grid)

    error, angles = find_angles.inverse_kinematic(size_whole_arm_array, min_point, max_point, base_arm_1, base_arm_2, init_position, init_position, size_between_motors, angles_per_step)

    grid, center_1 = create_down_arm(grid, base_arm_1, size_whole_arm_array[0], angles[0], "left_down_arm")

    grid, center_2 = create_down_arm(grid, base_arm_2, size_whole_arm_array[1], angles[1], "right_down_arm")

    error, position = find_points.kinematic([base_arm_1, base_arm_2], size_whole_arm_array, angles)

    grid = create_upper_arm(grid, center_1, position, "left_upper_arm")

    grid = create_upper_arm(grid, center_2, position, "right_upper_arm")

    create_label(left, "Target X:")

    entry_x = create_entry(left)

    create_label(left, "Target Y:")

    entry_y = create_entry(left)

    button = create_button(left, "Send", lambda:create_change_position(grid, init_position, separations, size_whole_arm_array, size_between_motors, max_point, min_point, base_arm_1, base_arm_2, angles_per_step, [entry_x, entry_y], total_duration_ms))
    root.mainloop()