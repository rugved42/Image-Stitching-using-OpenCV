"""
Image Stitching Problem
(Due date: Nov. 9, 11:59 P.M., 2020)
The goal of this task is to stitch two images of overlap into one image.
To this end, you need to find feature points of interest in one image, and then find
the corresponding ones in another image. After this, you can simply stitch the two images
by aligning the matched feature points.
For simplicity, the input two images are only clipped along the horizontal direction, which
means you only need to find the corresponding features in the same rows to achieve image stiching.

Do NOT modify the code provided to you.
You are allowed use APIs provided by numpy and opencv, except “cv2.findHomography()” and
APIs that have “stitch”, “Stitch”, “match” or “Match” in their names, e.g., “cv2.BFMatcher()” and
“cv2.Stitcher.create()”.
"""
"""
References: 
https://docs.opencv.org/3.4/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d
https://medium.com/analytics-vidhya/image-stitching-with-opencv-and-python-1ebd9e0a6d78
https://docs.opencv.org/master/da/df5/tutorial_py_sift_intro.html
https://docs.opencv.org/master/da/d6e/tutorial_py_geometric_transformations.html
https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html

Link 1: Image Features Documentation Opencv 
Link 2: Image Stiching in details medium blog. 
Link 3: SIFT Tutorial
Link 4: Geometric Tansformations Warp Perspective Tutorial OpenCV Documentation. 
Link 5: BF Matcher OpenCV Documentation
"""
import cv2 
import matplotlib.pyplot as plt
import numpy as np
import random
import itertools
import math
import os

def match(kp1,kp2,des1,des2): 
    matches = dict()
    dis = 500
    threshold = 10
    count = 0
    while dis > threshold:
        random_s1 = random.sample(list(enumerate(des1)), 100)
        random_s2 = random.sample(list(enumerate(des2)), 100)
        for i in range(len(random_s1)): 
            for j in range(len(random_s2)): 
                dist = np.linalg.norm(random_s1[i][1] - random_s2[j][1])
                if dist < dis: 
                    kpi = kp1[random_s1[i][0]] #
                    kpj = kp2[random_s2[j][0]]
                    matches[dist] = [kpi.pt,kpj.pt]
                    dis = dist
    #                 if len(list(matches)) > 5:
    #                     print("check",list(matches)[-1],list(matches)[-4],np.abs(list(matches)[-1] - list(matches)[-4]))
                    if dis < threshold and np.abs((list(matches)[-1] - list(matches)[-4])) < 50:
                        # print("check22",list(matches)[-1],list(matches)[-4],np.abs(list(matches)[-1] - list(matches)[-4]))
                        count += 1
                        if count < 2: 
                            threshold -= 3
                        else: 
                            threshold -= 0
                        if threshold == 0: 
                            threshold += 5
                    break
            if threshold == 10 and dis < threshold: 
                dis = dis + threshold
        if count == 2 and np.abs(dis - threshold) < 1.5:
            break
            # print("dis",dis,threshold)
    sorted_matches = dict(sorted(matches.items()))
    sorted_match = dict(itertools.islice(sorted_matches.items(), 10))  
    return (sorted_match)

def solution(left_img, right_img):
    """
    :param left_img:
    :param right_img:
    :return: you need to return the result image which is stitched by left_img and right_img
    """
    left = left_img 
    right = right_img
    pts_left = []
    pts_right = []
    sift = cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(left,None)
    kp2, des2 = sift.detectAndCompute(right,None)
    sorted_match = match(kp1,kp2,des1,des2)
    print(sorted_match)
    for key in sorted_match.keys(): 
        pts_left.append(sorted_match[key][0])
        pts_right.append(sorted_match[key][1])
    pts_left = np.float32(pts_left).reshape(-1,1,2)
    pts_right = np.float32(pts_right).reshape(-1,1,2)
    M, mask = cv2.findHomography(pts_right,pts_left,cv2.RANSAC,3)
    print("Homography Matrix is: ",M)
    warped_right1 = cv2.warpPerspective(right, M, (left.shape[1]+right.shape[1],left.shape[0]))
    warped_right1[0:left.shape[0], 0:left.shape[1]] = left
    return warped_right1

if __name__ == "__main__":
    left_img = cv2.imread('left.jpg')
    right_img = cv2.imread('right.jpg')
    result_image = solution(left_img, right_img)
    if os.path.exists("results/task1_result.jpg"):
        os.remove("results/task1_result.jpg")
        print("file already existed and now removed")
    cv2.imwrite('results/task1_result.jpg',result_image)


