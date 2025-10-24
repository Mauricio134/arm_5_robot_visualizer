#include "pwm.h"  // API Renesas pour PWM sur R4

const byte pinA = 2;
const byte pinB = 3;

// Pines L298N
const byte IN1 = 8;
const byte IN2 = 9;
const byte ENA = 10;

const byte pinC = 11;
const byte pinD = 12;

// Pines L298N
const byte IN3 = 6;
const byte IN4 = 7;
const byte ENB = 5;

// déclarer deux instances, pour deux broches
PwmOut pwmENA(ENA);
PwmOut pwmENB(ENB);


const float cpr = 12;
const float radius = 100.37;
const float factor = 1;
const float pulses_per_turn = cpr * radius * factor;

const float torque_max = 1.3 * 0.0981;
const float RPM = 330.0f;

bool direction_1 = false;
bool direction_2 = false;
bool entering_1, entering_2;

volatile long initial_position_1 = 0;
volatile long initial_position_2 = 0;

float total_time = 1.0f;
float temp_resolution = 0.01f;

long final_position_1;
long delta_position_1;
long final_position_2;
long delta_position_2;

float velocity_peak_1;
float velocity_peak_2;

float time_acc_1;
float time_acc_2;

float aceleration_max_1;
float aceleration_max_2;

volatile uint8_t lastEncoded1 = 0;
volatile uint8_t lastEncoded2 = 0;

float position_wished_1;
float position_wished_2;

float Kp = 0.75;
float Ki = 3.0;
float Kd = 0.01;

float error;

float result_1[2];
float result_2[2];
float result_3;

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




void update_counter_1() {
  uint8_t MSB = digitalRead(pinA);  // canal A
  uint8_t LSB = digitalRead(pinB);  // canal B
  uint8_t encoded = (MSB << 1) | LSB;
  uint8_t sum = (lastEncoded1 << 2) | encoded;

  // invertir la convención para que antihorario = positivo
  if (sum == 0b0001 || sum == 0b0111 || sum == 0b1110 || sum == 0b1000) initial_position_1++;
  if (sum == 0b0010 || sum == 0b0100 || sum == 0b1101 || sum == 0b1011) initial_position_1--;

  lastEncoded1 = encoded;
}

void update_counter_2() {
  uint8_t MSB = digitalRead(pinC);  // canal A
  uint8_t LSB = digitalRead(pinD);  // canal B
  uint8_t encoded = (MSB << 1) | LSB;
  uint8_t sum = (lastEncoded2 << 2) | encoded;

  // igual para motor 2
  if (sum == 0b0001 || sum == 0b0111 || sum == 0b1110 || sum == 0b1000) initial_position_2--;
  if (sum == 0b0010 || sum == 0b0100 || sum == 0b1101 || sum == 0b1011) initial_position_2++;

  lastEncoded2 = encoded;
}

float get_distance_between_points(float* init, float* fin) {
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

    return false;  // Intersection found
  } else {
    return true;  // No intersection
  }
}

bool find_x_max(float radius, float position_y, float* padding_k_h, float* result) {

  float sqrt_entry = pow(radius, 2) - pow(position_y - padding_k_h[0], 2);

  if (sqrt_entry < 0.0) {
    return true;
  }

  float valor = sqrt(sqrt_entry);

  result[0] = valor + padding_k_h[1];
  result[1] = -valor + padding_k_h[0];

  return false;
}

float largest_divisor(float n) {
  float result = sqrt(n);
  float i = int(result);

  while (i >= 1) {
    if (fmod(n, i) == 0.0) return i;
    i--;
  }

  return result;
}

bool gcd(float a, float b, float& result) {
  float n = min(round(a), round(b));

  while (n > 0.0) {
    if (fmod(a, n) == 0.0 && fmod(b, n) == 0.0) {
      result = n;
      return false;
    }
    n--;
  }
  result = 0.0;
  return true;
}

