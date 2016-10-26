import PiCamera, subprocess, sys

process = subprocess.Popen( ["cvlc", "v4l2:///dev/video0", "--sout", "#transcode{vcodec=MJPG,vb=500,width=352,height=288}:duplicate{dst=std{access=http{mime=multipart/x-mixed-replace;boundary=--7b3cc56e5f51db803f790dad720ed50a},mux=mpjpeg,dst=:9090/webcam.mjpg}}"]
                          )

print("Video capture started")





# videoProcess = None
# count = 0

# def turnOnWebcam(counter):
#   videoProcess = subprocess.Popen(["cvlc", "v4l2:///dev/video" + str(counter), "--sout", "#transcode{vcodec=MJPG,vb=500,width=352,height=288}:duplicate{dst=std{access=http{mime=multipart/x-mixed-replace;boundary=--7b3cc56e5f51db803f790dad720ed50a},mux=mpjpeg,dst=:9090/webcam.mjpg}}"], stdout=subprocess.PIPE)

#   print("Starting video capture on /dev/video" + str(counter))

#   for line in videoProcess.stdout:
#     print(videoProcess.stdout.read())
#     if "v4l2 demux error" in line:
#       videoProcess.kill()
#       count += 1
#       turnOnWebcam(count)
#       break
#     elif count == 2:
#       videoProcess.kill()
#       print("Video capture can't be started")
#       break

# turnOnWebcam(count)





# with open("test.avi", "rb") as infile:
#     p = subprocess.Popen(["ffmpeg", "-i", "-", "-f", "matroska", "-vcodec", "mpeg4", "-strict", "experimental", "-"], stdin=infile, stdout=subprocess.PIPE)
#     while True:
#         data = p.stdout.read(1024)
#         if len(data) == 0:
#             break
#         # do something with data...
#         print(data)
#     print p.wait() # should have finisted anyway

# webcam = cv2.VideoCapture(0)
# while (webcam.isOpened()):
#     #read() return a tuple (True/False, frame/None)
#     returnValue, frame = webcam.read()
#     if (returnValue):
#         sys.stdout.write(frame.tostring())
#     else:
#         break
# webcam.release
