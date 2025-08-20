import math

def get_euclidean_distance(init, fin):
    delta_x = (fin[0] - init[0])**2
    delta_y = (fin[1] - init[1])**2
    return math.sqrt(delta_x + delta_y)
    
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