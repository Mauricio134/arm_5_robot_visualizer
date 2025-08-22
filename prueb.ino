#include <AccelStepper.h>
#include <math.h>

using namespace std;

#define STEPS 200

AccelStepper motor_1(AccelStepper::DRIVER, 7, 6);
AccelStepper motor_2(AccelStepper::DRIVER, 9, 8);

float error;

float result_1[2];
float result_2[2];
float result_3;

float angles_per_step;
float total_duration_ms;

float size_lower_arm;
float size_upper_arm;

float size_whole_arm[2];

float base_arm_1[2];
float base_arm_2[2];

float height_of_the_base = 35.0;
float simple_or_each = false;

float distance_between_motors;

float init_position[2];

float min_point_y;
float max_point_y;
float max_point_x;
float min_point_x;

float max_point[2];
float min_point[2];

float num_large_h;
float num_large_w;

float size_segments[2];

float get_distance_between_points(float * init, float * fin){
  float delta_x = pow((fin[0] - init[0]), 2);
  float delta_y = pow((fin[1] - init[1]), 2);
  return sqrt(delta_x + delta_y);
}

bool intersection_points(float radius, float centers_rotation[2][2], float* result_x, float* result_y) {
  
  float distance = get_distance_between_points(centers_rotation[0], centers_rotation[1]);
  
  if (distance < radius * 2.0) {
    // Intersection exists
    float distance_a = (radius * radius - radius * radius + distance * distance) / (2.0 * distance);
    float distance_h = sqrt(radius * radius - distance_a * distance_a);
    
    // Calculate midpoint
    float mid_x = centers_rotation[0][0] + (distance_a / distance) * (centers_rotation[1][0] - centers_rotation[0][0]);
    float mid_y = centers_rotation[0][1] + (distance_a / distance) * (centers_rotation[1][1] - centers_rotation[0][1]);
    
    // Calculate perpendicular vectors (normalized by distance)
    float perp1_x = (centers_rotation[1][1] - centers_rotation[0][1]) / distance;
    float perp1_y = (centers_rotation[0][0] - centers_rotation[1][0]) / distance;
    
    // Calculate intersection points
    result_x[0] = mid_x + distance_h * perp1_x;
    result_y[0] = mid_y + distance_h * perp1_y;
    
    result_x[1] = mid_x - distance_h * perp1_x;
    result_y[1] = mid_y - distance_h * perp1_y;
    
    return false; // Intersection found
  } else {
    return true; // No intersection
  }
}

bool find_x_max(float radius, float position_y, float * padding_k_h, float * result){

  float sqrt_entry = pow(radius , 2) - pow(position_y - padding_k_h[0] , 2);

  if( sqrt_entry < 0.0 ){
    return true;
  }

  float valor = sqrt(sqrt_entry);

  result[0] = valor + padding_k_h[1];
  result[1] = -valor + padding_k_h[0];

  return false;
}

float largest_divisor(float n){
  float result = sqrt(n);
  float i = int(result);

  while (i >= 1 ){
    if(fmod(n,i) == 0.0) return i;
    i--;
  }

  return result;
}

bool gcd(float a, float b, float &result){
  float n = min(round(a), round(b));

  while(n > 0.0){
    if(fmod(a,n) == 0.0 && fmod(b,n) == 0.0){
      result = n;
      return false;
    }
    n--;
  }
  result = 0.0;
  return true;
}

bool get_omegas(float arms_size[2], float separation, float target_x, float target_y, float * result) {
 
  float L0 = separation / 2.0;

  float k = sqrt(pow((target_x + L0), 2) + pow(target_y, 2));
  float s = sqrt(pow((target_x - L0), 2) + pow(target_y, 2));

  float cos_value_1 = (pow(arms_size[0], 2) - pow(arms_size[1], 2) + pow(k, 2)) / (2.0 * arms_size[0] * k);
  float cos_value_2 = (pow(arms_size[0], 2) - pow(arms_size[1], 2) + pow(s, 2)) / (2.0 * arms_size[0] * s);

  if (cos_value_1 < -1.0 || cos_value_1 > 1.0 || cos_value_2 < -1.0 || cos_value_2 > 1.0) {
    return true;
  }

  result[0] = degrees(acos(cos_value_1));
  result[1] = degrees(acos(cos_value_2));

  return false;
}

