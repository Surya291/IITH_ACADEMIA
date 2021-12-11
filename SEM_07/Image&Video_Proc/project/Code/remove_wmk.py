from imports import *
from find_angled_bbox import return_angled_bbox_pixels

def show_opencv(img, title="None"):  ## to display images
    cv2.imshow(title, cv2.resize(img, (500, 800)))
    cv2.waitKey(0)

def remove_watermark(only_wmk, with_wmk, save_as):
    '''
    consider the image with "only watermark" for reference .. find those pixels and turn them into white..
    otsu thresholding is to find the best threshold automatically when it is a bimodal pixels are present..
    '''

    '''
    wmk = cv2.imread(only_wmk)
    gray_wmk = cv2.cvtColor(wmk, cv2.COLOR_BGR2GRAY)
    gray_wmk = cv2.resize(gray_wmk, (2500, 3700)) #resizing according to aspect ration
    thres, bin_wmk = cv2.threshold(gray_wmk, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    '''




    gray_img = cv2.imread(with_wmk, cv2.IMREAD_GRAYSCALE)
    gray_img = cv2.resize(gray_img, (2500, 3700)) #resizing according to aspect ration

    y_idx, x_idx = return_angled_bbox_pixels()


    print(len(x_idx) )
    print(len(y_idx))

    # Finding the pixels of watermark and changing them ..
    #x_idx, y_idx = np.where(bin_wmk < thres)
    #print(thres)

    img_without_wmk = gray_img.copy()

    for i in range(len(x_idx)):
        if (gray_img[x_idx[i]][y_idx[i]] < 100):  # 100 chosen since the avg intensity of watermark pix is 180
            img_without_wmk[x_idx[i]][y_idx[i]] = 0
        else:
            img_without_wmk[x_idx[i]][y_idx[i]] = 255

    show_opencv(img_without_wmk, title = "adfad")
    cv2.imwrite(save_as, img_without_wmk)
    print('Watermark removed !! and image without watermark has been saved !!')

if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path of the image")
    ap.add_argument("-s", "--save_as", required=True, help="save as ")
    args = vars(ap.parse_args())

    only_wmk = '../test_dir/jpg_files/SD-2020/page11.jpg'
    with_wmk = '../test_dir/jpg_files/SD-2020/' + str(args["image"])
    save_as = '../test_dir/jpg_files/SD-2020/' + str(args["save_as"])
    remove_watermark(only_wmk, with_wmk, save_as)




