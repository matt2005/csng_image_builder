#!/usr/bin/python3 -u

import socket
import sys
import os
import threading
import time
import datetime as dt
import imp
import subprocess
from threading import Thread
from PIL import Image

# set default paths
imageoverlay = "/boot/crankshaft/camera-overlay.png"

if (os.path.ismount("/media/USBDRIVES/CSSTORAGE")):
    os.system("sudo mkdir -p /media/USBDRIVES/CSSTORAGE/RPIDC/AUTOSAVE")
    os.system("sudo mkdir -p /media/USBDRIVES/CSSTORAGE/RPIDC/EVENTS")
    os.system("sudo chmod 777 /media/USBDRIVES/CSSTORAGE/RPIDC -R")
    recordpath = "/media/USBDRIVES/CSSTORAGE/RPIDC/"
    storagepath = "/media/USBDRIVES/CSSTORAGE/RPIDC/"
else:
    os.system("sudo mkdir -p /tmp/RPIDC/AUTOSAVE")
    os.system("sudo mkdir -p /tmp/RPIDC/EVENTS")
    os.system("sudo chmod 777 /tmp/RPIDC -R")
    recordpath = "/tmp/RPIDC/"
    storagepath = "/tmp/RPIDC/"

# Camera library compatibility layer
camera_api = None
try:
    # Try modern picamera2 first (Trixie/Bookworm+)
    from picamera2 import Picamera2
    from libcamera import controls, Transform
    camera_api = "picamera2"
    print("Using modern picamera2 library")
except ImportError:
    try:
        # Fallback to legacy picamera (Buster/Bullseye)
        imp.find_module('picamera')
        import picamera
        from picamera import PiCamera
        camera_api = "picamera"
        print("Using legacy picamera library")
    except ImportError:
        print("No camera library available! Install python3-picamera2 or python3-picamera")
        quit()

