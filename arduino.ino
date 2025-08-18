#include <iostream>
#include <cmath>

using namespace std;

#define STEPS 200

double get_euclidean_distance(double init[2], double fin[2]);

double angles_per_step = 1.8;
double total_duration_ms = 6000;

double size_lower_arm = 76.34;
double size_upper_arm = 94.66;
double size_whole_arm = size_lower_arm + size_upper_arm;

double size_whole_arm_array[2];
size_whole_arm_array[0] = size_lower_arm;
size_whole_arm_array[1] = size_upper_arm;

double base_arm_1[2] = {-20.5, 0};
double base_arm_2[2] = {20.5, 0};

double size_between_motors = get_euclidean_distance(base_arm_1, base_arm_2);

double get_euclidean_distance(double init[2], double fin[2]){

    double delta_x = pow((fin[0] - init[0]), 2);

    double delta_y = pow((fin[1] - init[1]), 2);

    return sqrt(delta_x + delta_y);
}
