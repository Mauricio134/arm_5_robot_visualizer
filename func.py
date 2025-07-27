import math
import time

# Functions
def findD(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def findAngSide(a, b, c):
    cos_value = (a**2 + b**2 - c**2) / (2 * a * b)
    cos_value = max(min(cos_value, 1), -1)
    return math.degrees(math.acos(cos_value))