bool get_beta(float separation, float max_point[2], float min_point[2], float center_1[2], float center_2[2], 
             float target_x, float target_y, float reference[2], float result[2]) {
 
  float L0 = separation / 2.0;

  if (abs(L0 + target_x) == 0 || abs(L0 - target_x) == 0) {
    return true;
  }

  if (center_2[0] <= reference[0] && reference[0] <= max_point[0] && min_point[1] <= reference[1] && reference[1] <= max_point[1]) {
    
    result[0] = degrees(atan(target_y / abs(L0 + target_x)));
    result[1] = degrees(atan(target_y / abs(L0 - target_x)));
    return false;
  }
  else if (center_1[0] <= reference[0] && reference[0] < center_2[0] && min_point[1] <= reference[1] && reference[1] <= max_point[1]) {
    
    result[0] = degrees(atan(target_y / abs(L0 + target_x)));
    result[1] = degrees(PI - atan(target_y / abs(L0 - target_x)));
    return false;
  }
  else if (min_point[0] <= reference[0] && reference[0] < center_1[0] && min_point[1] <= reference[1] && reference[1] <= max_point[1]) {
    
    result[0] = degrees(PI - atan(target_y / abs(L0 + target_x)));
    result[1] = degrees(PI - atan(target_y / abs(L0 - target_x)));
    return false;
  }

  return true;
}

void convert_angles(float angles_per_step, float angles[2]) {
 
  if (fmod(angles[0], angles_per_step) != 0.0) {
    angles[0] = round(angles[0] / angles_per_step) * angles_per_step;
  }

  if (fmod(angles[1], angles_per_step) != 0.0) {
    angles[1] = round(angles[1] / angles_per_step) * angles_per_step;
  }

}

bool inverse_kinematic(float size_whole_arm_array[2], float min_point[2], float max_point[2], 
                      float base_arm_1[2], float base_arm_2[2], float target[2], float reference[2], 
                      float distance_between_motors, float angles_per_step, float result[2]) {
 
  float omegas[2];
  bool error = get_omegas(size_whole_arm_array, distance_between_motors, target[0], target[1], omegas);
  if (error) return true;

  float betas[2];
  error = get_beta(distance_between_motors, max_point, min_point, base_arm_1, base_arm_2, target[0], target[1], reference, betas);
  if (error) return true;

  float theta_1 = betas[0] + omegas[0];
  float theta_2 = betas[1] - omegas[1];

  result[0] = theta_1;
  result[1] = theta_2;

  if (angles_per_step > 0.0) convert_angles(angles_per_step, result);

  return false;
}

bool get_base_point_upper_arm(float point_position_base_lower_arm[2], float size_lower_arm, 
                             float angle_lower_arm, float result[2]) {
 
  float extremo_x = point_position_base_lower_arm[0] + size_lower_arm * cos(radians(angle_lower_arm));
  float extremo_y = point_position_base_lower_arm[1] + size_lower_arm * sin(radians(angle_lower_arm));

  result[0] = extremo_x;
  result[1] = extremo_y;

  return false;
}

bool limitations(float min_point[2], float max_point[2], float point[2]) {
 
  if (point[1] < min_point[1] || point[1] > max_point[1] || 
      point[0] < min_point[0] || point[0] > max_point[0]) {
    return true;
  }

  return false;
}

bool kinematic(float base_arm[2][2], float size_whole_arm[2], float angles[2], float result[2]) {
 
  float center_1[2];
  bool error = get_base_point_upper_arm(base_arm[0], size_whole_arm[0], angles[0], center_1);
  if (error) {
    return true;
  }

  float center_2[2];
  error = get_base_point_upper_arm(base_arm[1], size_whole_arm[0], angles[1], center_2);
  if (error) {
    return true;
  }

  float centers_rotation[2][2] = {{center_1[0], center_1[1]}, {center_2[0], center_2[1]}};
  float intersection_result_x[2];
  float intersection_result_y[2];

  error = intersection_points(size_whole_arm[1], centers_rotation, intersection_result_x, intersection_result_y);
  if (error) {
    return true;
  }

  result[0] = intersection_result_x[1];
  result[1] = intersection_result_y[1];

  return false;
}

