import cv2
import os
from natsort import natsorted

def create_video_from_image_folder(frame_dir, output_path='reconstructed_video.mp4', fps=25):
    """
    Combines image frames from a folder into an MP4 video.

    Args:
        frame_dir (str): Path to the folder containing image frames.
        output_path (str): Path to save the output video file.
        fps (int): Frames per second of the output video.
    """
    # Get all image file paths and sort them naturally (e.g., frame1.jpg, frame2.jpg, ...)
    frame_files = [f for f in os.listdir(frame_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    frame_files = natsorted(frame_files)

    if not frame_files:
        raise ValueError("No image frames found in the directory.")

    # Read the first frame to get dimensions
    first_frame_path = os.path.join(frame_dir, frame_files[0])
    frame = cv2.imread(first_frame_path)
    height, width, _ = frame.shape

    # Define video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Write each frame to the video
    for file_name in frame_files:
        frame_path = os.path.join(frame_dir, file_name)
        frame = cv2.imread(frame_path)
        out.write(frame)

    out.release()
    print(f"[✓] Video saved to {output_path}")


# Example usage
if __name__ == "__main__":
    frame_folder = "01-01"  # Replace with your frame folder path
    create_video_from_image_folder(frame_folder)