#-*- coding: utf-8 -*-
import cv2
import numpy as np

def nothing(a):

    pass


def trackbar():
    window_name = "COLOR_DETECTION"

    # 트랙바 담을 윈도우 생성
    cv2.namedWindow(window_name)

    # 트랙바 생성
    cv2.createTrackbar("lower_h", window_name, 0, 255, nothing)
    cv2.createTrackbar("lower_s", window_name, 0, 255, nothing)
    cv2.createTrackbar("lower_v", window_name, 0, 255, nothing)
    cv2.createTrackbar("upper_h", window_name, 120, 255, nothing)
    cv2.createTrackbar("upper_s", window_name, 120, 255, nothing)
    cv2.createTrackbar("upper_v", window_name, 120, 255, nothing)

    while True:

        frame = 'images/test.jpg'

        frame = cv2.imread(frame)
        original = frame.copy()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # threshold 값 트랙바에서 찾기
        lower_h = cv2.getTrackbarPos("lower_h", window_name)
        lower_s = cv2.getTrackbarPos("lower_s", window_name)
        lower_v = cv2.getTrackbarPos("lower_v", window_name)
        upper_h = cv2.getTrackbarPos("upper_h", window_name)
        upper_s = cv2.getTrackbarPos("upper_s", window_name)
        upper_v = cv2.getTrackbarPos("upper_v", window_name)


        detect = cv2.inRange(frame, (lower_h, lower_s, lower_v), (upper_h, upper_s, upper_v))

        # contour 찾습니다.
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

        # Contour 안 채우기
        empty = cv2.fillPoly(empty, sorted_cnt, color=(255, 255, 255))

        # Contour 제외 색 채우기
        original[empty != 255] = 0
        cv2.imshow(window_name, original)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
def apply_mask(frame, mask):
    """Apply binary mask to frame, return masked image.
    """
    return cv2.bitwise_and(frame, frame, mask=mask)
def main():
    import os
    trackbar()

if __name__ == '__main__':
    main()

