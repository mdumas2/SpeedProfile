from SegmentToPoints import SegmentToPoints
import os

current_folder = os.path.dirname(__file__)
json_file_path = os.path.join(current_folder, "Track.json")
def main():
    segment_to_points = SegmentToPoints()
    segment_to_points.generate_points_from_track(json_file_path, plot=True, save=True, result_filename='Segment_to_Points')

if __name__ == "__main__":
    main()