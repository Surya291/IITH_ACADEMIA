import cv2
import matplotlib.pyplot as plt
from skimage import measure, morphology
from skimage.color import label2rgb
from skimage.measure import regionprops
import numpy as np
from imports import *
'''
Utility functions ..
'''
def detect_and_disp_CC(img,bg_img):
    '''
    given a img , find the connected components and show the bounding boxes of the top 10 percentile
    REMEMBER !!! It can only detect white pixels while the document has black ones...
    '''
    output = cv2.connectedComponentsWithStats(img, 8, cv2.CV_32S)  # 4 refers to connectivity
    (numLabels, labels, stats, centroids) = output

    area_vec = stats[:, cv2.CC_STAT_AREA]
    Q3 = np.percentile(area_vec, 90, interpolation='midpoint')
    img_show = bg_img.copy()
    area_vec = []
    for i in range(0, numLabels):
        if (i == 0):
            continue
        else:
            area = stats[i, cv2.CC_STAT_AREA]

            if (area > Q3):
                x = stats[i, cv2.CC_STAT_LEFT]
                y = stats[i, cv2.CC_STAT_TOP]
                w = stats[i, cv2.CC_STAT_WIDTH]
                h = stats[i, cv2.CC_STAT_HEIGHT]
                (cX, cY) = centroids[i]
                cv2.rectangle(img_show, (x, y), (x + w, y + h), (0, 0, 255), 3)
                cv2.circle(img_show, (int(cX), int(cY)), 4, (0, 0, 255), -1)

    cv2.imshow("CC_anal", cv2.resize(img_show, (500, 800)))
    cv2.waitKey(0)

def show_opencv(img, title = "None"): ## to display images
    cv2.imshow(title,cv2.resize(img,(500,800) ))
    #cv2.imshow(title, img)
    cv2.waitKey(0)

def invert_img(img): ## complementing an imgae
    temp = img.copy()
    temp[img==255] = 0
    temp[img==0] = 255
    return temp


def sort_contours(contours): ## given a contours list sort them based on their decreasing order of their
    lst = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        lst.append( (x,y,w,h) )
    sorted_list = sorted(lst, key= lambda x: -1*x[2]*x[3])
    ## Returns descending order of areas .
    return sorted_list



if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="image name in Data dir ")
   # ap.add_argument("-s", "--save_as", required=True, help="save as ")
    args = vars(ap.parse_args())

    img_path = '../Data/' + str(args["image"]  + '.jpg')
    #save_as = '../Data/' + str(args["save_as"] + '.jpg' )


    # read the input image
    img = cv2.imread(img_path)
    img = cv2.resize(img, (2500,3700))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    save_as = "../Data/pre_5.jpg"

    # Preprocessing threshold + blur + threshold
    thresh_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    blur = cv2.GaussianBlur(thresh_inv, (1, 1), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    inv_thresh = invert_img(thresh)


    '''
    Dilation --> increasing the white pixels in neighbourhood for an inverted image .. effectively bulgening the black font in the doc starts here !!
    '''
    for i in range(0,7):
        dilated = cv2.dilate(inv_thresh.copy(), None, iterations=i + 1)
        dilated = invert_img(dilated)
    cv2.imshow("Dilated {} times".format(i + 1),cv2.resize(dilated,(500,800) ))
    cv2.waitKey(0)
    detect_and_disp_CC(invert_img(dilated), img)

    contours = cv2.findContours(invert_img(dilated), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    sorted_cntrs = sort_contours(contours) # returns contours in descending order ..

    contour_show = img.copy()
    for i in range(1, 20):
        (x, y, w, h) = sorted_cntrs[i]
        cv2.rectangle(contour_show, (x, y), (x + w, y + h), (0, 0, 255), 2)

    show_opencv(contour_show, title = "Contour plots")

    '''
    for i in range(0, 5):
    
        eroded = cv2.erode(thresh.copy(), None, iterations=i + 1)
        cv2.imshow("Eroded {} times".format(i + 1),cv2.resize(eroded,(500,800) ))
        cv2.waitKey(0)
    
    kernelSizes = [(3, 3), (5, 5), (7, 7)]
    # loop over the kernels sizes
    for kernelSize in kernelSizes:
        # construct a rectangular kernel from the current size and then
        # apply an "opening" operation
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernelSize)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        opening = invert_img(opening)
        show_opencv(opening)
    
        detect_and_disp_CC(opening, img)
    '''
    cv2.destroyAllWindows()


