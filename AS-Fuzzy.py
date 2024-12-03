import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# تعریف متغیرهای ورودی و خروجی برای مرحله اول (تشخیص فعالیت)
x_accel = ctrl.Antecedent(np.arange(0, 1.6, 0.1), 'X_Acceleration')
z_accel = ctrl.Antecedent(np.arange(0, 1.6, 0.1), 'Z_Acceleration')
activity = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'Activity')

# توابع عضویت برای شتاب‌سنج
x_accel['low'] = fuzz.trimf(x_accel.universe, [0, 0, 0.3])
x_accel['medium'] = fuzz.trimf(x_accel.universe, [0.2, 0.5, 0.8])
x_accel['high'] = fuzz.trimf(x_accel.universe, [0.7, 1.2, 1.5])

z_accel['low'] = fuzz.trimf(z_accel.universe, [0, 0, 0.3])
z_accel['medium'] = fuzz.trimf(z_accel.universe, [0.2, 0.5, 0.8])
z_accel['high'] = fuzz.trimf(z_accel.universe, [0.7, 1.2, 1.5])

# توابع عضویت برای خروجی فعالیت
activity['resting'] = fuzz.trimf(activity.universe, [0, 0, 0.3])
activity['walking'] = fuzz.trimf(activity.universe, [0.2, 0.5, 0.8])
activity['running'] = fuzz.trimf(activity.universe, [0.7, 1, 1])

# تعریف قوانین فازی برای مرحله اول
rule1 = ctrl.Rule(x_accel['low'] & z_accel['low'], activity['resting'])
rule2 = ctrl.Rule(x_accel['medium'] & z_accel['medium'], activity['walking'])
rule3 = ctrl.Rule(x_accel['high'] & z_accel['high'], activity['running'])

# ایجاد سیستم کنترل فازی برای مرحله اول
activity_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
activity_sim = ctrl.ControlSystemSimulation(activity_ctrl)

# دریافت ورودی‌های شتاب‌سنج از کاربر
x_input = float(input("Enter X-axis Acceleration (0 to 1.5): "))
z_input = float(input("Enter Z-axis Acceleration (0 to 1.5): "))

# بررسی محدوده ورودی‌ها
if not (0 <= x_input <= 1.5) or not (0 <= z_input <= 1.5):
    print("Error: Input values are out of range. Please enter values between 0 and 1.5.")
else:
    # محاسبه مرحله اول
    activity_sim.input['X_Acceleration'] = x_input
    activity_sim.input['Z_Acceleration'] = z_input
    activity_sim.compute()
    activity_level = activity_sim.output['Activity']
    print(f"Detected Activity Level: {activity_level}")


# تعریف متغیرهای ورودی و خروجی برای مرحله دوم (پایش سلامت)
heart_rate = ctrl.Antecedent(np.arange(50, 201, 10), 'HeartRate')
health_status = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'HealthStatus')

# توابع عضویت برای ضربان قلب
heart_rate['low'] = fuzz.trimf(heart_rate.universe, [50, 60, 70])
heart_rate['normal'] = fuzz.trimf(heart_rate.universe, [60, 100, 140])
heart_rate['high'] = fuzz.trimf(heart_rate.universe, [120, 160, 200])

# توابع عضویت برای خروجی سلامت
health_status['warning'] = fuzz.trimf(health_status.universe, [0, 0, 0.5])
health_status['normal'] = fuzz.trimf(health_status.universe, [0.5, 1, 1])

# قوانین فازی برای مرحله دوم
rule4 = ctrl.Rule(heart_rate['low'], health_status['normal'])
rule5 = ctrl.Rule(heart_rate['normal'], health_status['normal'])
rule6 = ctrl.Rule(heart_rate['high'], health_status['warning'])

# ایجاد سیستم کنترل فازی برای مرحله دوم
health_ctrl = ctrl.ControlSystem([rule4, rule5, rule6])
health_sim = ctrl.ControlSystemSimulation(health_ctrl)

# دریافت ورودی ضربان قلب از کاربر
heart_rate_input = float(input("Enter Heart Rate (50 to 200): "))

# محاسبه مرحله دوم
health_sim.input['HeartRate'] = heart_rate_input
health_sim.compute()
health_output = health_sim.output['HealthStatus']
print(f"Health Status: {health_output}")

# تجسم توابع عضویت برای شتاب و ضربان قلب
x_accel.view()
z_accel.view()
heart_rate.view()
health_status.view()
plt.show()
