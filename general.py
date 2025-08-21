import math

def get_distance_between_points(init_point, fin_point):

    delta_x = ( fin_point[0] - init_point[0] ) ** 2

    delta_y = ( fin_point[1] - init_point[1] ) ** 2

    return math.sqrt( delta_x + delta_y )

def gcd(a,b):

    n = min(round(a),round(b))

    while(n > 0):
        print(n)
        if(a % n == 0 and b % n == 0):
            return True, n
        n-=1

    return False, 0.0

def largest_divisor(n):

    i = int(math.sqrt(n))

    while(i >= 1):
        if n % i == 0:
            return i
        i-=1
        
    return math.sqrt(n)