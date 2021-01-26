import cv2 
import matplotlib.pyplot as plt
import numpy as np
import random
import itertools
import math
import os

"""
References: 

https://docs.opencv.org/3.4/d4/d70/tutorial_hough_circle.html
https://docs.opencv.org/3.4/da/d5c/tutorial_canny_detector.html
https://docs.opencv.org/3.4/d5/db5/tutorial_laplace_operator.html
https://docs.opencv.org/master/d6/d10/tutorial_py_houghlines.html
https://docs.opencv.org/master/dc/da5/tutorial_py_drawing_functions.html

Link 1: Hough Circles Opencv Docs and Tutorial.   [OpenCV Documentation]
Link 2: Canny Detector Opencv Documentation       [OpenCV Documentation]
Link 3: Laplacian Detector Opencv Documentation    [OpenCV Documentation]
Link 4: Hough lines tutorial                        [OpenCV Documentation]
Link 5: Cv2 Lines Tutorial                           [OpenCV Documentation]
"""

def blue_lines():
    if os.path.exists("results/blue_lines.txt"):
        os.remove("results/blue_lines.txt")
        print("file already existed and now removed")
    if os.path.exists("results/blue_lines.jpg"):
        os.remove("results/blue_lines.jpg")
    hough = cv2.imread("Hough.png")
    hough_gray = cv2.cvtColor(hough, cv2.COLOR_BGR2GRAY)
    hough_canny = cv2.Canny(hough_gray,20,55,3)
    plt.imshow(hough_canny)
    lines = cv2.HoughLines(hough_canny, 1, np.pi / 180, 57, None, 50, 10)
    hough_canny_c = cv2.cvtColor(hough_canny,cv2.COLOR_GRAY2BGR)
    rho_old = -1000
    k = 0
    rho_all = [0]
    exist = False
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            exist = False
            if theta >= 2.5132741 and theta <= 2.52 and np.abs(rho-rho_old) >= 25:
    #             print(rho)
                for r in rho_all:
    #                 print("check",np.abs(r-rho))
                    if np.abs(r-rho) < 45:
                        exist = True
                if exist == False:
                    rho_all.append(rho)
                    a = math.cos(theta)
                    b = math.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    pt1 = (int(x0 + 500*(-b)), int(y0 + 500*(a)))
                    pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                    print(pt1,pt2,rho,theta)
                    k = k + 1
                    f = open("results/blue_lines.txt", "a")
                    f.write("Line {} :- rho {}, theta {} \n".format(k,rho,theta))
                    f.close()
                    cv2.line(hough, pt1, pt2, (255,0,0), 2, cv2.LINE_AA)
                    rho_old = rho
    cv2.imwrite('results/blue_lines.jpg',hough)
    #                 exist = False
    #         if k == 8:
    #             break

def red_lines():
    if os.path.exists("results/red_lines.txt"):
        os.remove("results/red_lines.txt")
        print("file already existed and now removed")
    if os.path.exists("results/red_lines.jpg"):
        os.remove("results/red_lines.jpg")
    hough = cv2.imread("Hough.png")
    hough_gray = cv2.cvtColor(hough, cv2.COLOR_BGR2GRAY)
    hough_canny = cv2.Canny(hough_gray,20,55,3)
    plt.imshow(hough_canny)
    lines = cv2.HoughLines(hough_canny, 1, np.pi / 180, 57, None, 50, 10)
    hough_canny_c = cv2.cvtColor(hough_canny,cv2.COLOR_GRAY2BGR)
    rho_old = -1000
    k = 0
    rho_all = [0]
    exist = False
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            exist = False
            if theta >= 3 and theta <= 3.13 and np.abs(rho-rho_old) >= 25:
    #                 print(rho)
                for r in rho_all:
    #                 print("check",np.abs(r-rho))
                    if np.abs(r-rho) < 100:
                        exist = True
                if exist == False:
                    rho_all.append(rho)
                    a = math.cos(theta)
                    b = math.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    pt1 = (int(x0 + 500*(-b)), int(y0 + 500*(a)))
                    pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                    print(pt1,pt2,rho,theta)
                    k = k + 1
                    f = open("results/red_lines.txt", "a")
                    f.write("Line {} :- rho {}, theta {} \n".format(k,rho,theta))
                    f.close()
                    cv2.line(hough, pt1, pt2, (0,0,255), 2, cv2.LINE_AA)
                    rho_old = rho
    cv2.imwrite('results/red_lines.jpg',hough)
    #                 exist = False
    #         if k == 3:
    #             break

def circles():
    if os.path.exists("results/coins.txt"):
        os.remove("results/coins.txt")
        print("file already existed and now removed")
    if os.path.exists("results/coins.jpg"):
        os.remove("results/coins.jpg")
    hough = cv2.imread("Hough.png")
    hough_gray = cv2.cvtColor(hough, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(hough_gray, 5)
    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows/10,
                               param1=100, param2=20,
                               minRadius=8, maxRadius=30)
    print(circles)
    k = 0
    for circle in circles[0,:]:
        f = open("results/coins.txt", "a")
        k = k + 1
        f.write("Circle {} :- Center:x {}, Center:y {}, radius {} \n".format(k,circle[0],circle[1],circle[2]))
        f.close()
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv2.circle(hough, center, i[2], (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv2.circle(hough, center, radius, (255, 0, 255), 3)
    cv2.imwrite('results/coins.jpg',hough)
    # plt.imshow(hough)

if __name__ == "__main__":
    blue_lines()
    red_lines()
    circles()
    pass