# not needed
# from PIL import Image
import pytesseract
import cv2
# we might need for speed
import imutils
from imutils.video import VideoStream


def ocr_core(filename):
    text = pytesseract.image_to_string(Image.open(filename))
    return text

#print(ocr_core('example.png'))

# see image_to_data
# https://stackoverflow.com/questions/20831612/getting-the-bounding-box-of-the-recognized-words-using-python-tesseract
cap = cv2.VideoCapture(0)

while True:
	# read image ----
	ret, img = cap.read()
	if ret:
		# process image ---
		# if needed grayscale
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# blur
		gray = cv2.GaussianBlur(gray, (3,3), 0)
		img2 = cv2.GaussianBlur(img, (31,31), 0)
		# if needed do some sort of edge detection to reduce ROI
		mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
		# get ROI to work and crop image
		# invert the mask
		#mask = 255 - mask

		condition = False
		# only call tesseract if needed
		if condition:
			print(pytesseract.image_to_string(img))
			# feed to tesseract
			d = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
			# there might be good stuff inside here --> print(d.keys())
			n_boxes = len(d['level'])

			for i in range(n_boxes):
			    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
			    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

		cv2.imshow('img', img)
		cv2.imshow("mask", mask)
		cv2.imshow("img-blur", img2)
		k = cv2.waitKey(1)
		if k == ord("q"):
			break

cv2.destroyAllWindows()

