# Copyright 2025 David Marc MéTIN
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cv2
import numpy as np
import mediapipe as mp
import subprocess
import os

# Global parameters
VIDEO_PATH = "input_video.mp4"  # Input video
OUTPUT_DIR = "dance_analysis_output"
AUDIO_TEMP = "temp_audio.wav"
SAMPLE_RATE = 22050
WINDOW_SIZE = 16  # Window size for capturing poses
INVERSE_MODE_SELFIE = 0
HAS_IMAGE = 0

# Create output directory
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Extract audio from video
def extract_audio_from_video(video_path, output_audio_path):
    if os.path.exists(output_audio_path):
        os.remove(output_audio_path)
    command = ["ffmpeg", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", str(SAMPLE_RATE), "-ac", "1", output_audio_path, "-y"]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

# Extract poses with MediaPipe
def extract_poses(video_path, window_size):
    cap = cv2.VideoCapture(video_path)
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    poses = []
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    window_frames = min(int(window_size * fps), total_frames)
    for i in range(window_frames):
        ret, frame = cap.read()
        if not ret:
            break
        if INVERSE_MODE_SELFIE:
            frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]
        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        keypoints = []
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            keypoints = [(int(l.x * width), int(l.y * height)) for l in landmarks]
        poses.append(keypoints if keypoints else None)
    cap.release()
    pose.close()
    poses = interpolate_missing_poses(poses)
    return poses, fps

# Interpolate missing poses
def interpolate_missing_poses(poses):
    interpolated_poses = []
    last_valid_pose = None
    for pose in poses:
        if pose is not None:
            interpolated_poses.append(pose)
            last_valid_pose = pose
        else:
            interpolated_poses.append(last_valid_pose if last_valid_pose else None)
    return interpolated_poses

# Generate annotated video
def generate_annotated_video(video_path, poses, fps, output_video_path, audio_path):
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
    frame_idx = 0

    # Define connections with colors (BGR)
    connections = [
        (mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX, mp.solutions.pose.PoseLandmark.RIGHT_ANKLE, (0, 0, 255)),
        (mp.solutions.pose.PoseLandmark.RIGHT_ANKLE, mp.solutions.pose.PoseLandmark.RIGHT_KNEE, (0, 0, 255)),
        (mp.solutions.pose.PoseLandmark.RIGHT_KNEE, mp.solutions.pose.PoseLandmark.RIGHT_HIP, (0, 0, 255)),
        (mp.solutions.pose.PoseLandmark.LEFT_FOOT_INDEX, mp.solutions.pose.PoseLandmark.LEFT_ANKLE, (0, 0, 128)),
        (mp.solutions.pose.PoseLandmark.LEFT_ANKLE, mp.solutions.pose.PoseLandmark.LEFT_KNEE, (0, 0, 128)),
        (mp.solutions.pose.PoseLandmark.LEFT_KNEE, mp.solutions.pose.PoseLandmark.LEFT_HIP, (0, 0, 128)),
        (mp.solutions.pose.PoseLandmark.RIGHT_WRIST, mp.solutions.pose.PoseLandmark.RIGHT_ELBOW, (0, 255, 0)),
        (mp.solutions.pose.PoseLandmark.RIGHT_ELBOW, mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER, (0, 255, 0)),
        (mp.solutions.pose.PoseLandmark.LEFT_WRIST, mp.solutions.pose.PoseLandmark.LEFT_ELBOW, (0, 128, 0)),
        (mp.solutions.pose.PoseLandmark.LEFT_ELBOW, mp.solutions.pose.PoseLandmark.LEFT_SHOULDER, (0, 128, 0)),
        (mp.solutions.pose.PoseLandmark.RIGHT_HIP, mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER, (255, 0, 0)),
        (mp.solutions.pose.PoseLandmark.LEFT_HIP, mp.solutions.pose.PoseLandmark.LEFT_SHOULDER, (255, 0, 0)),
        (mp.solutions.pose.PoseLandmark.LEFT_HIP, mp.solutions.pose.PoseLandmark.RIGHT_HIP, (255, 0, 0)),
        (mp.solutions.pose.PoseLandmark.LEFT_SHOULDER, mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER, (255, 0, 0)),
    ]

    while frame_idx < len(poses):
        if HAS_IMAGE:
            ret, frame = cap.read()
            if not ret:
                break
            if INVERSE_MODE_SELFIE:
                frame = cv2.flip(frame, 1)
        else:
            frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)  # Black background

        keypoints = poses[frame_idx]
        if keypoints:
            for point in keypoints:
                cv2.circle(frame, tuple(map(int, point)), 5, (0, 255, 255), -1)
            for start_idx, end_idx, color in connections:
                start_point = tuple(map(int, keypoints[start_idx.value]))
                end_point = tuple(map(int, keypoints[end_idx.value]))
                cv2.line(frame, start_point, end_point, color, 2)

        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()
    add_audio_to_video(output_video_path, audio_path, output_video_path)

# Add audio to video
def add_audio_to_video(video_path, audio_path, output_path):
    temp_encoded = os.path.join(OUTPUT_DIR, "temp_encoded_video.mp4")
    encode_cmd = ["ffmpeg", "-i", video_path, "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p", temp_encoded, "-y"]
    audio_cmd = ["ffmpeg", "-i", temp_encoded, "-i", audio_path, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", output_path, "-y"]
    subprocess.run(encode_cmd, check=True)
    subprocess.run(audio_cmd, check=True)
    if os.path.exists(temp_encoded):
        os.remove(temp_encoded)

# Main program
def main():
    print("Extracting poses...")
    poses, fps = extract_poses(VIDEO_PATH, WINDOW_SIZE)
    print("Extracting audio...")
    audio_path = os.path.join(OUTPUT_DIR, AUDIO_TEMP)
    extract_audio_from_video(VIDEO_PATH, audio_path)
    print("Generating annotated video...")
    generate_annotated_video(VIDEO_PATH, poses, fps, os.path.join(OUTPUT_DIR, "annotated_video_v02.mp4"), audio_path)
    print("Done! Video saved at", os.path.join(OUTPUT_DIR, "annotated_video_v02.mp4"))

if __name__ == "__main__":
    main()