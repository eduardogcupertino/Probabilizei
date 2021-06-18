import cv2
import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
from PIL import Image

img = Image.open(r'C:\Users\gamac\Desktop\text.png')

config = ("-l eng --oem 1 --psm 7")
text = tess.image_to_string(img, config=config)
print("resultado: ")
print(text)