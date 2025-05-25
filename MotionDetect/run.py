from motion_detect import MotionDetect
from datetime import datetime
import os

source = os.getenv('SOURCE', '')
cam_name = os.getenv('CAM_NAME', '')
min_size_movement = os.getenv('MOVEMENT_SIZE_MIN', 2000)
max_size_movement = os.getenv('MOVEMENT_SIZE_MAX', 200000)
hour_cut = os.getenv('HOUR_CUT', 0)
must_separate_cut = os.getenv('MUST_SEPARATE_CUT', "True").lower() in ("true", "1", "t")

if source == '':
    print('Define source')
    exit()
if cam_name == '':
    print('Define camera name')
    exit(1)

# minSizeMovements = [25, 50, 100, 200, 400, 800, 1600, 3000, 6000, 9000, 12000, 15000, 20000]
minSizeMovements = [min_size_movement]
for minSizeMovement in minSizeMovements:
    md = MotionDetect()
    md.MIN_SIZE_FOR_MOVEMENT = minSizeMovement
    md.MAX_SIZE_FOR_MOVEMENT = max_size_movement
    md.hours_to_cut = hour_cut
    md.MUST_SEPARATE_CUT = must_separate_cut
    md.camera_name = cam_name
    # md.LIMIT_TOTAL_FRAMES = 60 * 60 * 10 #TODO just for testing 

    # source = "Volumes/imggen/sample.mp4" # webcam| rtsp_url | video file as input'
    # source = "rtsp://admin:senha123@192.168.0.49/onvif1"

    # source = "rtsp://administrador:administrador@192.168.0.50/stream1"; # TAPO

    # source = "rtsp://admin:senha123@192.168.0.49/stream1"; # IPEGA
    # source = "rtsp://admin:senha123@192.168.0.49/onvif1"; # IPEGA
    # source = "rtsp://192.168.0.42:8554/teste2"
    md.avoid_x = 510 #490
    md.avoid_y = 55 #45

    # source = "rtsp://192.168.0.42/live"; # IPEGA

    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    print(f'Started at {current_datetime}')
    folder = f'Volumes/records'
    md.apply(source, folder)
    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    print(f'Ended at {current_datetime}')

    # rtsp://admin:admin@192.168.0.10:1945
exit(1)