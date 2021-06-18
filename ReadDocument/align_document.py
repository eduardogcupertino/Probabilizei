# import the necessary packages
from pyimagesearch.align_images import align_images
from collections import namedtuple
import pytesseract
import numpy as np
import argparse
import imutils
import cv2

def cleanup_text(text):
	# strip out non-ASCII text so we can draw the text on the image
	# using OpenCV
	return "".join([c if ord(c) < 128 else "" for c in text]).strip()

# create a named tuple which we can use to create locations of the
# input document which we wish to OCR
OCRLocation = namedtuple("OCRLocation", ["id", "bbox",
	"filter_keywords"])

# define the locations of each area of the document we wish to OCR
OCR_LOCATIONS = [
	OCRLocation("step1_first_name", (265, 237, 751, 106),
		["middle", "initial", "first", "name"]),
	OCRLocation("step1_last_name", (1020, 237, 835, 106),
		["last", "name"]),
	OCRLocation("step1_address", (265, 336, 1588, 106),
		["address"]),
	OCRLocation("step1_city_state_zip", (265, 436, 1588, 106),
		["city", "zip", "town", "state"]),
	OCRLocation("step5_employee_signature", (319, 2516, 1487, 156),
		["employee", "signature", "form", "valid", "unless",
		 	"you", "sign"]),
	OCRLocation("step5_date", (1804, 2516, 504, 156), ["date"]),
	OCRLocation("employee_name_address", (265, 2706, 1224, 180),
		["employer", "name", "address"]),
	OCRLocation("employee_ein", (1831, 2706, 448, 180),
		["employer", "identification", "number", "ein"]),
]

# load the input image and template from disk
print("[INFO] loading images...")
image = cv2.imread("images/input.jpg")
template = cv2.imread("images/Modelo.jpg")
# align the images
print("[INFO] aligning images...")
aligned = align_images(image, template, debug=True)

# initialize a results list to store the document OCR parsing results
print("[INFO] OCR'ing document...")
parsingResults = []
# loop over the locations of the document we are going to OCR
for loc in OCR_LOCATIONS:
	# extract the OCR ROI from the aligned image
	(x, y, w, h) = loc.bbox
	roi = aligned[y:y + h, x:x + w]
	# OCR the ROI using Tesseract
	rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
	text = pytesseract.image_to_string(rgb)