import matplotlib.pyplot as plt
import json

MAX_ACCELERATION = 15.0
MAX_SPEED = 7.0
TIME_STEP = 0.01

class SpeedProfile:
    def __init__(self):
        self._segment_speed_profiles = []

    def _calculate_end_speed(self, index, segment_data):
        index = index + 1
        if index < len(segment_data):
            segment = segment_data[index]
            if segment["type"] == 'straight':
                segment_end_speed = (2 * MAX_ACCELERATION * (segment['length']/10)) ** 0.5
            else:
                segment_end_speed = (MAX_ACCELERATION * (segment['radius']/100)) ** 0.5
            if segment_end_speed > MAX_SPEED:
                segment_end_speed = MAX_SPEED
        else:
            segment_end_speed = 0
        return segment_end_speed

    def _calculate_top_speed_straight(self, length):
        segment_top_speed = (2 * MAX_ACCELERATION * length) ** 0.5
        if segment_top_speed > MAX_SPEED:
            segment_top_speed = MAX_SPEED
        return segment_top_speed

    def _calculate_top_speed_curve(self, radius):
        segment_top_speed = (MAX_ACCELERATION * radius) ** 0.5
        if segment_top_speed > MAX_SPEED:
            segment_top_speed = MAX_SPEED
        return segment_top_speed

    def _generate_trapezoidal_velocity_profile(self, segment_initial_speed, segment_end_speed, segment_top_speed, segment_length, max_acceleration, max_deceleration, time_step=TIME_STEP):
        time_values = []
        velocity_values = []

        acceleration_time = (segment_top_speed - segment_initial_speed) / max_acceleration
        acceleration_distance = 0.5 * max_acceleration * (acceleration_time ** 2)
        if acceleration_distance < segment_length / 2:
            acceleration_distance = segment_length / 2
            acceleration_time = (2 * acceleration_distance / max_acceleration) ** 0.5

        deceleration_time = (segment_top_speed - segment_end_speed) / max_deceleration
        deceleration_distance = 0.5 * max_deceleration * (deceleration_time ** 2)
        if deceleration_distance < segment_length / 2:
            deceleration_distance = segment_length / 2
            deceleration_time = (2 * deceleration_distance / max_deceleration) ** 0.5

        total_time = acceleration_time + ((segment_length - acceleration_distance - deceleration_distance) / segment_top_speed) + deceleration_time

        current_time = 0
        current_distance = 0
        current_speed = segment_initial_speed

        while current_time <= total_time:
            time_values.append(current_time)
            velocity_values.append(current_speed)

            if current_distance < acceleration_distance:
                current_speed = min(current_speed + max_acceleration * time_step, segment_top_speed)
            elif current_distance < segment_length - deceleration_distance:
                current_speed = segment_top_speed
            else:
                current_speed = max(current_speed - max_deceleration * time_step, segment_end_speed)

            current_distance += current_speed * time_step
            current_time += time_step

        return time_values, velocity_values
    
    def generate_track_speed_profile_from_segments(self, segment_file, plot=False):
        segment_data = None
        segment_initial_speed = 0
        segment_end_speed = 0
        segment_top_speed = 0
        with open(segment_file, 'r') as file:
            segment_data = json.load(file)
        for index, segment in enumerate(segment_data):
            time_values = []
            velocity_values = []
            if segment["type"] == "straight":
                segment_end_speed = self._calculate_end_speed(index, segment_data)
                segment_top_speed = self._calculate_top_speed_straight(segment['length']/10)
                time_values, velocity_values = self._generate_trapezoidal_velocity_profile(segment_initial_speed, segment_end_speed, segment_top_speed, segment['length']/10, MAX_ACCELERATION, MAX_ACCELERATION)
            elif segment["type"] == "curve":
                segment_end_speed = self._calculate_end_speed(index, segment_data)
                segment_top_speed = self._calculate_top_speed_curve(segment['radius']/100)
                if segment_end_speed > segment_top_speed:
                    segment_end_speed = segment_top_speed
                time_values, velocity_values = self._generate_trapezoidal_velocity_profile(segment_initial_speed, segment_end_speed, segment_top_speed, segment['arc_length']/100, MAX_ACCELERATION, MAX_ACCELERATION)
            segment_initial_speed = segment_end_speed
            self._segment_speed_profiles.append((time_values, velocity_values))

        all_time_values = []
        all_velocity_values = []
        current_time = 0
        for time_values, velocity_values in self._segment_speed_profiles:
            for time in time_values:
                all_time_values.append(current_time)
                current_time += TIME_STEP
            all_velocity_values.extend(velocity_values)

        if plot:
            plt.figure()
            plt.plot(all_time_values, all_velocity_values)
            plt.xlabel("Time (s)")
            plt.ylabel("Velocity (m/s)")
            plt.title("Track Speed Profile")
            plt.grid(True)
            plt.show()
