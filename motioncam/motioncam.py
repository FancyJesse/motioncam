#!/usr/bin/env python3
from threading import Lock
import io
import os
import time

from PIL import Image
import picamera

from logger import log
import config


MUTEX = Lock()
PICAM = None


def setup():
	try:
		if config.LOG_DISPLAY:
			print('DISPLAY MODE IS ON - ALL LOG DATA WILL BE DISPLAYED ON CONSOLE')

		# Directory check
		if config.DIR_LOG == None:
			config.DIR_LOG = os.path.expanduser('~') + '/motioncam/log/'
		if config.DIR_CAPTURES == None:
			config.DIR_CAPTURES = os.path.expanduser('~') + '/motioncam/captures/'
		if not os.path.exists(config.DIR_LOG):
			os.makedirs(config.DIR_LOG)
		if not os.path.exists(config.DIR_CAPTURES):
			os.makedirs(config.DIR_CAPTURES)
		log(__name__, 'Directory Check Complete')

		# Initialize pi-camera
		global PICAM
		PICAM = picamera.PiCamera()
		PICAM.led = config.LED
		PICAM.resolution = config.IMAGE_RESOLUTION
		if config.CAPTURE_DELAY < 0:
			config.CAPTURE_DELAY = 0
		PICAM.start_preview()
		time.sleep(2)
		log(__name__, 'Camera Online')
	except:
		exit()


def close():
	global PICAM
	try:
		PICAM.close()
		log(__name__, 'Camera Offline')
	except:
		pass


def storage_available():
	currentSize = 0
	for fileName in os.listdir(config.DIR_CAPTURES):
		filePath = os.path.join(config.DIR_CAPTURES, fileName)
		currentSize += os.path.getsize(filePath)
	currentSizeMB = currentSize / (1024 * 1024)
	storage_available = config.STORAGE_SIZE_LIMIT > currentSizeMB
	if not storage_available:
		log(__name__, 'Storage Limit Reached - {:.2f}MB'.format(currentSizeMB))
	return storage_available


def get_image_stream():
	global PICAM
	try:
		MUTEX.acquire()
		stream = io.BytesIO()
		title = 'Image_%s.jpg' % time.strftime('%Y%m%d-%H%M%S')
		PICAM.capture(stream, format='jpeg')
		stream.seek(0)
		image = Image.open(stream)
		return image, title
	finally:
		MUTEX.release()


def record(length=config.VIDEO_LENGTH):
	global PICAM
	try:
		MUTEX.acquire()
		PICAM.resolution = config.VIDEO_RESOLUTION
		capName = 'Video_%s.h264' % time.strftime('%Y%m%d-%H%M%S')
		PICAM.start_recording(config.DIR_CAPTURES + capName)
		PICAM.wait_recording(length)
		PICAM.stop_recording()
	finally:
		PICAM.resolution = config.IMAGE_RESOLUTION
		MUTEX.release()
		log(__name__, 'Captured - {}'.format(capName))


def motion_capture():
	total_pixels = config.IMAGE_RESOLUTION[0] * config.IMAGE_RESOLUTION[1]
	pixel_limit = (total_pixels / config.PIXEL_SKIP) * ((100 - config.CAPTURE_THRESHOLD) / 100)
	sensitivity = 255 * (config.PIXEL_SENSITIVITY / 100)

	image1 = get_image_stream()[0]
	pixels1 = list(image1.getdata())

	video_trigger_cnt = 0
	space_available = storage_available()
	while space_available:
		time.sleep(config.CAPTURE_DELAY)

		image2, title2 = get_image_stream()
		pixels2 = list(image2.getdata())

		similar_pixels = 0
		for i in range(0, total_pixels, config.PIXEL_SKIP):
			offset = (
				abs(pixels1[i][0] - pixels2[i][0]),
				abs(pixels1[i][1] - pixels2[i][1]),
				abs(pixels1[i][2] - pixels2[i][2]))

			if offset[0] <= sensitivity and offset[1] <= sensitivity and offset[2] <= sensitivity:
				similar_pixels += 1
				if similar_pixels > pixel_limit:
					video_trigger_cnt = 0
					break

		image_difference = 100 - (similar_pixels / pixel_limit) * 100
		if image_difference >= config.CAPTURE_THRESHOLD:
			video_trigger_cnt += 1
			image2.save(config.DIR_CAPTURES + title2)
			log(__name__, 'Motion Detected - {:.2f}% - Captured - {}'.format(image_difference, title2))

			if video_trigger_cnt == config.VIDEO_TRIGGER_LIMIT:
				record()
				video_trigger_cnt = 0

			space_available = storage_available()

		image1 = image2
		pixels1 = pixels2


def main():
	try:
		setup()
		motion_capture()
	except Exception as e:
		log(__name__, 'Something Went Wrong - {}'.format(e))
	finally:
		log(__name__, 'MotionCam Preparing to Exit ...')
		close()
		log(__name__, 'Good Bye.')


if __name__ == "__main__":
	main()