class CameraWrapper:
    """Compatibility wrapper for picamera and picamera2 APIs"""
    
    def __init__(self):
        self.api = camera_api
        self.recording = False
        self.preview_active = False
        self._annotate_text = ""
        self._annotate_background = None
        self._annotate_text_size = 20
        
        if self.api == "picamera2":
            self.camera = Picamera2()
            self.video_config = self.camera.create_video_configuration(main={"size": (1920, 1080)})
            self.preview_config = self.camera.create_preview_configuration(main={"size": (1920, 1080)})
            self.camera.configure(self.preview_config)
            self.camera.start()
            
            # Default values for picamera2
            self._resolution = (1920, 1080)
            self._rotation = 0
            self._framerate = 30
            self._awb_mode = "auto"
            self._exposure_mode = "auto"
            self._hflip = False
            self._vflip = False
        else:
            self.camera = PiCamera()
            # picamera defaults
            self._resolution = (1920, 1080)
            self._rotation = 0
            self._framerate = 30
            self._awb_mode = "auto"
            self._exposure_mode = "auto"
            self._hflip = False
            self._vflip = False
            
    @property
    def resolution(self):
        return self._resolution
        
    @resolution.setter
    def resolution(self, value):
        self._resolution = value
        if self.api == "picamera":
            self.camera.resolution = value
        else:
            # For picamera2, need to reconfigure
            if value == (1920, 1080):
                self._annotate_text_size = 80
            elif value == (1280, 720):
                self._annotate_text_size = 40
            else:
                self._annotate_text_size = 20
            self.video_config = self.camera.create_video_configuration(main={"size": value})
            self.preview_config = self.camera.create_preview_configuration(main={"size": value})
            
    @property
    def rotation(self):
        return self._rotation
        
    @rotation.setter
    def rotation(self, value):
        self._rotation = value
        if self.api == "picamera":
            self.camera.rotation = value
        else:
            # picamera2 uses Transform
            transform = Transform()
            if value == 90:
                transform = Transform(rotation=90)
            elif value == 180:
                transform = Transform(rotation=180)
            elif value == 270:
                transform = Transform(rotation=270)
            # Apply transform in next configure
            
    @property
    def framerate(self):
        return self._framerate
        
    @framerate.setter
    def framerate(self, value):
        self._framerate = value
        if self.api == "picamera":
            self.camera.framerate = value
        # picamera2 framerate is set in configuration
            
    @property
    def awb_mode(self):
        return self._awb_mode
        
    @awb_mode.setter
    def awb_mode(self, value):
        self._awb_mode = value
        if self.api == "picamera":
            self.camera.awb_mode = value
        else:
            # picamera2 uses controls
            awb_map = {
                'auto': controls.AwbModeEnum.Auto,
                'off': controls.AwbModeEnum.Manual,
                'sunlight': controls.AwbModeEnum.Daylight,
                'cloudy': controls.AwbModeEnum.Cloudy,
                'shade': controls.AwbModeEnum.Shade,
                'tungsten': controls.AwbModeEnum.Tungsten,
                'fluorescent': controls.AwbModeEnum.Fluorescent,
                'incandescent': controls.AwbModeEnum.Incandescent,
                'flash': controls.AwbModeEnum.Flash,
                'horizon': controls.AwbModeEnum.Auto  # fallback
            }
            if value in awb_map:
                self.camera.set_controls({"AwbMode": awb_map[value]})
                
    @property
    def exposure_mode(self):
        return self._exposure_mode
        
    @exposure_mode.setter
    def exposure_mode(self, value):
        self._exposure_mode = value
        if self.api == "picamera":
            self.camera.exposure_mode = value
        else:
            # picamera2 uses AeEnable and manual controls
            if value == "auto":
                self.camera.set_controls({"AeEnable": True})
            elif value == "off":
                self.camera.set_controls({"AeEnable": False})
            # Other modes would need specific control mappings
                
    @property
    def hflip(self):
        return self._hflip
        
    @hflip.setter
    def hflip(self, value):
        self._hflip = value
        if self.api == "picamera":
            self.camera.hflip = value
        else:
            # picamera2 uses Transform
            transform = Transform(hflip=value, vflip=self._vflip)
            # Apply in next configure
            
    @property
    def vflip(self):
        return self._vflip
        
    @vflip.setter
    def vflip(self, value):
        self._vflip = value
        if self.api == "picamera":
            self.camera.vflip = value
        else:
            # picamera2 uses Transform
            transform = Transform(hflip=self._hflip, vflip=value)
            # Apply in next configure
            
    @property
    def annotate_text(self):
        return self._annotate_text
        
    @annotate_text.setter
    def annotate_text(self, value):
        self._annotate_text = value
        if self.api == "picamera":
            self.camera.annotate_text = value
        # picamera2 doesn't have built-in annotation, would need overlay
        
    @property
    def annotate_background(self):
        return self._annotate_background
        
    @annotate_background.setter
    def annotate_background(self, value):
        self._annotate_background = value
        if self.api == "picamera":
            self.camera.annotate_background = value
        # picamera2 doesn't have built-in annotation background
        
    @property
    def annotate_text_size(self):
        return self._annotate_text_size
        
    @annotate_text_size.setter
    def annotate_text_size(self, value):
        self._annotate_text_size = value
        if self.api == "picamera":
            self.camera.annotate_text_size = value
        # picamera2 doesn't have built-in annotation sizing
        
    def start_preview(self, **kwargs):
        if self.api == "picamera":
            self.camera.start_preview(**kwargs)
        else:
            # picamera2 preview is always running after start()
            pass
        self.preview_active = True
        
    def stop_preview(self):
        if self.api == "picamera":
            self.camera.stop_preview()
        # picamera2 doesn't stop preview separately
        self.preview_active = False
        
    def start_recording(self, output, **kwargs):
        if self.api == "picamera":
            self.camera.start_recording(output, **kwargs)
        else:
            # picamera2 recording
            if not self.recording:
                self.camera.configure(self.video_config)
                self.camera.start_recording(output, **kwargs)
        self.recording = True
        
    def stop_recording(self):
        if self.recording:
            self.camera.stop_recording()
            if self.api == "picamera2":
                # Switch back to preview config
                self.camera.configure(self.preview_config)
        self.recording = False
        
    def add_overlay(self, source, **kwargs):
        if self.api == "picamera":
            return self.camera.add_overlay(source, **kwargs)
        else:
            # picamera2 overlay would need different implementation
            # Return dummy overlay object for compatibility
            class DummyOverlay:
                def __init__(self):
                    self.alpha = 0
                    self.layer = 0
            return DummyOverlay()
            
    def close(self):
        if self.recording:
            self.stop_recording()
        if self.api == "picamera2":
            self.camera.stop()
        self.camera.close()