bool get_omegas(float arms_size[2], float separation, float target_x, float target_y, float* result) {

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
              float target_x, float target_y, float result[2]) {

  float L0 = separation / 2.0;

  if (abs(L0 + target_x) == 0 || abs(L0 - target_x) == 0) {
    return true;
  }

  if (center_2[0] <= target_x && target_x <= max_point[0] && min_point[1] <= target_y && target_y <= max_point[1]) {

    result[0] = degrees(atan(target_y / abs(L0 + target_x)));
    result[1] = degrees(atan(target_y / abs(L0 - target_x)));
    return false;
  } else if (center_1[0] <= target_x && target_x < center_2[0] && min_point[1] <= target_y && target_y <= max_point[1]) {

    result[0] = degrees(atan(target_y / abs(L0 + target_x)));
    result[1] = degrees(PI - atan(target_y / abs(L0 - target_x)));
    return false;
  } else if (min_point[0] <= target_x && target_x < center_1[0] && min_point[1] <= target_y && target_y <= max_point[1]) {

    result[0] = degrees(PI - atan(target_y / abs(L0 + target_x)));
    result[1] = degrees(PI - atan(target_y / abs(L0 - target_x)));
    return false;
  }

  return true;
}

bool inverse_kinematic(float size_whole_arm_array[2], float min_point[2], float max_point[2],
                       float base_arm_1[2], float base_arm_2[2], float target[2],
                       float distance_between_motors, float result[2]) {

  float omegas[2];
  bool error = get_omegas(size_whole_arm_array, distance_between_motors, target[0], target[1], omegas);
  if (error) return true;

  float betas[2];
  error = get_beta(distance_between_motors, max_point, min_point, base_arm_1, base_arm_2, target[0], target[1], betas);
  if (error) return true;

  float theta_1 = betas[0] + omegas[0];
  float theta_2 = betas[1] - omegas[1];

  result[0] = theta_1;
  result[1] = theta_2;

  return false;
}

