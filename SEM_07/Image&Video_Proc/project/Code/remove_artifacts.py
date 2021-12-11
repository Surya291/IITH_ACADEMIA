from imports import *

'''
Failed attempts 

        Uses erosion operation to join the black pixels effectively joining all the letters.
        --> Running contour detection and finding the bbox of the contours of the bbox with largest areas
        -->If width is larger than the typical font then understand it as a artifact --> done to remove stamps and other large objects


        TODO :  need to standardize the constants
        TODO : Problem arises when the signature is close to the text then it detects a large bbox
        thus it automatically gets removed.


1. tried extracting the ROI and pass through OCR and find conf to find if the ROI has text or is an artifact--> Very slow and not accurate
2. Staryted using the black hat operator and closing operatio to find text blobs in the image ,
3. Tried using the angled contour detection which only captures small areas and thus not ideal \
4. Introduced mean line width to eliminate contours that are detected by the line ,

'''



'''

Resource : OCR with OpenCV, Tesseract, and Python, passport

New :
USed black hat operator to convert to white pixels on black bacforount
Later used closing operation to detect lines 
filtered the contours by height (allow if larger than avaerage font size) or width (allow if greater than  half the line length)

'''

def show_opencv( img, title="None"):  ## to display images
    cv2.imshow(title, cv2.resize(img, (500, 800)))
    cv2.waitKey(0)

