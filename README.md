# 🤖 Autonomous UGV Rover | Vision-Based Obstacle Avoidance

An autonomous Unmanned Ground Vehicle (UGV) built using the **Waveshare UGV Rover platform and Raspberry Pi**, implementing real-time obstacle detection and reactive navigation using classical computer vision.

The rover uses an onboard camera to analyze its surroundings, identify potential obstacles, and make navigation decisions by controlling its left and right motors independently.

## Project Demo

<!-- Add your rover photograph here -->
<img width="2160" height="3010" alt="UGV Rover" src="https://github.com/user-attachments/assets/7d4434a9-be89-444a-b328-80586ccf3d62" />


**Demo Video:** [Watch Autonomous Navigation Demo](https://lnkd.in/p/gHjRukte)

## Project Objective

The primary objective of this project is to develop a vision-based obstacle avoidance system that allows a mobile robot to navigate an environment without continuous human intervention.

Instead of relying on ultrasonic sensors or a pre-trained deep learning model, this implementation uses classical computer vision techniques to distinguish the floor from potential obstacles and make real-time movement decisions.

## Hardware Components

| Component | Purpose |
|---|---|
| Waveshare UGV Rover | Mobile robotic platform |
| Raspberry Pi | Main onboard computing unit |
| USB/CSI Camera | Visual perception |
| DC Motors | Rover locomotion |
| Motor Controller | Motor speed and direction control |

*Refer to your specific Waveshare UGV hardware configuration for exact component specifications.*

## Software and Technologies

- **Python** – Main programming language
- **OpenCV** – Image processing and visual perception
- **NumPy** – Numerical operations and image analysis
- **Raspberry Pi OS** – Onboard computing environment
- **Waveshare Base Controller** – Motor communication and control
- **Jupyter Notebook** – Development and visualization

## System Architecture

The rover follows a reactive perception-to-action pipeline:

```text
       Camera Input
            |
            v
     Image Acquisition
            |
            v
      Image Processing
       (OpenCV)
            |
            v
     BGR to LAB Conversion
            |
            v
      Floor Calibration
            |
            v
   Obstacle Identification
            |
            v
    Divide Image into Zones
       /      |      \
      /       |       \
   Left     Centre    Right
      \       |       /
       \      |      /
            v
     Navigation Decision
            |
            v
      Motor Control
            |
            v
      Rover Movement
            |
            +------> Repeat
```

## Obstacle Avoidance Algorithm

The navigation algorithm consists of the following stages:

### 1. Image Acquisition

The onboard camera captures real-time video frames. Each frame is resized to 160 × 120 pixels to reduce computational overhead.

### 2. Image Preprocessing

The captured image is processed using:
- Gaussian Blur to reduce image noise.
- BGR-to-LAB colour space conversion for colour-based floor analysis.

### 3. Floor Calibration

Before navigation begins, the rover observes the floor directly in front of it.

A small region from the lower-centre portion of the image is selected, and its average LAB colour is calculated as the reference floor colour.

### 4. Obstacle Detection

For each pixel, the Euclidean colour distance from the reference floor colour is calculated:

\[
D(x,y)=\|I_{LAB}(x,y)-F_{LAB}\|_2
\]

Where:

- \(I_{LAB}\) = LAB color of the current pixel.
- \(F_{LAB}\) = Reference floor color.
- \(D(x,y)\) = Color distance.

Pixels with a colour distance greater than a predefined threshold are classified as potential obstacles.

### 5. Zone-Based Analysis

The lower half of the image is divided into three regions:

- **Left Zone**
- **Center Zone**
- **Right Zone**

The proportion of pixels classified as obstacles is calculated independently for each region.

### 6. Navigation Decision

The rover uses the following decision-making strategy:

| Condition | Action |
|---|---|
| Center path is clear | Move forward |
| Center path is blocked | Rotate in place |
| Left side has more obstacles | Prefer turning right |
| Right side has more obstacles | Prefer turning left |
| Side clutter while moving forward | Apply gentle steering correction |

The rover uses a reactive navigation strategy rather than a predefined global path.

## Getting Started

### Prerequisites

- Raspberry Pi with Raspberry Pi OS.
- Waveshare UGV Rover hardware.
- Compatible camera connected to the Raspberry Pi.
- Python 3.
- Access to the Waveshare base controller library.

### 1. Clone the Repository

```bash
git clone https://github.com/iamrealrushi/AutoNav.git

cd AutoNav
```

### 2. Install Dependencies

```bash
sudo apt update

sudo apt install python3-opencv python3-numpy
```

If you are using Jupyter Notebook for development:

```bash
pip install ipywidgets notebook
```

### 3. Configure the Hardware

Ensure that:
- The camera is connected and accessible.
- The motor controller is connected to the Raspberry Pi.
- The serial communication port is configured correctly.
- The Waveshare `base_ctrl` module is available in your Python environment.

The current implementation uses:

```python
base = BaseController('/dev/ttyAMA0', 115200)
```

Adjust the serial port and baud rate according to your hardware configuration.

### 4. Run the Program

Run the Python script or execute the notebook containing the obstacle avoidance implementation.

```bash
python3 main.py
```

**Important:** The rover should initially face a clear, uniformly colored floor surface so that the floor calibration can work correctly.

## Algorithm Parameters

The following parameters control the rover's navigation behaviour:

| Parameter | Default Value | Description |
|---|---:|---|
| `SPEED` | 0.15 | Forward motor speed |
| `TURN` | 0.20 | Rotation speed |
| `BLOCKED` | 0.30 | Obstacle density threshold for blocking the centre zone |
| `DIFF` | 25 | LAB color distance threshold |

These parameters can be tuned depending on lighting conditions, floor colour, camera position, and environment.

## Real-Time Visualization

The implementation also provides a visual representation of the obstacle detection process.

- Potential obstacles are highlighted in red.
- Green lines separate the three navigation zones.
- Obstacle density for each zone is displayed.
- The current navigation action is displayed on the camera feed.

This visualization helps in debugging the perception and navigation pipeline.

## Limitations

The current implementation is an experimental, vision-based reactive obstacle avoidance system.

Some limitations include:

- Performance depends on lighting conditions.
- Floor calibration assumes a reasonably uniform floor surface.
- Objects with colors similar to the floor may not be detected reliably.
- Shadows and reflections can cause false obstacle detections.
- The system does not perform SLAM or environment mapping.
- Obstacle detection is based on colour difference rather than semantic object recognition.

## Future Improvements

Potential extensions to this project include:

- Integration with ROS 2 for modular robot software architecture.
- Implementation of SLAM for environment mapping and localization.
- Depth-based obstacle detection using depth cameras.
- Sensor fusion using camera, LiDAR, and ultrasonic sensors.
- Global path planning using A* or other planning algorithms.
- Deep learning-based object detection.
- Improved navigation in dynamic and unstructured environments.

## Learning Outcomes

Through this project, I explored and implemented:

- Camera-based visual perception.
- Classical computer vision techniques.
- LAB colour space for image analysis.
- Real-time image processing using OpenCV.
- Reactive obstacle avoidance.
- Differential motor control.
- Integration of software with a physical mobile robot.

## Author

**Rushikesh Waghmare**

M.Tech Robotics and AI | IIT Guwahati

Interested in mobile robotics, autonomous systems, computer vision, and intelligent robotic navigation.

- **LinkedIn:** [Your LinkedIn Profile](www.linkedin.com/in/iamrealrushi)
- **GitHub:** [Your GitHub Profile](https://github.com/iamrealrushi)

---

⭐ If you find this project interesting, consider starring the repository!

*Built as part of my exploration of autonomous mobile robotics and vision-based navigation.*
