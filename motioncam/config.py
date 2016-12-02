"""
This file contains all of the configuration values for motioncam
Update this file with values for your specific settings/configuration
Please read the short descriptions before altering a value
"""

# Option to display what is logged without
# having to constantly check log files
# 0 - Logs are written quietly
# 1 - Logs are displayed onto console as well
LOG_DISPLAY = 1


# Directory used to store log files
# Leave value None for Home directory ('~')
DIR_LOG = None

# Directory used to store images and video
# Leave value None for Home directory ('~')
DIR_CAPTURES = None

# Max storage limit for DIR_CAPTURES directory
# Program will end once the limit is reached
# Value measured in MB
STORAGE_SIZE_LIMIT = 100

# Disable or enable the pi-camera LED
# 0 - Disable
# 1 - Enable
LED = 0

# Resolution for images taken by the pi-camera
# Value order - ( width , height )
IMAGE_RESOLUTION = (1920, 1080)

# Resolution for video taken by the pi-camera
# Value order - ( width , height )
VIDEO_RESOLUTION = (1280, 720)

# Length of video when recorded by the pi-camera
# Value measured in seconds
VIDEO_LENGTH = 30

# In order to detect motion, the pi-camera captures
# two images and compares, this is the delay before
# capturing the second image
# Value measured in seconds
CAPTURE_DELAY = 5

# No two images are ever exactly the same when comparing
# down to the pixel level, we must compensate
#
# PIXEL_SENSITIVITY - the range difference that decides whether
#                     two pixels are similar or not
#                     Uses RGB range 0-255
#                     i.e: 05.00% * 255 = 12.75
#                     DEFAULT VALUE: 03.00
#
# CAPTURE_TRESHOLD - the percentage difference of two images
#                    needed to reach in order to store the image
#                    DEFAULT VALUE: 15.00
#
# Both values measured in percentage ( 00.00 -> 100.00 )
PIXEL_SENSITIVITY = 03.00
CAPTURE_THRESHOLD = 15.00

# Depending on the image resolution, comparing each pixel can
# be a time intensive process
# The value below skips the pixels it checks during the loop
# i.e. range(0, PIXEL_COUNT, PIXEL_SKIP)
# It is recommended to adjust along with IMAGE_RESOLUTION
# Different values result in different patterns to check the image
# Further research and testing is required to find best value
PIXEL_SKIP = 11

# The limit of consecutive motion captures before
# triggering a video recording
VIDEO_TRIGGER_LIMIT = 5
