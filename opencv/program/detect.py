import numpy as np
import cv2
import cv2.aruco as aruco
import math


####################### Define Utility Functions Here ##########################
"""
Function Name : getCameraMatrix()
Input: None
Output: camera_matrix, dist_coeff
Purpose: Loads the camera calibration file provided and returns the camera and
         distortion matrix saved in the calibration file.
"""
def getCameraMatrix():
        with np.load('System.npz') as X:
                camera_matrix, dist_coeff, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]
        return camera_matrix, dist_coeff

"""
Function Name : sin()
Input: angle (in degrees)
Output: value of sine of angle specified
Purpose: Returns the sine of angle specified in degrees
"""
def sin(angle):
        return math.sin(math.radians(angle))

"""
Function Name : cos()
Input: angle (in degrees)
Output: value of cosine of angle specified
Purpose: Returns the cosine of angle specified in degrees
"""
def cos(angle):
        return math.cos(math.radians(angle))


################################################################################


"""
Function Name : detect_markers()
Input: img (numpy array), camera_matrix, dist_coeff
Output: aruco list in the form [(aruco_id_1, centre_1, rvec_1, tvec_1),(aruco_id_2,
        centre_2, rvec_2, tvec_2), ()....]
Purpose: This function takes the image in form of a numpy array, camera_matrix and
         distortion matrix as input and detects ArUco markers in the image. For each
         ArUco marker detected in image, paramters such as ID, centre coord, rvec
         and tvec are calculated and stored in a list in a prescribed format. The list
         is returned as output for the function
"""
def detect_markers(img, camera_matrix, dist_coeff):
        markerLength = 100
        aruco_list = []
        ######################## INSERT CODE HERE ########################
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
        parameters = aruco.DetectorParameters_create()
        corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)
        rvec, tvec,_= aruco.estimatePoseSingleMarkers(corners, markerLength, camera_matrix, dist_coeff)
        centrecoord=[]
        L=len(ids)
        
        for i in range(0,L):
                x=int(corners[i][0][0][0]+corners[i][0][1][0]+corners[i][0][3][0]+corners[i][0][2][0])/4
                y=int(corners[i][0][0][1]+corners[i][0][1][1]+corners[i][0][3][1]+corners[i][0][2][1])/4
                p=(x,y)
                centrecoord.append(p)
        for i in range(0,L):
                p=(ids[i][0],centrecoord[i],rvec[i],tvec[i])
                
                aruco_list.append(p)
        ##################################################################
        return aruco_list

"""
Function Name : drawAxis()
Input: img (numpy array), aruco_list, aruco_id, camera_matrix, dist_coeff
Output: img (numpy array)
Purpose: This function takes the above specified outputs and draws 3 mutually
         perpendicular axes on the specified aruco marker in the image and
         returns the modified image.
"""
def drawAxis(img, aruco_list, aruco_id, camera_matrix, dist_coeff):
        for x in aruco_list:
                if aruco_id == x[0]:
                        rvec, tvec = x[2], x[3]
        markerLength = 100
        m = markerLength/2
        pts = np.float32([[-m,m,0],[m,m,0],[-m,-m,0],[-m,m,m]])
        pt_dict = {}
        imgpts, _ = cv2.projectPoints(pts, rvec, tvec, camera_matrix, dist_coeff)
        for i in range(len(pts)):
                 pt_dict[tuple(pts[i])] = tuple(imgpts[i].ravel())
        src = pt_dict[tuple(pts[0])];   dst1 = pt_dict[tuple(pts[1])];
        dst2 = pt_dict[tuple(pts[2])];  dst3 = pt_dict[tuple(pts[3])];
        
        img = cv2.line(img, src, dst1, (0,255,0), 4)
        img = cv2.line(img, src, dst2, (255,0,0), 4)
        img = cv2.line(img, src, dst3, (0,0,255), 4)
        return img

"""
Function Name : drawCube()
Input: img (numpy array), aruco_list, aruco_id, camera_matrix, dist_coeff
Output: img (numpy array)
Purpose: This function takes the above specified outputs and draws a cube
         on the specified aruco marker in the image and returns the modified
         image.
"""
def drawCube(img, ar_list, ar_id, camera_matrix, dist_coeff):
        for x in ar_list:
                if ar_id == x[0]:
                        rvec, tvec = x[2], x[3]
        markerLength = 100
        m = markerLength/2
        ######################## INSERT CODE HERE ########################
        pts = np.float32([[-m,m,m], [-m,-m,m], [m,-m,m], [m,m,m],[-m,m,0], [-m,-m,0], [m,-m,0], [m,m,0]])
        imgpts, _ = cv2.projectPoints(pts, rvec, tvec, camera_matrix, dist_coeff)
        imgpts = np.int32(imgpts).reshape(-1,2)
        img = cv2.drawContours(img, [imgpts[:4]],-1,(0,0,255),4)
        for i,j in zip(range(4),range(4,8)): img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(0,0,255),4);
        img = cv2.drawContours(img, [imgpts[4:]],-1,(0,0,255),4)
        ##################################################################
        return img

"""
Function Name : drawCylinder()
Input: img (numpy array), aruco_list, aruco_id, camera_matrix, dist_coeff
Output: img (numpy array)
Purpose: This function takes the above specified outputs and draws a cylinder
         on the specified aruco marker in the image and returns the modified
         image.
"""
def drawCylinder(img, ar_list, ar_id, camera_matrix, dist_coeff):
        for x in ar_list:
                if ar_id == x[0]:
                        centre,rvec, tvec = x[1],x[2], x[3]
        pt_dict = {}
        markerLength = 100
        radius = markerLength/2;
        height = markerLength*1.5
        m = markerLength/2
        side=40
        the=360/side;
        xp=0
        yp=0
        pts1=[]
        pts2=[]        
        ######################## INSERT CODE HERE #########,###############
        for i in range(1,side):
                x=radius*cos(the*i)
                y=radius*sin(the*i)
                if i%3==0:
                        pts=np.float32([[0,0,0],[x,y,0],[x,y,height],[0,0,height],])
                        imgpts, _ = cv2.projectPoints(pts, rvec, tvec, camera_matrix, dist_coeff)
                        imgpts = np.int32(imgpts).reshape(-1,2)
                        img = cv2.drawContours(img, [imgpts],-1,(0,0,255),4)
                pts1=pts1+[[x,y,0],[xp,yp,0]]
                pts2=pts2+[[x,y,height],[xp,yp,height]]
                xp=x
                yp=y
        L=len(pts1)
        pts1 = np.float32(pts1+pts2)
        imgpts1, _ = cv2.projectPoints(pts1, rvec, tvec, camera_matrix, dist_coeff)
        imgpts1 = np.int32(imgpts1).reshape(-1,2)
        img = cv2.drawContours(img, [imgpts1[:L]],-1,(0,0,255),4)
        img = cv2.drawContours(img, [imgpts1[L:]],-1,(0,0,255),4)
                
        ##################################################################
        return img

"""
MAIN CODE
This main code reads images from the test cases folder and converts them into
numpy array format using cv2.imread. Then it draws axis, cubes or cylinders on
the ArUco markers detected in the images.
"""


if __name__=="__main__":
        cam, dist = getCameraMatrix()
        img = cv2.imread("..\\TestCases\\image_3.jpg")
        aruco_list = detect_markers(img, cam, dist)
        for i in aruco_list:
                img = drawAxis(img, aruco_list, i[0], cam, dist)
                img = drawCube(img, aruco_list, i[0], cam, dist)
                img = drawCylinder(img, aruco_list, i[0], cam, dist)
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
