from imports import *
'''
source  : https://theailearner.com/tag/cv2-minarearect/
Algo : 

AIM :  To find the header which resembles a rectangle (an angled rectangle) placed in the top of the page.

Algo : 

1. Find the contours in the image
2. Find the center of the detected contour , if this lies on the first third of the page --> qualifies as a header
3. Find the contour with max area .
4. Remove it 

'''

def find_max_header_contour(contours):
    maxi = 0
    for c in contours:
        ### Get the angled rectangle box
        rect = cv2.minAreaRect(c) ## min area rect
        (center, (w,h) ,_ ) = rect
        if(center[1] < 1000 ): ## If contour lies in the first third

            if(w*h >  maxi):
                maxi = w*h
                rect_max = rect
    return rect_max


def remove_header_util(img):
    '''
    img : should be a bgr image will be converted to gray later
    Descript : This function is responsible for detecting the header (logically the largest bounded rectangle that can be detected)
    '''
    # Preprocessing threshold + blur + threshold
    thresh_inv = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    blur = cv2.GaussianBlur(thresh_inv, (1, 1), 0)
    thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    rect_max = find_max_header_contour(contours)
    ### get the angled rectangular box 
    box = cv2.boxPoints(rect_max) ## finding the box points bounding it 
    box = np.int0(box) 
    # cv2.rectangle(image, start_point, end_point, color (BGR), thickness)
    # -1 refers to filled rectange..
    cv2.drawContours(img,[box],0,(255,255,255),-1)

    return img




if __name__ == "__main__":

    def show_opencv( img, title="None"):  ## to display images
        cv2.imshow(title, cv2.resize(img, (500, 800)))
        cv2.waitKey(0)

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="image name in Data dir ")
    #ap.add_argument("-s", "--save_as", required=True, help="save as ")
    args = vars(ap.parse_args())

    img_path = '/home/surya/Desktop/Lending_Kat/Property docs for MVP/jpg_files_new2/MDSD_2018/' + str(args["image"]  + '.jpg')
    #save_as = '/home/surya/Desktop/Lending_Kat/Property docs for MVP/jpg_files_new2/1_SaleDeed-2020/' + str(args["save_as"] + '.jpg' )

    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (2500, 3700))  # resizing according to aspect ration
    img_without_header = remove_header_util(gray)
    #cv2.imwrite(save_as, img_without_header)

    show_opencv(img_without_header, title = "Without header !!!")
    '''
    cv2.imshow("thresh", cv2.resize(img, (500, 800)))
    cv2.imshow("temp", cv2.resize(thresh, (500, 800)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''