def get_var(varname):
    #print("Request:" + varname)
    CMD = 'echo $(source /boot/crankshaft/crankshaft_env.sh; echo $%s)' % varname
    p = subprocess.Popen(CMD, stdout=subprocess.PIPE, shell=True, executable='/bin/bash')
    try:
        result = p.stdout.readlines()[0].strip()
    except:
        result = ""

    CMD = 'echo $(source /opt/crankshaft/crankshaft_default_env.sh; echo $%s)' % varname
    p = subprocess.Popen(CMD, stdout=subprocess.PIPE, shell=True, executable='/bin/bash')
    try:
        resultfb = p.stdout.readlines()[0].strip()
    except:
        resultfb = ""

    if (result != ""):
        return result.decode('utf-8')
    else:
        return resultfb.decode('utf-8')

# Create a TCP/IP socket
sockdc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get display resolution
rescheck = str.strip(os.popen("fbset | grep geometry").read())
resarray = rescheck.split(' ')
resx = int(resarray[1])
resy = int(resarray[2])

# Initialize camera with compatibility wrapper
camera = CameraWrapper()
if (get_var('RPICAM_RESOLUTION') == "1080"):
    camera.resolution = (1920, 1080)
    camera.annotate_text_size = 80
elif (get_var('RPICAM_RESOLUTION') == "720"):
    camera.resolution = (1280, 720)
    camera.annotate_text_size = 40
else:
    camera.resolution = (800, 480)
    camera.annotate_text_size = 20

rearcammode = "false"
rearcamoverlay = "false"

# init from crankshaft_env
respreview_w = int(get_var('RPICAM_WIDTH'))
respreview_h = int(get_var('RPICAM_HEIGTH'))
respreview_x = int(get_var('RPICAM_X'))
respreview_y = int(get_var('RPICAM_Y'))
camera.rotation = int(get_var('RPICAM_ROTATION'))
camera.framerate = int(get_var('RPICAM_FPS'))
camera.awb_mode = str(get_var('RPICAM_AWB'))
camera.exposure_mode = str(get_var('RPICAM_EXP'))
recordtime = int(get_var('RPICAM_LOOPTIME'))
loopcount = int(get_var('RPICAM_LOOPCOUNT'))
start_recording = int(get_var('RPICAM_AUTORECORDING'))

hflip = int(get_var('RPICAM_HFLIP'))
if hflip == 1:
    camera.hflip = True
else:
    camera.hflip = False

vflip = int(get_var('RPICAM_VFLIP'))
if vflip == 1:
    camera.vflip = True
else:
    camera.vflip = False

respreview_y_correction = int(get_var('RPICAM_YCORRECTION'))
respreview_zoom = int(get_var('RPICAM_ZOOM'))

print("RPi-Camera: Res - " + str(get_var('RPICAM_RESOLUTION')))
print("RPi-Camera: Width  - " + str(respreview_w))
print("RPi-Camera: Heigth - " + str(respreview_h))
print("RPi-Camera: FPS - " + str(camera.framerate))
print("RPi-Camera: AWB - " + str(camera.awb_mode))
print("RPi-Camera: EXP - " + str(camera.exposure_mode))
print("RPi-Camera: X - " + str(respreview_x))
print("RPi-Camera: Y - " + str(respreview_y))
print("RPi-Camera: HFlip - " + str(hflip))
print("RPi-Camera: VFlip - " + str(vflip))
print("RPi-Camera: YCorrection - " + str(respreview_y_correction))
print("RPi-Camera: Zoom - " + str(respreview_zoom))
print("RPi-Camera: Loop Time - " + str(recordtime))
print("RPi-Camera: Loop Count - " + str(loopcount))
print("RPi-Camera: Start Recording - " + str(start_recording))

