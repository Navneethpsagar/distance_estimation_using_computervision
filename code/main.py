import numpy as np
import os
import cv2

def get_files(folder):
    return os.listdir(folder)

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images

def rescale_frame(frame, scale =0.75):
	width  = int(frame.shape[1] * scale)
	height  = int(frame.shape[0] * scale)
	dimensions = (width, height)
	return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA )

def get_image_data(image):
    dimensions = image.shape
    megapixels = dimensions[0] * dimensions[1] / 1000000
    return megapixels

def gray_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def blur_image(image, ksize):
    # image
    # Gaussian Kernel Size. [height width]. height and width should be odd and can have different values. If ksize is set to [0 0], then ksize is computed from sigma values
    # Specifies image boundaries while kernel is applied on image borders. Possible values are : cv.BORDER_CONSTANT cv.BORDER_REPLICATE cv.BORDER_REFLECT cv.BORDER_WRAP cv.BORDER_REFLECT_101 cv.BORDER_TRANSPARENT cv.BORDER_REFLECT101 cv.BORDER_DEFAULT cv.BORDER_ISOLATED
    blured_image = cv2.GaussianBlur(image,(ksize,ksize),cv2.BORDER_DEFAULT)
    return blured_image

def get_edge(image, minVal, maxVal):
    # minVal & maxVal : minimum intensity gradient and maximum intensity gradient
    edge_image = cv2.Canny(image, minVal, maxVal)
    return edge_image

def corner_detect(image_g, bsize = 2, ksize = 3, k = 0.04):
    # image - Input image. It should be grayscale and float32 type.
    # blockSize - It is the size of neighbourhood considered for corner detection
    # ksize - Aperture parameter of the Sobel derivative used.
    # k - Harris detector free parameter in the equation.

    if image_g.shape[2] != 1:
        image_g = np.float32(gray_image(image_g))
    else:
        image_g = np.float32(image_g)
    corner = cv2.cornerHarris(image_g, bsize, ksize, k)
    return corner

def corner_sub_detect(image_g, bsize = 2, ksize = 3, k = 0.04 ):

    if image_g.shape[2] != 1:
        image_g = np.float32(gray_image(image_g))
    else:
        image_g = np.float32(image_g)
        
    # find Harris corners
    dst = cv2.cornerHarris(image_g,2,3,0.04)
    dst = cv2.dilate(dst,None)
    ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
    dst = np.uint8(dst)
    
    # find centroids
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    # define the criteria to stop and refine the corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(image_g,np.float32(centroids),(5,5),(-1,-1),criteria)
    # Now draw them
    res = np.hstack((centroids,corners))
    res = np.int0(res)
    image_g[res[:,1],res[:,0]]=[0,0,255]
    image_g[res[:,3],res[:,2]] = [0,255,0]
    cv2.imwrite('subpixel5.png',image_g)