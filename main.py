from SegmentToPoints import SegmentToPoints
from PointsToSegment import PointsToSegment
from SpeedProfile import SpeedProfile
import os

current_folder = os.path.dirname(__file__)
track_file_path = os.path.join(current_folder, "Track.json")
def main():
    segment_to_points = SegmentToPoints()
    points_file_path = segment_to_points.generate_points_from_track(track_file_path, plot=True, save=True, result_filename='Segment_to_Points')
    points_to_segment = PointsToSegment()
    segments_file_path = points_to_segment.generate_segments_from_points(points_file_path, plot=True, save=True, result_filename='Points_to_Segment')
    points_to_segment = SpeedProfile()
    points_to_segment.generate_track_speed_profile_from_segments(segments_file_path, plot=True)

if __name__ == "__main__":
    main()