# Bind the socket to the address given on the command line
server_address = ('127.0.0.1', 6000)
sockdc.bind(server_address)
print("RPi-Camera: Starting Server...")
sockdc.listen(1)

# define default values

camera_recording = 0
loop_recording = 1
camera_preview = 0
camera_rearcam = 0
savingfile = 0
exit = 0

# Add default overlay for rearcam mode
sizeA = (1280, 720)
img = Image.open(imageoverlay)
pad = Image.new("RGB", (((img.size[0] + 31) // 32) * 32, ((img.size[1] + 15) // 16) * 16))
pad.paste(img, (0, 0), img)
overlay = camera.add_overlay(pad.tobytes(), size=sizeA)
overlay.alpha = 0
overlay.layer = 0

def freespace(p):
    s = os.statvfs(p)
    return round(s.f_bsize * s.f_bavail / 1024 / 1024,0)

free = freespace(recordpath)

def updateWindow():
    global free, camera_recording, savingfile
    counter = 0
    while True:
        if camera_recording == 1:
            if not (os.path.exists("/tmp/dashcam_is_recording")):
                os.system("sudo touch /tmp/dashcam_is_recording")
            if savingfile == 1:
                camera.annotate_text = "RPi-Dashcam - Saving file..."
            else:
                #camera.annotate_text = "RPi-Dashcam - " + dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S') + " (" + str(free) + " MB free)"
                camera.annotate_text = "RPi-Dashcam - " + dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            if loop_recording == 1:
                counter = counter + 0.2
                if counter > recordtime:
                    camera.stop_recording()
                    time.sleep(1.0)
                    camera.annotate_text = "RPi-Dashcam - " + dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S') + " (Moving file to archive...)"
                    source = recordpath + 'RPIDC_' + dt.datetime.now().strftime('%d%m%Y') + '.h264'
                    destination = storagepath + 'AUTOSAVE/RPIDC_AUTOSAVE_' + dt.datetime.now().strftime('%d%m%Y') + '_' + dt.datetime.now().strftime('%H%M%S') + '.h264'
                    print("Moving current recording file to archive...")
                    os.system("mv " + source + " " + destination)
                    print("Cleaning archived loop files to max of " + str(loopcount) + "...")
                    os.system("ls -tpd " + recordpath + "AUTOSAVE/* | grep -v '/$' | tail -n +" + str(loopcount+1) + " | xargs -d '\n' -r rm -- &")
                    camera.start_recording(recordpath + 'RPIDC_' + dt.datetime.now().strftime('%d%m%Y') + '.h264')
                    counter = 0
        if camera_recording == 0 and camera_preview == 1:
            if (os.path.exists("/tmp/dashcam_is_recording")):
                os.system("sudo rm /tmp/dashcam_is_recording")
            camera.annotate_text = ''
            # give us a break
        if camera_recording == 0:
            if (os.path.exists("/tmp/dashcam_is_recording")):
                os.system("sudo rm /tmp/dashcam_is_recording")
        if free <= 128:
            camera.annotate_text = 'Recording stopped !!! - Storage device is full.'
            camera.stop_recording()
            camera_recording = 0
            # give us a break
        time.sleep(0.2)

t1 = Thread(target=updateWindow)
t1.setDaemon(True)
t1.start()

def fsCheck():
    global camera_preview, free
    while True:
        if camera_preview == 1:
            free = freespace(recordpath)
        time.sleep(30)

t2 = Thread(target=fsCheck)
t2.setDaemon(True)
t2.start()

def updateStatus():
    if camera_recording == 1:
        print("RPi-Camera: Recording...")
    else:
        print("RPi-Camera: Not recording...")

updateStatus()

def cameraStartPreview():
    global camera_rearcam, overlay, rearcamoverlay, rearcammode
    if rearcammode == "false":
        camera.start_preview(fullscreen=False,
                             window=(respreview_x, respreview_y + respreview_y_correction, respreview_w + respreview_zoom, respreview_h + respreview_zoom))
        if camera_rearcam == 1:
            overlay.layer = 0
            overlay.alpha = 0
            camera_rearcam = 0
    else:
        overlay.layer = 3
        if rearcamoverlay == "false":
            overlay.alpha = 0
        else:
            overlay.alpha = 64
        camera_rearcam = 1
        camera.start_preview()

UDP_IP = "127.0.0.1"
UDP_PORT = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT))

while exit != 1:
    if (start_recording == 1):
        start_recording = 0
        data = "Record"
        print("start_recording = 0")
    else:
        dataudp, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        try:
            data = str(dataudp.rstrip('\x00').decode('utf-8'))
        except:
            data = str(dataudp.decode('utf-8'))

    print("RPi-Camera: received command: " + data)

    if data == "Status":
        updateStatus()

    if data == "Foreground":
        if camera_preview == 0:
            cameraStartPreview()
            camera_preview = 1
            print("RPi-Camera: Switching to foreground...")

    if data == "Background":
        if camera_preview == 1:
            camera.stop_preview()
            camera_preview = 0
            overlay.layer = 0
            overlay.alpha = 0
            camera_rearcam = 0
            print("RPi-Camera: Switching to background...")

    if data == "AWB":
        if camera_awbmode == "auto":
            camera.awb_mode = 'shade'
            camera_awbmode = "shade"
        else:
            camera.awb_mode = 'auto'
            camera_awbmode = "auto"
            updateStatus()

    if data == "EXP":
        if camera_expmode == "auto":
            camera.exposure_mode = 'nightpreview'
            camera_expmode = "night"
        else:
            camera.exposure_mode = 'auto'
            camera_expmode = "auto"
            updateStatus()

    if data == "Record":

        if free <= 128:
            camera.annotate_text = 'Recording not possible - Storage device is full.'
        else:
            if camera_recording == 0:
                if loop_recording == 0:
                    if camera.api == "picamera":
                        camera.annotate_background = picamera.Color('black')
                    camera.annotate_text = "RPi-Dashcam - " + dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                    camera.start_recording(
                    recordpath + 'RPIDC_' + dt.datetime.now().strftime('%d%m%Y') + '_' + dt.datetime.now().strftime('%H%M%S') + '.h264')
                    camera_recording = 1
                    updateStatus()
                else:
                    if camera.api == "picamera":
                        camera.annotate_background = picamera.Color('black')
                    camera.annotate_text = "RPi-Dashcam - " + dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                    camera.start_recording(recordpath + 'RPIDC_' + dt.datetime.now().strftime('%d%m%Y') + '.h264')
                    camera_recording = 1
                    updateStatus()

    if data == "Stop":
        if camera_recording == 1:
            camera.stop_recording()
            camera_recording = 0
            updateStatus()

    if data == "SaveEvent":
        savingfile = 1
        source = recordpath + 'RPIDC_' + dt.datetime.now().strftime('%d%m%Y') + '.h264'
        destination = storagepath + 'EVENTS/RPIDC_SAVED_EVENT_' + dt.datetime.now().strftime(
            '%d%m%Y') + '_' + dt.datetime.now().strftime('%H%M%S') + '.h264'
        os.system("cp " + source + " " + destination)
        time.sleep(1)
        savingfile = 0

    if "YCorrection" in data:
        splitposy = data.split(',')
        respreview_y_correction = int(splitposy[1])

    if "PosYUp" in data:
        respreview_y_correction = respreview_y_correction - 1
        os.system("echo " + str(respreview_y_correction) + " > /tmp/ycorrection")
        cameraStartPreview()

    if "PosYDown" in data:
        respreview_y_correction = respreview_y_correction + 1
        os.system("echo " + str(respreview_y_correction) + " > /tmp/ycorrection")
        cameraStartPreview()

    if "ZoomPlus" in data:
        respreview_zoom = respreview_zoom + 1
        os.system("echo " + str(respreview_zoom) + " > /tmp/zoomlevel")
        cameraStartPreview()

    if "ZoomMinus" in data:
        respreview_zoom = respreview_zoom - 1
        os.system("echo " + str(respreview_zoom) + " > /tmp/zoomlevel")
        cameraStartPreview()

    if "Path" in data:
        splitpath = data.split(',')
        recordpath = splitpath[1]
        free = freespace(recordpath)

    if "Rotation" in data:
        splitrotation = data.split(',')
        rotation = str(splitrotation[1])
        if rotation == "0":
            camera.rotation = '0'
        if rotation == "1":
            camera.rotation = '90'
        if rotation == "2":
            camera.rotation = '180'
        if rotation == "3":
            camera.rotation = '270'

    if "AWB" in data:
        splitawb = data.split(',')
        awb = str(splitawb[1])
        if awb == "0":
            camera.awb_mode = 'off'
        if awb == "1":
            camera.awb_mode = 'auto'
        if awb == "2":
            camera.awb_mode = 'sunlight'
        if awb == "3":
            camera.awb_mode = 'cloudy'
        if awb == "4":
            camera.awb_mode = 'shade'
        if awb == "5":
            camera.awb_mode = 'tungsten'
        if awb == "6":
            camera.awb_mode = 'fluorescent'
        if awb == "7":
            camera.awb_mode = 'incandescent'
        if awb == "8":
            camera.awb_mode = 'flash'
        if awb == "9":
            camera.awb_mode = 'horizon'

    if "EXP" in data:
        splitexp = data.split(',')
        exp = str(splitexp[1])
        if exp == "0":
            camera.exposure_mode = 'off'
        if exp == "1":
            camera.exposure_mode = 'auto'
        if exp == "2":
            camera.exposure_mode = 'night'
        if exp == "3":
            camera.exposure_mode = 'nightpreview'
        if exp == "4":
            camera.exposure_mode = 'backlight'
        if exp == "5":
            camera.exposure_mode = 'spotlight'
        if exp == "6":
            camera.exposure_mode = 'sports'
        if exp == "7":
            camera.exposure_mode = 'snow'
        if exp == "8":
            camera.exposure_mode = 'beach'
        if exp == "9":
            camera.exposure_mode = 'verylong'
        if exp == "10":
            camera.exposure_mode = 'fixedfps'
        if exp == "11":
            camera.exposure_mode = 'antishake'
        if exp == "12":
            camera.exposure_mode = 'fireworks'

    if "RearcamMode" in data:
        splitoverlay = data.split(',')
        rearcammode = str(splitoverlay[1])
        if rearcammode == "true":
            print("RPi-Camera: RearcamMode activated...")
        else:
            print("RPi-Camera: RearcamMode deactivated...")

    if "RearcamOverlay" in data:
        splitoverlay = data.split(',')
        rearcamoverlay = str(splitoverlay[1])
        if rearcamoverlay == "true":
            print("RPi-Camera: RearcamMode Overlay activated...")
        else:
            print("RPi-Camera: RearcamMode Overlay deactivated...")

    if "RecordMode" in data:
        splitrecordmode = data.split(',')
        recordmode = str(splitrecordmode[1])
        recordtimeloop = str(splitrecordmode[2])
        if recordtimeloop == "0":
            recordtime = 300
        if recordtimeloop == "1":
            recordtime = 600
        if recordtimeloop == "2":
            recordtime = 900
        if recordtimeloop == "3":
            recordtime = 1800
        if recordtimeloop == "4":
            recordtime = 3600
        if recordmode == "true":
            loop_recording = 1
            print("RPi-Camera: Recording in loop activated...")
        else:
            loop_recording = 0
            print("RPi-Camera: Recording in loop deactivated...")

    if "HFlip" in data:
        splitflip = data.split(',')
        hflip = str(splitflip[1])
        if hflip == "true":
            camera.hflip = True
            print("RPi-Camera: Flip image horizontally...")
        else:
            camera.hflip = False

    if "VFlip" in data:
        splitflip = data.split(',')
        vflip = str(splitflip[1])
        if vflip == "true":
            camera.vflip = True
            print("RPi-Camera: Flip image vertically...")
        else:
            camera.vflip = False

    if "Exit" in data:
        exit = 1
        break

sock.close()
camera.close()
