import csv
import matplotlib.pyplot as plt
import json
import os
import math

class PointsToSegment:
    def __init__(self, robot_width=12):
        self._segments = []
        self._file_points = []
        self.robot_width = robot_width  # Convert cm to meters

    def _calculate_distance(self, point_1, point_2):
        x_1, y_1 = point_1
        x_2, y_2 = point_2
        return ((x_2 - x_1)**2 + (y_2 - y_1)**2) ** 0.5

    def _calculate_radius(self, segment):
        x1, y1 = segment[0]
        x2, y2 = segment[len(segment)//2]
        x3, y3 = segment[-1]

        a = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        b = ((x3 - x2) ** 2 + (y3 - y2) ** 2) ** 0.5
        c = ((x3 - x1) ** 2 + (y3 - y1) ** 2) ** 0.5

        s = (a + b + c) / 2  # semi-perimeter
        area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
        radius = a * b * c / (4 * area)

        return float(round(radius, 2))

    def _extract_segments_from_file_points(self, file_points):
        with open(file_points, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter='\t')
            next(csv_reader)
            for row in csv_reader:
                x, y = map(float, row)
                self._file_points.append((x, y))

        single_segment = []
        old_curvature = 0
        for index in range(1, len(self._file_points)):
            x1, y1 = self._file_points[index - 1]
            x2, y2 = self._file_points[index]
            dx = x2 - x1
            dy = y2 - y1
            ds = (dx**2 + dy**2) ** 0.5
            new_curvature = 0
            if dx != 0 and ds != 0:
                new_curvature = abs(dy / dx) / ds
            else:
                new_curvature = 0
            single_segment.append((x1, y1))
            if (new_curvature != old_curvature) and (new_curvature == 0 or old_curvature == 0):
                self._segments.append(single_segment)
                single_segment = []
                old_curvature = new_curvature
        single_segment.append(self._file_points[-1])
        self._segments.append(single_segment)

    def _generate_segment_json(self, plot=False, save=False, result_filename=None):
        result = []
        optimized_segments = []
        
        for segment in self._segments:
            curvatures = []
            length = 0
            for index in range(1, len(segment)):
                x1, y1 = segment[index-1]
                x2, y2 = segment[index]
                dx = x2 - x1
                dy = y2 - y1
                ds = (dx**2 + dy**2) ** 0.5
                length += ds
                curvature = 0
                if dx != 0 and ds != 0:
                    curvature = abs(dy / dx) / ds
                else:
                    curvature = 0
                curvatures.append(curvature)

            if all(curvature == 0 for curvature in curvatures):
                segment_info = {
                    "type": "straight",
                    "length": length
                }
            else:
                radius = self._calculate_radius(segment)
                arc_length = sum(self._calculate_distance(segment[i], segment[i+1]) for i in range(len(segment)-1))
                segment_info = {
                    "type": "curve",
                    "radius": radius,
                    "arc_length": arc_length
                }

            optimized_segment = self._adjust_segment_for_robot(segment)
            optimized_segments.append(optimized_segment)

            if save:
                result.append(segment_info)
                
            if plot:
                xs, ys = zip(*segment)
                plt.plot(xs, ys, marker='o', linestyle='-', label='Original Path', color='blue')
        
        if plot:
            # Plot the optimized path
            for optimized_segment in optimized_segments:
                xs, ys = zip(*optimized_segment)
                plt.plot(xs, ys, marker='o', linestyle='--', label='Optimized Path', color='red')
            
            plt.title('Original vs Optimized Path')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.grid(True)
            plt.legend()
            plt.show()
            
        if save:
            file_name = result_filename + '.json'
            file_path = os.path.abspath(file_name)
            with open(file_path, 'w') as json_file:
                json.dump(result, json_file, indent=4)
        return file_path

    def _adjust_segment_for_robot(self, segment):
        """ Adjust the segment for the robot's optimization by moving points inward in curves. """
        adjusted_segment = []
        for index, (x, y) in enumerate(segment):
            if index == 0 or index == len(segment) - 1:
                # No need to adjust the first or last point
                adjusted_segment.append((x, y))
            else:
                # Adjust points inward for curves
                prev_point = segment[index - 1]
                next_point = segment[index + 1]
                
                # Calculate direction vectors
                dx1 = x - prev_point[0]
                dy1 = y - prev_point[1]
                dx2 = next_point[0] - x
                dy2 = next_point[1] - y

                # Calculate average direction vector
                dx_avg = (dx1 + dx2) / 2
                dy_avg = (dy1 + dy2) / 2
                magnitude = math.sqrt(dx_avg**2 + dy_avg**2)

                # Normalize the vector and scale by the robot's width
                if magnitude != 0:
                    dx_norm = dx_avg / magnitude
                    dy_norm = dy_avg / magnitude
                    adjusted_x = x - self.robot_width * dy_norm  # Move perpendicular to the direction
                    adjusted_y = y + self.robot_width * dx_norm
                else:
                    adjusted_x, adjusted_y = x, y

                adjusted_segment.append((adjusted_x, adjusted_y))
        return adjusted_segment

    def generate_segments_from_points(self, points_file, plot=False, save=False, result_filename=None):
        self._extract_segments_from_file_points(points_file)
        file_path = self._generate_segment_json(plot, save, result_filename)
        return file_path