void movement_motors(float angle1, float angle2) {

  Serial.print("Angle of Destination: ");
  Serial.print(angle1);
  Serial.print(" ");
  Serial.println(angle2);

  final_position_1 = round(angle1 / 360.0f * pulses_per_turn);
  final_position_2 = round(angle2 / 360.0f * pulses_per_turn);

  Serial.print("Pulses of Destination: ");
  Serial.print(final_position_1);
  Serial.print(" ");
  Serial.println(final_position_2);

  float total_distance_1 = final_position_1 - initial_position_1;
  float total_distance_2 = final_position_2 - initial_position_2;

  delta_position_1 = abs(total_distance_1);
  delta_position_2 = abs(total_distance_2);

  Serial.print("Complete path: ");
  Serial.print(delta_position_1);
  Serial.print(" ");
  Serial.println(delta_position_2);

  velocity_peak_1 = 2.0f * delta_position_1 / total_time;
  velocity_peak_2 = 2.0f * delta_position_2 / total_time;

  Serial.print("Max Velocity: ");
  Serial.print(velocity_peak_1);
  Serial.print(" ");
  Serial.println(velocity_peak_2);

  aceleration_max_1 = 4.0f * delta_position_1 / pow(total_time, 2);
  aceleration_max_2 = 4.0f * delta_position_2 / pow(total_time, 2);

  Serial.print("Max Aceleration: ");
  Serial.print(aceleration_max_1);
  Serial.print(" ");
  Serial.println(aceleration_max_2);

  time_acc_1 = velocity_peak_1 / aceleration_max_1;
  time_acc_2 = velocity_peak_2 / aceleration_max_2;

  Serial.print("Time Acceleration: ");
  Serial.print(time_acc_1);
  Serial.print(" ");
  Serial.println(time_acc_2);

  float t = 0.0f;

  float sign_1 = (final_position_1 - initial_position_1 >= 0) ? 1.0f : -1.0f;
  float sign_2 = (final_position_2 - initial_position_2 >= 0) ? 1.0f : -1.0f;

  long pos_initial_1 = initial_position_1;
  long pos_initial_2 = initial_position_2;

  float integral_1 = 0;
  float integral_2 = 0;

  float error_prev_1 = 0;
  float error_prev_2 = 0;

  while (t <= total_time) {
    // Motor 1
    if (t < time_acc_1) {
      position_wished_1 = pos_initial_1 + sign_1 * 0.5f * aceleration_max_1 * pow(t, 2);
    } else {
      position_wished_1 = final_position_1 - sign_1 * 0.5f * aceleration_max_1 * pow((total_time - t), 2);
    }

    // Motor 2
    if (t < time_acc_2) {
      position_wished_2 = pos_initial_2 + sign_2 * 0.5f * aceleration_max_2 * pow(t, 2);
    } else {
      position_wished_2 = final_position_2 - sign_2 * 0.5f * aceleration_max_2 * pow((total_time - t), 2);
    }

    float error_1 = position_wished_1 - initial_position_1;
    float error_2 = position_wished_2 - initial_position_2;

    integral_1 += error_1 * temp_resolution;
    integral_2 += error_2 * temp_resolution;

    float derivative_1 = (error_1 - error_prev_1) / temp_resolution;
    float derivative_2 = (error_2 - error_prev_2) / temp_resolution;

    float output_1 = Kp * error_1 + Ki * integral_1 + Kd * derivative_1;
    float output_2 = Kp * error_2 + Ki * integral_2 + Kd * derivative_2;

    error_prev_1 = error_1;
    error_prev_2 = error_2;

    output_1 = constrain(abs(output_1), 0, 255);
    output_2 = constrain(abs(output_2), 0, 255);

    // dirección
    if (error_1 >= 0) {
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
    } else {
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
    }

    if (error_2 >= 0) {
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
    } else {
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
    }

    //analogWrite(ENA, output_1);
    pwmENA.pulse_perc((((float)output_1)/255.0) * 100.0f);
    //analogWrite(ENB, output_2);
    pwmENB.pulse_perc((((float)output_2)/255.0) * 100.0f);

    Serial.print("Positions Wished: ");
    Serial.print(position_wished_1);
    Serial.print(" ");
    Serial.println(position_wished_2);
    Serial.print("Pulses positions: ");
    Serial.print(initial_position_1);
    Serial.print(" ");
    Serial.println(initial_position_2);

    t += temp_resolution;
    delay(temp_resolution * 1000.0f);
  }

  Serial.print("FINAL POSITIONS: ");
  Serial.print(initial_position_1);
  Serial.print(" ");
  Serial.println(initial_position_2);

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void setup() {
  Serial.begin(9600);

  pinMode(pinA, INPUT_PULLUP);
  pinMode(pinB, INPUT_PULLUP);

  pinMode(pinC, INPUT_PULLUP);
  pinMode(pinD, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(pinA), update_counter_1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(pinB), update_counter_1, CHANGE);

  attachInterrupt(digitalPinToInterrupt(pinC), update_counter_2, CHANGE);
  attachInterrupt(digitalPinToInterrupt(pinD), update_counter_2, CHANGE);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);

  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);

  // Initialiser avec fréquence 20000 Hz, rapport cyclique 50 %
  pwmENA.begin(20000.0f, 0.5f);    // fréquence 5000 Hz, duty à 50%
  pwmENB.begin(20000.0f, 0.5f);

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  //analogWrite(ENA, 0);
   pwmENA.pulse_perc(0 * 100.0f);     // duty cycle en pourcentage

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  //  analogWrite(ENB, 0);
  pwmENB.pulse_perc(0 * 100.0f);
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

  if (simple_or_each) {
    error = gcd(distance_height, distance_width, result_3);
    float new_num_large_h = result_3;
    float new_num_large_w = new_num_large_h;
    if (error) {
      num_large_h = num_large_h;
      num_large_w = num_large_w;
    } else {
      num_large_h = new_num_large_h;
      num_large_w = new_num_large_w;
    }
  }

  size_segments[0] = num_large_w;
  size_segments[1] = num_large_h;

  float angles_init[2];
  error = inverse_kinematic(size_whole_arm, min_point, max_point, base_arm_1, base_arm_2, init_position, distance_between_motors, angles_init);

  movement_motors(angles_init[0], angles_init[1]);
}

void loop() {
  if (Serial.available()) {

    float position_x = Serial.parseFloat();
    Serial.readStringUntil(' ');
    float position_y = Serial.parseFloat();
    Serial.readStringUntil('\n');

    if (position_y == 0.0f) {
      final_position_1 = 545;
      final_position_2 = 58;
    } else {
      float target[2];
      target[0] = position_x;
      target[1] = position_y;
      float angles_init[2];
      error = inverse_kinematic(size_whole_arm, min_point, max_point, base_arm_1, base_arm_2, target, distance_between_motors, angles_init);

      movement_motors(angles_init[0], angles_init[1]);
    }
  }
}