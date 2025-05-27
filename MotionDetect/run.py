from motion_detect import MotionDetect
from datetime import datetime
import os

source = os.getenv('SOURCE', '')
cam_name = os.getenv('CAM_NAME', '')
min_size_movement = os.getenv('MOVEMENT_SIZE_MIN', 2000)
max_size_movement = os.getenv('MOVEMENT_SIZE_MAX', 200000)
hour_cut = os.getenv('HOUR_CUT', 3)
must_separate_cut = os.getenv('MUST_SEPARATE_CUT', "True").lower() in ("true", "1", "t")

if source == '':
    print('Define source')
    exit()
if cam_name == '':
    print('Define camera name')
    exit(1)

md = MotionDetect()
md.MIN_SIZE_FOR_MOVEMENT = min_size_movement
md.MAX_SIZE_FOR_MOVEMENT = max_size_movement
md.hours_to_cut = hour_cut
md.MUST_SEPARATE_CUT = must_separate_cut
md.camera_name = cam_name

md.avoid_x = 510 #490
md.avoid_y = 55 #45

current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
print(f'Started at {current_datetime}')
folder = f'Volumes/records'
md.apply(source, folder)
current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
print(f'Ended at {current_datetime}')

exit(1)