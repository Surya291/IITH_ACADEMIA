from imports import *
from remove_signature import *

def find_avg_conf(d):
    list = d['conf']
    conf_sum = 0;
    count = 0
    for i in list:
        if(i == '-1'):
            continue
        else:
            conf_sum = conf_sum + int(i)
            count = count +1
    if(count == 0): return 0
    return conf_sum/count

def remove_bbox(img, dim_tuple ):
    (x, y, w, h) = dim_tuple
    img[y:y+h,x:x+w] = 255*np.ones((h,w))
    return img
if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="image name in Data dir ")
    ap.add_argument("-s", "--save_as", required=True, help="save as ")
    args = vars(ap.parse_args())

    img_path = '../Data/' + str(args["image"] + '.jpg')
    save_as = '../Data/' + str(args["save_as"] + '.jpg' )

    # read the input image
    img = cv2.imread(img_path)
    img = cv2.resize(img, (2500, 3700))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    # Preprocessing threshold + blur + threshold
    thresh_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    blur = cv2.GaussianBlur(thresh_inv, (1, 1), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    inv_thresh = thresh.copy()
    #inv_thresh = invert_img(thresh)

    '''
    Dilation --> increasing the white pixels in neighbourhood for an inverted image .. effectively bulgening the black font in the doc starts here !!
    '''
    for i in range(0, 7):
        dilated = cv2.erode(inv_thresh.copy(), None, iterations=i + 1)
        #dilated = invert_img(dilated)
    #cv2.imshow("Dilated {} times".format(i + 1), cv2.resize(dilated.copy(), (500, 800)))
    #cv2.waitKey(0)
    #detect_and_disp_CC(invert_img(dilated), img)

    contours = cv2.findContours(invert_img(dilated), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    sorted_cntrs = sort_contours(contours)  # returns contours in descending order ..

    contour_show = img.copy()
    print(contour_show.shape)
    print(gray.shape)

    dim_thresh =0
    conf_thresh = 70
    conf_thresh2 = 40
    img_without_sign = thresh.copy()
    for i in range(int(0.6*len(sorted_cntrs))):  ## displaying top contours with greater sizes
        (x, y, w, h) = sorted_cntrs[i]
        print(x,y,w,h)
        w,h = w + dim_thresh, h+dim_thresh
        cropped_img = gray[y:y+h,x:x+w]


        cv2.rectangle(contour_show, (x, y), (x + w, y + h), (0, 0, 255), 2)
        d = pytesseract.image_to_data(cropped_img, output_type=Output.DICT, config='--psm 6')
        print(find_avg_conf(d))

        avg_conf_d = find_avg_conf(d)
        if( (avg_conf_d< conf_thresh and h > 65) or (avg_conf_d < conf_thresh2) ):
            img_without_sign = remove_bbox(img_without_sign, (x,y,w,h))
        #plt.imshow(cropped_img, cmap = 'gray')
        #plt.show()

    show_opencv(contour_show, title="Detected artifacts")
    show_opencv(img_without_sign, title="Image after removing artifacts ")


    cv2.destroyAllWindows()
    cv2.imwrite(save_as, img_without_sign)


