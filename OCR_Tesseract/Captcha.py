# importacao da biblioteca do opencv
import cv2

# le a imagem
image = cv2.imread('images/infra_gerar_captcha.png')

# transforma ela de colorida (RGB) para tons de cinza
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

# aplica o thresholding
for thresh in [cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV, cv2.THRESH_TRUNC, cv2.THRESH_TOZERO, cv2.THRESH_TOZERO_INV]:
    # o segundo parâmetro, 127, é ignorado
    (_, bw) = cv2.threshold(gray, 127, 255, thresh | cv2.THRESH_OTSU)