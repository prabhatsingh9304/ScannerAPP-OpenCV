import cv2
import numpy as np
import sys
#put corner point in anticlockwise like x1 then y1 then x2 then y2 and so on.

txt = sys.argv[1]
txt_file = open(txt)
img = sys.argv[2]
def readCorner():
    f=txt_file.readlines()
    coordinate=[]
    for i in f:
        coordinate.append(float(i))
    return coordinate


def getPerspectiveMatrix(srcPts, dstPts):
    s = np.zeros((8, 8))
    d = np.zeros((8))
    i=0
    while i<4:
        s[i][0] = s[i+4][3] = srcPts[i][0]
        s[i][1] = s[i+4][4] = srcPts[i][1]
        s[i][2] = s[i+4][5] = 1
        s[i][3] = s[i][4] = s[i][5] = 0
        s[i+4][0] = s[i+4][1] = s[i+4][2] = 0
        s[i][6] = -srcPts[i][0]*dstPts[i][0]
        s[i][7] = -srcPts[i][1]*dstPts[i][0]
        s[i+4][6] = -srcPts[i][0]*dstPts[i][1]
        s[i+4][7] = -srcPts[i][1]*dstPts[i][1]
        d[i] = dstPts[i][0]
        d[i+4] = dstPts[i][1]
        i=i+1
    inverse_of_s = np.linalg.inv(s)                     # sh=d can be h=inv(s) * d
    h = np.dot(inverse_of_s,d)
    h.resize((9,), refcheck=False)                      #resizing homography matrix
    h[8] = 1                                            #Assigning 1 to element
    return h.reshape((3,3))


image = cv2.imread(img)
src_pts= readCorner()
pt1 = np.float32([[src_pts[0],src_pts[1]],[src_pts[6],src_pts[7]],[src_pts[2],src_pts[3]],[src_pts[4],src_pts[5]]])
pt2 = np.float32([[0,0],[500,0],[0,600],[500,600]])
matrix = getPerspectiveMatrix(pt1,pt2)
dst = cv2.warpPerspective(image,matrix,(500,600))
#dst= cv2.resize(dst,(500,600))
cv2.imshow('Final Image',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
