import cv2
import subprocess

def clearCapture(capture):
    capture.release()
    cv2.destroyAllWindows()


def collate_usb_video_devices():
    """
    Runs the video 4 linux command to list all video devices
    returns a superlist of lists containing the webcam and video devices
    """

    cmd = subprocess.run(['v4l2-ctl', '--list-devices'], capture_output=True, text=True).stdout
    devlist = [block.split('\n') for block in cmd.split('\n\n')]

    return [sublist for sublist in devlist for item in sublist if 'usb' in item]

def probe_usb_cams():
    """
    uses opencv-python to probe the connected usb camera devices by attempting to obtain one frame. 
    if successful, the returned list is of the valid dev addresses
    """
    # strip the listed devices from bash command
    webcam_device_list=[[item.strip() for item in sublist[1:] if 'video' in item] for sublist in collate_usb_video_devices()]
    # dissolve the superlist into a single list of /dev/video addresses
    device_list = [j for i in webcam_device_list for j in i]

    #attempt to capture from each dev address, if successful, append to capture list
    capture_list = []
    for device in device_list:
        try:
            cap = cv2.VideoCapture(device,cv2.CAP_V4L2)
            ret, frame = cap.read()
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            clearCapture(cap)
            capture_list.append(device)
        except:
            clearCapture(cap)
            # break
    return capture_list