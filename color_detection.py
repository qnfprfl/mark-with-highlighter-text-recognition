#-*- coding: utf-8 -*-
import cv2
import numpy as np

def apply_mask(frame, mask):
    """Apply binary mask to frame, return masked image.
    """
    return cv2.bitwise_and(frame, frame, mask=mask)

def main():
    import os
    result_path =' result'

    if os.path.isdir(result_path):
        os.mkdir('result')
    path = "color.txt"

    # 파일 읽어오기
    f= open(path, "r")
    text = f.readlines()

    strdata = text[0].split(' ')

    frame = 'images/test.jpg'

    frame: np.ndarray = cv2.imread(frame)
    original = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    detect = cv2.inRange(frame, (int(strdata[0]), int(strdata[1]), int(strdata[2])),
                         (int(strdata[3]), int(strdata[4]), int(strdata[5])))

    # contour 찾기
    contours, _ = cv2.findContours(detect, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    sorted_cnt = []
    # 디텍션 이외의 정보 지우기
    for cnt in contours:
        cnt_len = cv2.arcLength(cnt, True)
        cnt_ = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
        # contour에서 일정 면적 이상만 저장하여 나중에 그림
        if cv2.contourArea(cnt_) > 1000:
            sorted_cnt.append(cnt)
    empty = np.zeros((original.shape[0], original.shape[1]))

    # Contour 채우기
    empty = cv2.fillPoly(empty, sorted_cnt, color=(255, 255, 255))

    # Contour 제외 색 채우기
    original[empty != 255] = 0
    cv2.imshow("RESULT", original)
    cv2.imwrite('result/result.jpg', original)
    cv2.waitKey(0)







if __name__ == '__main__':
    main()

