#-*- coding: utf-8 -*-
import cv2
import numpy as np
import pytesseract
from PIL import Image


def apply_mask(frame, mask):
    """Apply binary mask to frame, return masked image.
    """
    return cv2.bitwise_and(frame, frame, mask=mask)
def main():
    import os
    result_path ='C:\\'

    if os.path.isdir(result_path):
        os.mkdir('C:\\result')
    path = "color.txt"

    f= open(path, "r")
    text = f.readlines()

    strdata = text[0].split(' ')

    frame = 'test.jpg'

    frame: np.ndarray = cv2.imread(frame)
    original = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    detect = cv2.inRange(frame, (int(strdata[0]), int(strdata[1]), int(strdata[2])),
                         (int(strdata[3]), int(strdata[4]), int(strdata[5])))


    contours, _ = cv2.findContours(detect, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    sorted_cnt = []

    for cnt in contours:
        cnt_len = cv2.arcLength(cnt, True)
        cnt_ = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)

        if cv2.contourArea(cnt_) > 1000:
            sorted_cnt.append(cnt)
    empty = np.zeros((original.shape[0], original.shape[1]))

    original2 = original.copy()

    empty = cv2.fillPoly(empty, sorted_cnt, color=(255, 255, 255))

    # 변경하면 안됨.
    original[empty != 255] = 255


    empty_resize = cv2.resize(empty, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_AREA)
    original_resize = cv2.resize(original, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_AREA)

    cv2.imshow("111",empty_resize)
    cv2.imshow("result", original_resize)
    cv2.imwrite('result/result.jpg', original)

    kernel = np.ones((3, 3), np.uint8)
    empty = cv2.dilate(empty, kernel, iterations=5)  # // make dilation image
    original_gray = cv2.cvtColor(original2, cv2.COLOR_RGB2GRAY)
    original_gray[empty != 255] = 255

    ret, original_thresh = cv2.threshold(original_gray, 100, 255, cv2.THRESH_BINARY_INV)

    # tesseract 설치 경로
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

    img_new = Image.fromarray(original_thresh)

    text = pytesseract.image_to_string(img_new, lang='kor+eng')
    print(text)

    original_gray_resize = cv2.resize(original_gray, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_AREA)
    empty_resize = cv2.resize(empty, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_AREA)
    original_thresh_resize = cv2.resize(original_thresh, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_AREA)

    cv2.imshow("222",empty_resize)
    cv2.imshow("result2", original_gray_resize)
    cv2.imshow("thresh1", original_thresh_resize)

    cv2.waitKey(0)



if __name__ == '__main__':
    main()