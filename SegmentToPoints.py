import numpy as np
import matplotlib.pyplot as plt

NUM_OF_POINTS = 50

def generate_line(start_point, end_point, num_points=NUM_OF_POINTS):
    x_values = np.linspace(start_point[0], end_point[0], num_points).tolist()
    y_values = np.linspace(start_point[1], end_point[1], num_points).tolist()
    return x_values, y_values

def generate_curve(start_point, end_point, radius, center_point, num_points=NUM_OF_POINTS):
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

def plot_points(x_points, y_points):
    plt.figure(figsize=(10, 5))
    plt.plot(x_points, y_points, 'ro--')
    plt.title('Segment')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()

def save_points(x_points, y_points, filename):
    with open(filename + '.tsv', 'w') as f:
        f.write('X\tY\n')
        for x, y in zip(x_points, y_points):
            f.write(f'{x}\t{y}\n')
    print(f'Points saved to {filename}.tsv')

track = [
            {"start_point": (0, 0), "end_point": (50, 0), "is_curve": False},
            {"start_point": (50, 0), "end_point": (75, 25), "is_curve": True, "radius": 25, "center_point": (50, 25)},

            {"start_point": (75, 25), "end_point": (75, 75), "is_curve": False},
            {"start_point": (75, 75), "end_point": (50, 100), "is_curve": True, "radius": 25, "center_point": (50, 75)},

            {"start_point": (50, 100), "end_point": (0, 100), "is_curve": False},
            {"start_point": (0, 100), "end_point": (-50, 100), "is_curve": False},

            {"start_point": (-50, 100), "end_point": (-75, 75), "is_curve": True, "radius": 25, "center_point": (-50, 75)},
            {"start_point": (-75, 75), "end_point": (-75, 25), "is_curve": False},

            {"start_point": (-75, 25), "end_point": (-50, 0), "is_curve": True, "radius": 25, "center_point": (-50, 25)},
            {"start_point": (-50, 0), "end_point": (0, 0), "is_curve": False}
        ]

segment_points = []

for segment in track:
    if segment["is_curve"]:
        x_points, y_points = generate_curve(segment["start_point"], segment["end_point"], segment["radius"], segment["center_point"])
    else:
        x_points, y_points = generate_line(segment["start_point"], segment["end_point"])
    segment_points.append((x_points, y_points))

track_x = []
track_y = []
for segment in segment_points:
    x_points, y_points = segment
    track_x.extend(x_points)
    track_y.extend(y_points)

plot_points(track_x, track_y)
save_points(track_x, track_y, 'Segment_to_Points')
