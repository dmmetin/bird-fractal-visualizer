# Dance Video to Robot Skeleton

This project transforms a dance video into a video where a colored skeleton reproduces the dancer's movements. It uses MediaPipe for pose detection and OpenCV for drawing the skeleton.

## Prerequisites

- Python 3.8+ (preferably via Miniconda)
- FFmpeg (installed and added to the PATH)

## Installation

1. **Create a virtual environment with Miniconda:**

   ```bash
   conda create -n dance_robot python=3.8
   conda activate dance_robot
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg:**

   - Download FFmpeg from ffmpeg.org.
   - Add it to your system PATH.

## Usage

1. Place your dance video (`input_video.mp4`) in the current directory.

2. Run the program:

   ```bash
   python dance_robot.py
   ```

3. The annotated video will be saved in `dance_analysis_output/annotated_video_v02.mp4`.

## requirements.txt

```
opencv-python
mediapipe
numpy
```

## Library Origins and Licenses

- **OpenCV**: opencv.org, Apache 2.0 License
- **MediaPipe**: mediapipe.dev, Apache 2.0 License
- **NumPy**: numpy.org, BSD License
- **FFmpeg**: ffmpeg.org, LGPL or GPL License (depending on configuration)

## How It Works

1. **Pose Detection**: MediaPipe extracts body keypoints from each frame of the input video.
2. **Interpolation**: Missing poses are filled with the last valid pose.
3. **Skeleton Drawing**: OpenCV draws a colored skeleton on the frames based on the detected poses.
4. **Audio Addition**: FFmpeg recombines the original audio with the annotated video.

This project is a simple demonstration to share accessible tools on GitHub.

## License

This project is licensed under the Apache License, Version 2.0. See the `LICENSE` file for details.

Copyright 2025 David Marc MéTIN

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.