bool find_path(float size_whole_arm[2], float init_position[2], float fin_position[2], float min_point[2], 
              float max_point[2], float base_arm_1[2], float base_arm_2[2], float segment_x, float segment_y, 
              float distance_between_motors, float angles_per_step, float radius, 
              float path_x[], float path_y[], float reference_x[], float reference_y[], 
              int* path_length, int* reference_length) {
 
  *path_length = 0;
  *reference_length = 0;

  if (limitations(min_point, max_point, fin_position)) {
    return true;
  }

  float angles[2];
  bool error = inverse_kinematic(size_whole_arm, min_point, max_point, base_arm_1, base_arm_2, 
                                fin_position, fin_position, distance_between_motors, angles_per_step, angles);
  if (error) {
    return true;
  }

  float base_arm[2][2] = {{base_arm_1[0], base_arm_1[1]}, {base_arm_2[0], base_arm_2[1]}};
  float new_position_fin[2];
  error = kinematic(base_arm, size_whole_arm, angles, new_position_fin);
  if (error) {
    return true;
  }

  error = inverse_kinematic(size_whole_arm, min_point, max_point, base_arm_1, base_arm_2, 
                          init_position, init_position, distance_between_motors, angles_per_step, angles);
  if (error) {
    return true;
  }

  float new_position_init[2];
  error = kinematic(base_arm, size_whole_arm, angles, new_position_init);
  if (error) {
    return true;
  }

  while (get_distance_between_points(new_position_init, new_position_fin) > radius) {
    
    float init_x = init_position[0] - segment_x;
    float init_y = init_position[1] + segment_y;
    
    float distance = 99999.0;
    float new_pos_init_x = 0;
    float new_pos_init_y = 0;
    
    for (int i = 0; i < 3; i++) {
      for (int j = 0; j < 3; j++) {
        
        float pos_x = init_x + j * segment_x;
        float pos_y = init_y - i * segment_y;
        
        if (pos_x == init_position[0] && pos_y == init_position[1]) {
          continue;
        }
        
        float test_position[2] = {pos_x, pos_y};
        if (limitations(min_point, max_point, test_position)) {
          continue;
        }
        
        error = inverse_kinematic(size_whole_arm, min_point, max_point, base_arm_1, base_arm_2, 
                                test_position, test_position, distance_between_motors, angles_per_step, angles);
        if (error) {
          continue;
        }
        
        float new_position[2];
        error = kinematic(base_arm, size_whole_arm, angles, new_position);
        if (error) {
          continue;
        }
        
        float new_distance = get_distance_between_points(new_position_init, new_position) + 
                          get_distance_between_points(new_position, new_position_fin);
        
        if (new_distance < distance) {
          distance = new_distance;
          new_pos_init_x = pos_x;
          new_pos_init_y = pos_y;
          new_position_init[0] = new_position[0];
          new_position_init[1] = new_position[1];
        }
      }
    }
    
    init_position[0] = new_pos_init_x;
    init_position[1] = new_pos_init_y;
    
    reference_x[*reference_length] = init_position[0];
    reference_y[*reference_length] = init_position[1];
    (*reference_length)++;
    
    path_x[*path_length] = new_position_init[0];
    path_y[*path_length] = new_position_init[1];
    (*path_length)++;
  }

  if (*path_length > 0) {
    if (path_x[*path_length-1] != new_position_fin[0] || path_y[*path_length-1] != new_position_fin[1]) {
      reference_x[*reference_length] = init_position[0];
      reference_y[*reference_length] = init_position[1];
      (*reference_length)++;
      
      path_x[*path_length] = new_position_fin[0];
      path_y[*path_length] = new_position_fin[1];
      (*path_length)++;
    }
  }

  return false;
}

void create_change_position(float init_position[2], float size_segments[2], float size_whole_arm_array[2], 
                        float distance_between_motors, float max_point[2], float min_point[2], 
                        float base_arm_1[2], float base_arm_2[2], float angles_per_step, 
                        float new_entry_x, float new_entry_y, float duration) {

 float fin_position[2] = {new_entry_x, new_entry_y};
 float path_x[20];
 float path_y[20];
 float reference_x[20];
 float reference_y[20];
 int path_length, reference_length;

 bool error = find_path(size_whole_arm_array, init_position, fin_position, min_point, max_point, 
                     base_arm_1, base_arm_2, size_segments[0], size_segments[1], 
                     distance_between_motors, angles_per_step, min(size_segments[0], size_segments[1]),
                     path_x, path_y, reference_x, reference_y, &path_length, &reference_length);

 if (error || path_length == 0) {
   return;
 }

 float time_per_step = duration / path_length;
 unsigned long init_time = millis();
 int first = 0;

 while (first < path_length) {
   unsigned long current_time = millis();

   if (current_time - init_time >= time_per_step) {
     float path_point[2] = {path_x[first], path_y[first]};
     float reference_point[2] = {reference_x[first], reference_y[first]};
     
     float angles_init[2];
     error = inverse_kinematic(size_whole_arm_array, min_point, max_point, base_arm_1, base_arm_2, 
                               path_point, reference_point, distance_between_motors, angles_per_step, angles_init);
     
     if (!error) {
       // Calcular posición objetivo en steps (desde posición cero)
       long target_steps_1 = round(angles_init[0] / angles_per_step);
       long target_steps_2 = round(angles_init[1] / angles_per_step);
       
       // Calcular cuántos steps faltan desde la posición actual
       long steps_to_move_1 = target_steps_1 - motor_1.currentPosition();
       long steps_to_move_2 = target_steps_2 - motor_2.currentPosition();
       
       // Mover relativamente desde la posición actual
       motor_1.move(steps_to_move_1);
       motor_2.move(steps_to_move_2);
       
       // Ejecutar movimiento hasta completar
       while (motor_1.distanceToGo() != 0 || motor_2.distanceToGo() != 0) {
         motor_1.run();
         motor_2.run();
       }
       
       Serial.print("Target steps: ");
       Serial.print(target_steps_1);
       Serial.print(" ");
       Serial.println(target_steps_2);
     }
     
     init_time = current_time;
     first++;
   }
 }
}

