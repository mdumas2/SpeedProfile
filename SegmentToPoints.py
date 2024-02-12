import json
import numpy as np
import matplotlib.pyplot as plt

NUM_OF_POINTS = 50

class SegmentToPoints:
    def __init__(self):
        self._segment_points = []
        self._track_x = []
        self._track_y = []
        self._result_filename = 'Segment_to_Points'

    def _generate_line(self, start_point, end_point, num_points=NUM_OF_POINTS):
        x_values = np.linspace(start_point[0], end_point[0], num_points).tolist()
        y_values = np.linspace(start_point[1], end_point[1], num_points).tolist()
        return x_values, y_values

    def _generate_curve(self, start_point, end_point, radius, center_point, num_points=NUM_OF_POINTS):
        x_start_point, y_start_point = start_point
        x_end_point, y_end_point = end_point
        center_x , center_y = center_point
        start_angle = np.arctan2(y_start_point-center_y, x_start_point-center_x)
        end_angle = np.arctan2(y_end_point-center_y, x_end_point-center_x)
        if end_angle < start_angle:
            end_angle += 2 * np.pi
        angles = np.linspace(start_angle, end_angle, num_points)
        x_curve = (center_x + radius * np.cos(angles)).tolist()
        y_curve = (center_y + radius * np.sin(angles)).tolist()
        return x_curve, y_curve

    def _plot_points(self, x_points, y_points):
        plt.figure(figsize=(10, 5))
        plt.plot(x_points, y_points, 'ro--')
        plt.title('Segment')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        plt.show()

    def _save_points(self, x_points, y_points, filename):
        with open(filename + '.tsv', 'w') as f:
            f.write('X\tY\n')
            for x, y in zip(x_points, y_points):
                f.write(f'{x}\t{y}\n')
        print(f'Points saved to {filename}.tsv')

    def generate_points_of_track(self, track_file, plot=False, save=False, result_filename=None):
        track_data = None
        with open(track_file, 'r') as file:
            track_data = json.load(file)
        for segment in track_data:
            if segment["is_curve"]:
                x_points, y_points = self._generate_curve(segment["start_point"], segment["end_point"], segment["radius"], segment["center_point"])
            else:
                x_points, y_points = self._generate_line(segment["start_point"], segment["end_point"])
            self._segment_points.append((x_points, y_points))

        for segment in self._segment_points:
            x_points, y_points = segment
            self._track_x.extend(x_points)
            self._track_y.extend(y_points)

        if plot:
            self._plot_points(self._track_x, self._track_y)
        if save:
            if result_filename:
                self._result_filename = result_filename
            self._save_points(self._track_x, self._track_y, self._result_filename)


segment_to_points = SegmentToPoints()
segment_to_points.generate_points_of_track(r'C:\Users\mateu\Documents\GitHub\SpeedProfile\Track.json', plot=True, save=True, result_filename='Segment_to_Points')
