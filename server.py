import socket
import time
import cv2
import scipy.io as sio
import numpy as np
import picamera

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,800)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,600)
s = socket.socket()
host = '127.0.0.1'
port = 13500
addr = (host,port)
s.bind(addr)
s.listen(5)
mode = "listen"
box = np.array([[]])
print addr
while not mode == "end":
    conn, clientAdd = s.accept()
    cmdString = conn.recv(1024)
    cmdBox = cmdString.split('*')
    print cmdBox
    cmdType = cmdBox[0]
    if cmdType == 'getpic':
        ret, img = cam.read()
        data = cv2.imencode('.jpg',img)[1]
        conn.send(data.tobytes())
    elif cmdType == "classify":
        label = np.uint8([[cmdBox[1]]])
        conn.send('ack')
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        imdata = gray.reshape((1,gray.size))
        prevdata = box[-1,:-1]
        if np.array_equal(imdata[0],prevdata):
            conn.close()
            continue
        newdata = np.append(imdata,label,1)
        if box.size == 0:
            box = newdata
        else:
            box = np.append(box,newdata,0)
        print box
    conn.close()
cam.release()