void setup(){

    Serial.begin(9600);
    Serial.println("Ready");

    motor_1.setMaxSpeed(1000);
    motor_1.setAcceleration(500);
    motor_2.setMaxSpeed(1000);
    motor_2.setAcceleration(500);

    angles_per_step = 1.8;
    total_duration_ms = 6000;

    size_lower_arm = 76.34;
    size_upper_arm = 94.66;

    size_whole_arm[0] = size_lower_arm;
    size_whole_arm[1] = size_upper_arm;

    base_arm_1[0] = -20.5;
    base_arm_1[1] = 0.0;
    base_arm_2[0] = 20.5;
    base_arm_2[1] = 0.0;

    distance_between_motors = get_distance_between_points(base_arm_1, base_arm_2);

    init_position[0] = 0.0;
    init_position[1] = height_of_the_base + 3.0;

    min_point_y = init_position[1];

    float centers[2][2] = { { base_arm_1[0], base_arm_1[1] }, { base_arm_2[0], base_arm_2[1] } };

    error = intersection_points(size_whole_arm[0] + size_whole_arm[1], centers, result_1, result_2);
    if (error) return;

    max_point_y = result_2[1];

    error = find_x_max(size_whole_arm[0] + size_whole_arm[1], 0.0, base_arm_1, result_1);
    if (error) return;

    max_point_x = result_1[0];

    min_point_x = -max_point_x;

    min_point[0] = min_point_x;
    min_point[1] = min_point_y;
    max_point[0] = max_point_x;
    max_point[1] = max_point_y;

    result_1[0] = min_point[0];
    result_1[1] = max_point[1];

    result_2[0] = max_point[0];
    result_2[1] = min_point[1];

    float distance_height = get_distance_between_points(min_point, result_1);
    float distance_width = get_distance_between_points(min_point, result_2);

    num_large_h = largest_divisor(distance_height);
    num_large_w = largest_divisor(distance_width);

    if(simple_or_each){
    error = gcd(distance_height, distance_width, result_3);
    float new_num_large_h = result_3;
    float new_num_large_w = new_num_large_h;
    if (error) {
        num_large_h = num_large_h;
        num_large_w = num_large_w;
    }
    else{
        num_large_h = new_num_large_h;
        num_large_w = new_num_large_w;
    }
    }

    size_segments[0] = num_large_w;
    size_segments[1] = num_large_h;

    // Calcular ángulos iniciales y mover motores a posición inicial
    float angles_init[2];
    error = inverse_kinematic(size_whole_arm, min_point, max_point, base_arm_1, base_arm_2, 
                            init_position, init_position, distance_between_motors, angles_per_step, angles_init);

    if (!error) {
    // Calcular steps para la posición inicial
    long initial_steps_1 = round(angles_init[0] / angles_per_step);
    long initial_steps_2 = round(angles_init[1] / angles_per_step);

    Serial.println("Moving to initial position...");

    // Mover a la posición inicial (desde step 0)
    motor_1.moveTo(initial_steps_1);
    motor_2.moveTo(initial_steps_2);

    // Ejecutar movimiento hasta completar
    while (motor_1.distanceToGo() != 0 || motor_2.distanceToGo() != 0) {
        motor_1.run();
        motor_2.run();
    }

    Serial.print("Motors moved to initial position - Motor 1: ");
    Serial.print(initial_steps_1);
    Serial.print(" steps, Motor 2: ");
    Serial.print(initial_steps_2);
    Serial.println(" steps");
    } else {
    Serial.println("Error calculating initial angles");
    }

    Serial.println("Setup complete");
}

void loop(){
 if (Serial.available()) {
   delay(100);
   
   float x = Serial.parseFloat();
   float y = Serial.parseFloat();
   
   Serial.print("Recibido X: ");
   Serial.print(x);
   Serial.print(" Y: ");
   Serial.println(y);
   
   // Llamar create_change_position para mover los motores
   create_change_position(init_position, size_segments, size_whole_arm, 
                         distance_between_motors, max_point, min_point, 
                         base_arm_1, base_arm_2, angles_per_step, 
                         x, y, total_duration_ms);
   
   Serial.println("Movimiento completado");
   
   while (Serial.available()) {
     Serial.read();
   }
 }
}