def remove_artifacts_util(img_wout_header):
        '''
        Uses erosion operation to join the black pixels effectively joining all the letters.
        --> Running contour detection and finding the bbox of the contours of the bbox with largest areas
        -->If width is larger than the typical font then understand it as a artifact --> done to remove stamps and other large objects


        TODO :  need to standardize the constants
        TODO : Problem arises when the signature is close to the text then it detects a large bbox
        thus it automatically gets removed.
        '''

        def sort_contours(contours):  ## given a contours list sort them based on their decreasing order of their
            lst = []
            for c in contours:
                cx, cy, cw, ch = cv2.boundingRect(c)
                lst.append((cx, cy, cw, ch))
            sorted_list = sorted(lst, key=lambda x: -1 * x[2] * x[3])
            ## Returns descending order of areas .
            return sorted_list

        def find_avg_conf(d):  ### finding
            list = d['conf']
            conf_sum, count = 0, 0
            for i in list:
                if (i == '-1'):
                    continue
                else:
                    conf_sum = conf_sum + int(i)
                    count = count + 1
            if (count == 0): return 0
            return conf_sum / count

        ### To remove the ROI with given dimensions if ROI is found to contain useless artifacts
        def remove_bbox(img, dim_tuple):
            (x, y, w, h) = dim_tuple
            img[y:y + h, x:x + w] = 255 * np.ones((h, w))
            return img

        def invert_img(img):  ## complementing an imgae
            temp = img.copy()
            temp[img == 255] = 0
            temp[img == 0] = 255
            return temp

        ### Constants...
        CONST_EROSION_ITER = 10
        CONST_CONF_THRESH1 = 60  ## upper threhold also checks if the width is of general font width
        CONST_CONF_THRESH2 = 30  ### lower threshhol
        CONST_CNTR_PERCENTILE = 0.5  ## top contours
        CONST_EDGE_BUFF = 0  ## buffer length for bbox for broad coverage of ROI
        # CONST_AVG_FONT_WIDTH = 20 ## AVG_WIDTH of the font
        CONST_AVG_FONT_WIDTH = 80  ## AVG_WIDTH of the font
        CONST_AVG_LINE_WIDTH = 700
        CONST_CLOSE_FILTER_PARAM = (25,3)
        ##

        ### For display
        img_wout_artifacts = img_wout_header.copy()
        if(len(img_wout_artifacts.shape) == 3):
            img_wout_artifacts = cv2.cvtColor(img_wout_artifacts, cv2.COLOR_RGB2GRAY)

        img_ROIS = cv2.cvtColor(img_wout_artifacts, cv2.COLOR_GRAY2RGB)   ### for whitening the contour
        img_wout_artifacts = cv2.GaussianBlur(img_wout_artifacts, (5, 5), 0)

        rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, CONST_CLOSE_FILTER_PARAM)   #####################################  IMPORANT PARAMETER ###################
        img_wout_artifacts = cv2.morphologyEx(img_wout_artifacts, cv2.MORPH_BLACKHAT, rectKernel)
        grad = cv2.Sobel(img_wout_artifacts, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
        grad = np.absolute(grad)

        (minVal, maxVal) = (np.min(grad), np.max(grad))
        grad = (grad - minVal) / (maxVal - minVal)
        grad = (grad * 255).astype("uint8")

        grad = cv2.morphologyEx(grad, cv2.MORPH_CLOSE, rectKernel)
        thresh_grad = cv2.threshold(grad, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        show_opencv(thresh_grad, title = "Without artifacts !!!")
        cv2.imwrite('sobel.jpg', thresh_grad)
        #thresh_grad = cv2.morphologyEx(thresh_grad, cv2.MORPH_OPEN, rectKernel)
        #thresh_grad = cv2.morphologyEx(thresh_grad, cv2.MORPH_CLOSE, rectKernel)
        #show_opencv(thresh_grad, "threshed")
        #show_opencv(thresh, "eroded")

        contours = cv2.findContours((thresh_grad), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        sorted_cntrs = sort_contours(contours)


        '''
        ### Version 01 : Used typical morphological algo....
        img_eroded = cv2.threshold(img_wout_header, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        img_eroded = cv2.GaussianBlur(img_eroded, (5, 5), 0)
        img_eroded = cv2.threshold(img_eroded, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5))
        img_eroded = cv2.morphologyEx(img_eroded, cv2.MORPH_CLOSE, kernel)

        img_eroded = cv2.dilate(img_eroded, None, iterations=2)
        show_opencv(img_eroded, "eroded")
        img_eroded = cv2.erode(img_eroded, None, iterations=2)
        '''

        '''
        #### finding angled contours....   ### doesnot work since the elements gets small
        for c in contours:
            rect = cv2.minAreaRect(c)
            (center,(w,h),_) = rect

            if(h> CONST_AVG_FONT_WIDTH and w < CONST_AVG_LINE_WIDTH):
                box = cv2.boxPoints(rect) ## finding the box points bounding it
                box = np.int0(box) 
                cv2.drawContours(img_ROIS,[box],0,(255,255,0),2)
        '''
        for i in range(int(CONST_CNTR_PERCENTILE * len(sorted_cntrs))):
            ## displaying top contours with greater sizes

            (sc_x, sc_y, sc_w, sc_h) = sorted_cntrs[i]
            sc_w, sc_h = sc_w + CONST_EDGE_BUFF, sc_h + CONST_EDGE_BUFF
            #cropped_ROI = img_wout_artifacts[sc_y:sc_y + sc_h, sc_x:sc_x + sc_w]

            if(sc_h> CONST_AVG_FONT_WIDTH and sc_w < CONST_AVG_LINE_WIDTH):
                cv2.rectangle(img_ROIS, (sc_x, sc_y), (sc_x + sc_w, sc_y + sc_h), (255,255, 255),-1)
        #img_wout_artifacts = cv2.morphologyEx(img_wout_artifacts, cv2.MORPH_CLOSE, np.ones((5,5),np.uint8))       
        img_wout_artifacts = cv2.cvtColor(img_ROIS, cv2.COLOR_RGB2GRAY)


        return img_wout_artifacts

if __name__ == "__main__":

    '''
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="image name in Data dir ")
    #ap.add_argument("-s", "--save_as", required=True, help="save as ")
    args = vars(ap.parse_args())

    img_path = '/home/surya/Desktop/Lending_Kat/Property docs for MVP/jpg_files_new2/MDSD_2018/' + str(args["image"]  + '.jpg')
    #save_as = '/home/surya/Desktop/Lending_Kat/Property docs for MVP/jpg_files_new2/1_SaleDeed-2020/' + str(args["save_as"] + '.jpg' )

    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (2500, 3700))  # resizing according to aspect ration
    img_wout_artifacts = remove_artifacts_util(gray)
    #cv2.imwrite(save_as, img_without_header)

    show_opencv(img_wout_artifacts, title = "Without artifacts !!!")
    '''
    '''
    cv2.imshow("thresh", cv2.resize(img, (500, 800)))
    cv2.imshow("temp", cv2.resize(thresh, (500, 800)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()    
    '''

    '''
    direc = '/home/surya/Desktop/Lending_Kat/Property docs for MVP/jpg_files_new2/MDSD_2018'

    for filename in os.listdir(direc):
        if (not filename.endswith('cropped.jpg')):


            print(filename)
            img = cv2.imread(os.path.join(direc, filename))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.resize(gray, (2500, 3700))  # resizing according to aspect ration
            img_wout_artifacts = remove_artifacts_util(gray)

            show_opencv(img_wout_artifacts, title = "Without artifacts !!!")
    '''

    img = cv2.imread('/home/surya/Desktop/Lending_Kat/Property_docs_for_MVP/eng_expt/IVP_pipeline/jpg_files/MDSD-2012/11_wout_head.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (2500, 3700))  # resizing according to aspect ration
    img_wout_artifacts = remove_artifacts_util(gray)




            

    #run(im0_640_list , im0_2200_list, line_thickness=line_thickness, conf_thres=conf_thres)
    #print("done!!")
