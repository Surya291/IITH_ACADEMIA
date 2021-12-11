from imports import *
import math
'''
Remember in opencv the y_axis is the 0th dim and x axis the the 1st
'''


def return_angled_bbox_pixels(plot = False):

    only_wmk_path = '../Data/just_watermark.jpg'
    #only_wmk_path = '/home/surya/Desktop/Lending_Kat/Data/page11.jpg'
    gray_wmk = cv2.imread(only_wmk_path, cv2.IMREAD_GRAYSCALE)
    gray_wmk = cv2.resize(gray_wmk, (2500, 3700)) #resizing according to aspect ration

    ### Preprocessing ....
    _, bin_wmk = cv2.threshold(gray_wmk, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    bin_wmk = cv2.GaussianBlur(bin_wmk, (5, 5), 0)
    bin_wmk = cv2.GaussianBlur(bin_wmk, (5, 5), 0)
    bin_wmk = cv2.GaussianBlur(bin_wmk, (5, 5), 0)
    _, bin_wmk = cv2.threshold(bin_wmk, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    ### removes all the black noise pixels..
    bin_wmk = cv2.morphologyEx(bin_wmk, cv2.MORPH_CLOSE, np.ones((11,11)))


    ### threshold  = 130
    y_idx, x_idx = np.where(bin_wmk <  130) ## all the pixels with value 0

    y_mini, x_mini = np.amin(y_idx), np.amin(x_idx)
    y_maxi, x_maxi = np.amax(y_idx), np.amax(x_idx)
    y_center, x_center = np.mean(y_idx), np.mean(x_idx)

    ### Centering at the origin
    x_idx = x_idx - x_center
    y_idx = y_idx - y_center

    ### rotating with 45 deg
    theta = (np.pi)/4
    coords = np.array([x_idx, y_idx])

    ## Rotation matrix
    R = np.array( [ [  math.cos(theta), -1*math.sin(theta) ], [  math.sin(theta) , math.cos(theta)  ] ] )
    R_coords = R@coords

    x_min,x_max = np.amin(R_coords[0]), np.amax(R_coords[0])
    y_min,y_max = np.amin(R_coords[1]), np.amax(R_coords[1])


    ### finding the rotated bbox

    margin = 20 ## margin of the bbox
    bbox_x, bbox_y = [],[]
    for i in range(int(x_min)-margin, int(x_max)+margin ):
        for j in range(int(y_min) - margin, int(y_max) + margin):
            bbox_x.append(i)
            bbox_y.append(j)

    coords = np.array([bbox_x, bbox_y])

    ## rotating bacj
    theta = -1*(np.pi)/4
    R_inv = np.array( [ [  math.cos(theta), -1*math.sin(theta) ], [  math.sin(theta) , math.cos(theta)  ] ] )
    R_inv_coords = R_inv@coords

    x = np.array(R_inv_coords[0][:] + x_center, dtype = np.uint16)
    y = np.array(R_inv_coords[1][:] + y_center, dtype = np.uint16)




    if(plot==True):


        plt.imshow(bin_wmk, cmap='gray')
        plt.scatter(x=x, y=y, c='r')
        #plt.scatter(x=[x_mini, x_maxi, x_center], y=[y_maxi, y_mini, y_center], c='g')
        plt.axis('off')
        plt.savefig('wmk_bbox.jpg')
        plt.show()
    return x, y

### plotting the bbox



if __name__ == "__main__":
    return_angled_bbox_pixels(plot = True)