import cv2
import numpy as np

img = cv2.imread("obj1__0.png", cv2.IMREAD_GRAYSCALE)
#img = cv2.imread("obj2__255.png", cv2.IMREAD_GRAYSCALE)

sift = cv2.xfeatures2d.SIFT_create()
surf = cv2.xfeatures2d.SURF_create()

kp = sift.detect(img, None)
keypoints, descriptors = sift.detectAndCompute(img, None)
keypoints_surf, descriptors_surf = surf.detectAndCompute(img, None)
img = cv2.drawKeypoints(img, kp, None)
desc = []
for i in range(len(descriptors)):   # flatten
    for j in range(len(descriptors[0])):
        desc.append(descriptors[i][j])

if len(desc) >= 40:
    desc = desc[:20]


print("KeyPoints ******************************************", keypoints)
print("Descriptor -----------------------------------------", descriptors)
print("Updated -----------------------", desc)



print(len(descriptors), len(descriptors[0]))
# keypoints, descriptors = sift.detectAndCompute(img, None)

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()