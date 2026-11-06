import cv2, time
import numpy as np
from base_ctrl import BaseController

base = BaseController('/dev/ttyAMA0', 115200)
cam = cv2.VideoCapture(0, cv2.CAP_V4L2)
cam.release()
print(cam.isOpened(), cam.read()[0])

SPEED = 0.15 # forward speed
TURN = 0.2 # turning speed
BLOCKED = 0.30 # fraction of non-floor pixels that counts as blocked
DIFF = 25 # color difference that counts as non-floor

def drive(left, right):
    base.base_json_ctrl({"T": 1, "L": left, "R": right})
def get_lab():
    global small
    ok, frame = cam.read()
    if not ok:
        return None
    small = cv2.resize(frame, (160, 120))
    return cv2.cvtColor(cv2.GaussianBlur(small, (5,5), 0), cv2.COLOR_BGR2LAB).astype(np.float32)
    
def learn_floor():
    for _ in range(10):
        cam.read() # let the camera settle
    lab = get_lab()
    h, w = lab.shape[:2]
    patch = lab[h-30:h-10, w//2-20:w//2+20] # floor just in front of rover
    return patch.reshape(-1, 3).mean(axis=0)
def get_zones(lab, floor):
    obstacle = np.linalg.norm(lab - floor, axis=2) > DIFF
    lower = obstacle[lab.shape[0] // 2:, :] # bottomhalf only
    left, center, right = [z.mean() for z in
    np.array_split(lower, 3, axis=1)]
    return left, center, right
    
import ipywidgets as widgets
from IPython.display import display

video = widgets.Image(format='jpeg')
def show(lab, floor, left, center, right, action):
    img = small.copy()
    mask = np.linalg.norm(lab - floor, axis=2) > DIFF
    img[mask] = (img[mask] * 0.5 + np.array([0, 0, 127])).astype(np.uint8) # red = obstacle
    img = cv2.resize(img, (480, 360))
    cv2.line(img, (0, 180), (480, 180), (0, 255, 0), 1) # zones start here
    cv2.line(img, (160, 180), (160, 360), (0, 255, 0), 1)
    cv2.line(img, (320, 180), (320, 360), (0, 255, 0), 1)
    cv2.putText(img, f"L{left:.2f} C{center:.2f} R{right:.2f} {action}", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    video.value = cv2.imencode('.jpg', img)[1].tobytes()
    
display(video)
floor = learn_floor() # rover must face clear floor now
turn_dir = 0 # 1 = turning left, -1 = turning right

try:
    while True:
        lab = get_lab()
        if lab is None:
            continue
        left, center, right = get_zones(lab, floor)
        if center < BLOCKED: # path clear: go forwardturn_dir = 0
            s = (left - right) * 0.3 # gentle steer away from side clutter
            drive(SPEED + s, SPEED - s)
        else: # blocked: turn on the spot
            if turn_dir == 0:
                turn_dir = 1 if left < right else -1
            drive(-TURN * turn_dir, TURN * turn_dir)
            
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopped")
finally:
    drive(0, 0)
