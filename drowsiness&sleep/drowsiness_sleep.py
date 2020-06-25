# USAGE
# python video_facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat
# python video_facial_landmarks.py --shape-predictor shape_predictor_68_face_landmarks.dat --picamera 1
# python detect_drowsiness.py --shape-predictor shape_predictor_68_face_landmarks.dat --alarm alarm.wav

# 졸 때랑 하품할때.
# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import datetime
import math
import playsound
import argparse
import imutils
import time
import dlib
import cv2
import csv
import numpy as np
 

def sound_alarm(path):
	# play an alarm sound
	playsound.playsound(path)

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])

	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)

	# return the eye aspect ratio
	return ear
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-r", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-a", "--alarm", type=str, default="",
	help="path alarm .WAV file")
ap.add_argument("-w", "--webcam", type=int, default=0,
	help="index of webcam on system")
args = vars(ap.parse_args())

#eye detection
EYE_AR_THRESH = 0.19
EYE_AR_CONSEC_FRAMES = 60

COUNTER = 0
ALARM_ON = False

print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])


# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# start the video stream thread
print("[INFO] starting video stream thread...")
vs = VideoStream(src=args["webcam"]).start()
time.sleep(1.0)

print("[INFO] loading facial landmark predictor...")

print("[INFO] camera sensor warming up...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)
i = 0
j = 0
c = 0

C = 0
while True:
	frame = vs.read()
	frame = imutils.resize(frame, width=600)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	nose_image = cv2.imread("stop-watch.png")
	pin_image = cv2.imread("clothespin.png")

	C += 1
	if C==100:
		C = 0

	# detect faces in the grayscale frame, 얼굴 인식하는 거. 
	rects = detector(gray, 0)

	# loop over the face detections
	for rect in rects:
		shape = predictor(gray, rect)
		shape2 = face_utils.shape_to_np(shape) #numpy로 저장

		# csv 파일로 좌표 저장, 1~17:턱, 18~27:눈썹, 28~36:코, 37~48:눈, 
		if i==0:
			csvfile = open("mouth.csv", "a")
			csvwriter = csv.writer(csvfile)

		cv2.putText(frame, "hapum: {:.2f}".format(shape2[66, 1] - shape2[62, 1]), (10, 100), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 0, 0), 2)

		# 67-63 값 차이가 30 넘고, j>5초
		if (shape2[66, 1] - shape2[62, 1]) > 22 :
			c += 1
			if c > 29: #2초 동안 하품할 경우.
				cv2.putText(frame, " CHEER UP!!", (300, 150), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (250, 250, 250), 2)
		else :
			c = 0

		#shape2 (68,2) -> (1,136)로 바꿔주기.
		shape3 = np.reshape(shape2, (1,136))

		if j % 29==0:
			for row in shape3:
				csvwriter.writerow(row)
	
		# loop over the (x, y)-coordinates for the facial landmarks
		# and draw them on the image
		# for (x, y) in shape2:
		#  	cv2.circle(frame, (x, y), 1, (0, 0, 0), -1)
        
		top_nose = (shape.part(29).x, shape.part(29).y)
		center_nose = (shape.part(30).x, shape.part(30).y)
		left_nose = (shape.part(31).x, shape.part(31).y)
		right_nose = (shape.part(35).x, shape.part(35).y)

		nose_width = int(math.hypot(left_nose[0] - right_nose[0], left_nose[1] - right_nose[1])*1.7)
		nose_height = int(nose_width * 0.77)

		top_left = (int (center_nose[0]-nose_width/2), 
					int(center_nose[1] - nose_height/2))
		bottom_right = (int(center_nose[0]+nose_width/2),
					int(center_nose[1]+nose_height/2))

		nose_pig = cv2.resize(nose_image, (nose_width, nose_height))
		nose_pig_gray = cv2.cvtColor(nose_pig, cv2.COLOR_BGR2GRAY)
		_, nose_mask = cv2.threshold(nose_pig_gray, 25, 255, cv2.THRESH_BINARY_INV)

		nose_area = frame[top_left[1]: top_left[1]+nose_height,
						top_left[0]: top_left[0]+nose_width]
		nose_area_no_nose = cv2.bitwise_and(nose_area, nose_area, mask=nose_mask)
		final_nose = cv2.add(nose_area_no_nose, nose_pig)
		
		##################
		left_eye_l = (shape.part(37).x, shape.part(37).y)
		left_eye_r = (shape.part(40).x, shape.part(40).y)
		right_eye_l = (shape.part(43).x, shape.part(43).y)
		right_eye_r = (shape.part(46).x, shape.part(46).y)

		left_eye_width = int((left_eye_r[0]-left_eye_l[0])*2)
		right_eye_width = int((right_eye_r[0]-right_eye_l[0])*2)
		pin_height = int(left_eye_width * 3)

		tl = (int(left_eye_l[0]), int(left_eye_l[1]-pin_height))
		br = (int(left_eye_r[0]), int(left_eye_r[1]))
		tl2 = (int(right_eye_l[0]), int(right_eye_l[1]-pin_height))
		br2 = (int(right_eye_r[0]), int(right_eye_r[1]))

		left_pin = cv2.resize(pin_image, (left_eye_width, pin_height))
		right_pin = cv2.resize(pin_image, (right_eye_width, pin_height))
		left_pin_gray = cv2.cvtColor(left_pin, cv2.COLOR_BGR2GRAY)
		right_pin_gray = cv2.cvtColor(right_pin, cv2.COLOR_BGR2GRAY)
		_, left_pin_mask = cv2.threshold(left_pin_gray, 25, 255, cv2.THRESH_BINARY_INV)
		_, right_pin_mask = cv2.threshold(right_pin_gray, 25, 255, cv2.THRESH_BINARY_INV)

		pin_area = frame[tl[1]:tl[1]+pin_height, tl[0]:tl[0]+left_eye_width]
		pin_area_no_eye = cv2.bitwise_and(pin_area, pin_area, mask=left_pin_mask)
		pin_area2 = frame[tl2[1]:tl2[1]+pin_height, tl2[0]:tl2[0]+right_eye_width]
		pin_area_no_eye2 = cv2.bitwise_and(pin_area2, pin_area2, mask=right_pin_mask)
		final_left_pin = cv2.add(pin_height, left_pin)
		final_right_pin = cv2.add(pin_height, right_pin)

		# frame[tl[1]:tl[1]+pin_height, tl[0]:tl[0]+left_eye_width] = final_left_pin
		# frame[tl2[1]:tl2[1]+pin_height, tl2[0]:tl2[0]+right_eye_width] = final_right_pin
		#####################

		leftEye = shape2[lStart:lEnd]
		rightEye = shape2[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)
		ear = (leftEAR + rightEAR)/2.0

		# compute the convex hull for the left and right eye, then
		# visualize each of the eyes
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		# cv2.drawContours(frame, [leftEyeHull], -1, (0,0,0), 1)
		# cv2.drawContours(frame, [rightEyeHull], -1, (0,0,0), 1)
		
		if ear < EYE_AR_THRESH:
			COUNTER += 1

			# if the eyes were closed for a sufficient number of
			# then sound the alarm

			if COUNTER >= EYE_AR_CONSEC_FRAMES:
				if C>=50:
					frame[top_left[1]: top_left[1]+nose_height,
							top_left[0]: top_left[0]+nose_width] = final_nose
				else:
					frame[tl[1]:tl[1]+pin_height, tl[0]:tl[0]+left_eye_width] = final_left_pin
					frame[tl2[1]:tl2[1]+pin_height, tl2[0]:tl2[0]+right_eye_width] = final_right_pin
				
				# if the alarm is not on, turn it on
				if not ALARM_ON:
					ALARM_ON = True

					if args["alarm"] != "":
						t = Thread(target=sound_alarm, args=(args["alarm"],))
						t.deamon = True
						t.start()

				# draw an alarm on the frame
				cv2.putText(frame, "CHEER UP!", (300, 150), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (250,250,250), 2)

		# otherwise, the eye aspect ratio is not below the blink
		# threshold, so reset the counter and alarm
		else:
			COUNTER = 0
			ALARM_ON = False

		cv2.putText(frame, "EAR: {:.2f}".format(ear), (10, 130),
			cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 0, 0), 2)
		cv2.putText(frame, "COUNTER: {:d}".format(COUNTER), (10, 160),
			cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 0, 0), 2)
	  
	# show the frame
	cv2.imshow("Frame", frame)
	# cv2.imshow("Nose pig", nose_image)
    
	j += 1

	key = cv2.waitKey(1) & 0xFF
	
	if key == ord("d"):
		csvfile2 = open("LM_2.csv", "a")
		csvwriter = csv.writer(csvfile2)
		i = 1
		
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

csvfile.close()
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
