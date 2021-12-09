import sys
import subprocess
import cv2
import CamProbe

def clearCapture(capture):
    capture.release()
    cv2.destroyAllWindows()

def countCameras():
    n = 0
    for i in range(10):
        try:
            cap = cv2.VideoCapture(i)
            ret, frame = cap.read()
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            clearCapture(cap)
            n += 1
        except:
            clearCapture(cap)
            break
    return n



#set cam settings
x_res = 640
y_res = 480
fps = 30

#check how many USB/OpenCV cameras are plugged in
cam_list = CamProbe.probe_usb_cams()

usb_cam_cmd = []
for dev in cam_list:
    # usb_cam_cmd.append('-i')
    usb_cam_cmd.append('-i \"input_uvc.so -d {} -r {}x{} -f {}\"'.format(dev,x_res,y_res,fps))

# usb_cam_cmd = ' -i '.join(usb_cam_string)
#combine sublists to one list
# opencv_cam_cmd= [j for i in opencv_cam_cmd for j in i]

#check if the raspi cam is installed and active, build the raspicam input string
if 'detected=1' in subprocess.run(['/opt/vc/bin/vcgencmd', 'get_camera'], capture_output=True, text=True).stdout:
    print('Raspicam connected, {} USB Cameras connected, launching {} streams'.format(len(cam_list),len(cam_list)+1))
    raspi_cam_cmd = '-i \"input_raspicam.so -x {} -y {} -fps {}\"'.format(x_res,y_res,fps)

elif 'detected=0' in subprocess.run(['/opt/vc/bin/vcgencmd', 'get_camera'], capture_output=True, text=True).stdout:
    raspi_cam_cmd = ''
    print('{} USB Cameras connected, launching {} streams'.format(len(cam_list),len(cam_list)))
else:
    raise IOError('no good answer for raspicam check, exiting')

#construct input args


#construct the output string
output_cmd = ['-o \"output_http.so -p 8090 -w ./www\"']


streamer_cmd = ['./mjpg_streamer']+usb_cam_cmd+output_cmd
streamer_cmd = ' '.join(streamer_cmd)


print(streamer_cmd)
subprocess.run(streamer_cmd,shell=True,cwd='/home/pi/mjpg-streamer-master/mjpg-streamer-experimental')