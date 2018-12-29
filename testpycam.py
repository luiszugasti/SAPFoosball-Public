from picamera import PiCamera
from time import sleep

camera = PiCamera()

#define camera parameters
camera.resolution = (1920, 1080)
camera.framerate = 30

#Open up camera
camera.start_preview()
#sleep(5)
#camera.rotation = 180
#sleep(5)
#camera.rotation = 0
#sleep(5)
#camera.capture('/home/pi/Desktop/image.jpg')
#sleep(2)
camera.start_recording('/home/pi/video.h264')
sleep(5)
camera.stop_recording()
camera.stop_preview()