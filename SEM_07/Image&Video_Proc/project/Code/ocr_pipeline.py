'''
This script consists of all the functions required to convert a pdf to a a .txt OCR'd file .

Pipeline : pdf--> image parsing --> remove watermark --> remove header --> signature removal  --> OCR and pasting in a .txt file .

changed :
1. artifacts removal --> signature removal

'''

from imports import *
from remove_header import *
from remove_artifacts import *

import sys
from translate import *
from extract_text_bbox import *
from custom_ocr import *



sys.path.insert(0, '/home/surya/Desktop/Lending_Kat/Code/yolov5')
from yolo_sign_remove import run
from find_angled_bbox import return_angled_bbox_pixels  ## for removing wmk

class project:
    '''
    TODO :  there are tables present in the image which can be detected as largest box

    '''

    def __init__(self, pdf_dir, pdf_name, jpg_parent_dir, ocr_dir):

        self.ocr_dir = ocr_dir

        self.pdf_dir = pdf_dir
        self.pdf_name = pdf_name
        self.jpg_parent_dir = jpg_parent_dir
        self.CONST_WIDTH = 3700
        self.CONST_HEIGHT = 2500
        self.CONST_WMK_THRESH = 130

        ### constants for wmk
        self.y_idx, self.x_idx = return_angled_bbox_pixels()

    def show_opencv(self, img, title="None"):  ## to display images
        cv2.imshow(title, cv2.resize(img, (500, 800)))
        cv2.waitKey(0)

    def remove_wmk(self):
        '''
        TODO :  Need to set the wmk threshold ...
        TODO: improve wmk removal ...

        '''
        #### Created a matrix that return the bbox (slanted) coordintes to remove from.

        y_idx, x_idx = self.y_idx, self.x_idx
        self.img_wout_wmk = self.img.copy()
        # print(self.img.shape)
        for i in range(len(x_idx)):
            if (self.img[x_idx[i]][y_idx[i]] < 100):  # 100 chosen since the avg intensity of watermark pix is 180
                self.img_wout_wmk[x_idx[i]][y_idx[i]] = 0
            else:
                self.img_wout_wmk[x_idx[i]][y_idx[i]] = 255

        self.img_wout_wmk = cv2.threshold(self.img_wout_wmk, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        #self.show_opencv(self.img_wout_wmk, "Wout wmk")

    def remove_header(self):
        '''
        Does preprocessing --> Finds overall contours -->  find one with the max area --> whiten it
        TODO : Need to use edge detection like hough transform or track all the complete boundaru of the contour
        and then erase it .

        There are cases where the header is angled and thus by cropping it with its extreme boundaries also
        erases the text beneath it.
        '''

        self.img_wout_header = self.img_wout_wmk.copy()
        self.img_wout_header = remove_header_util(self.img_wout_header)  ## util function written in another script
        #self.show_opencv(self.img_wout_header, "wout header")
        
    def gray2rgb(self):
        '''
        converts the image without header to rgb image to send it to the yolo model which takes
        640 pixels rgb image.

        TODO :  consider the aspect ratio and retrain the model ..
        '''

        def scale_img2200to640(img2200):
            max_height = 640
            max_width = 480

            
            page_height, page_width = img2200.shape[:2]
            # computes the scaling factor
            if max_height < page_height or max_width < page_width:
                scaling_factor = max_height / float(page_height)
                if max_width / float(page_width) < scaling_factor:
                    scaling_factor = max_width / float(page_width)
                # scale the image with the scaling factor
                img640 = cv2.resize(img2200, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
            return img640

        self.img_rgb = self.img_wout_artifacts.copy()
        self.img_rgb = cv2.cvtColor(self.img_rgb, cv2.COLOR_GRAY2RGB)  ### 2200 image..
        self.img_rgb_640 = scale_img2200to640(self.img_rgb.copy())

    def remove_artifacts(self, image):
        '''
        Removes artifacts such as stamps and other left outs
        '''
        #self.img_wout_artifacts = image.copy()
        self.img_wout_artifacts = remove_artifacts_util(image)
        #self.show_opencv(self.img_wout_artifacts, title= "After removing artifacts...")


    def remove_space_in_txt(self,text):
        '''
        Removes space after a full stop . Observed that such punctuation is hampering the translation.
        '''
        text = text.replace(". ", ".")
        text = text.replace("|", "")
        text = text.replace("೫೦", "No.")
        return text



    def pdf2img(self):
        self.images = convert_from_path(os.path.join(self.pdf_dir, self.pdf_name))
        self.pdf_only_name = self.pdf_name[:-4]  ## only name -- removing .pdf
        self.jpg_dir = os.path.join(self.jpg_parent_dir, self.pdf_only_name)
                                                                                                                          
        self.txt_name = os.path.join(self.ocr_dir+'/raw_ocr/', self.pdf_only_name + ".txt")
        self.eng_txt_name = os.path.join(self.ocr_dir+'/translated_ocr/', self.pdf_only_name + "_eng.txt")

        print(self.txt_name)
        self.txt_file = open(self.txt_name, "w+")
        self.eng_txt_file = open(self.eng_txt_name,"w+")

        if (not (os.path.isdir(self.jpg_dir))):
            os.mkdir(self.jpg_dir)  ### Creating a dir with parsed images

        self.img_before_yolo_list_640 = []
        self.img_before_yolo_list_2200 = []
        for img_id in list([0,2,10,11]):#, len(self.images) , 1):   #len(self.images) , 1):
            self.img_pil = self.images[img_id]
            self.rgb_img = np.asarray(self.img_pil.resize((self.CONST_HEIGHT, self.CONST_WIDTH)))  ### Resizing into a definite size  \
            # maintaining the aspect ration : 1.7
            self.img = cv2.cvtColor(self.rgb_img, cv2.COLOR_BGR2GRAY)
            self.img = np.array(self.img)
            cv2.imwrite(self.jpg_dir + '/' + str(img_id) + '.jpg', self.img)
            #self.show_opencv(self.img, "raw iamge")
            self.remove_wmk()
            cv2.imwrite(self.jpg_dir + '/' + str(img_id) + '_wout_wmk.jpg', self.img_wout_wmk)
            self.remove_header()
            cv2.imwrite(self.jpg_dir + '/' + str(img_id) + '_wout_head.jpg', self.img_wout_header)
            self.remove_artifacts(self.img_wout_header)
            #self.show_opencv(self.img_wout_artifacts, "artifacts 1 iamge")
            cv2.imwrite(self.jpg_dir + '/' + str(img_id) + '_after_artifacts1.jpg', self.img_wout_artifacts)
            self.gray2rgb()
            self.img_before_yolo_list_640.append(self.img_rgb_640)
            #print('asdfasdfdsf',self.img_rgb.shape)
            self.img_before_yolo_list_2200.append(self.img_rgb)
            #cv2.imwrite(self.jpg_dir + '/' + str(img_id) + '_rgb2200.jpg', self.img_rgb)
            

        
        self.img_after_yolo_list = run(self.img_before_yolo_list_640, self.img_before_yolo_list_2200)
        cv2.destroyAllWindows()
        for img_id, self.img_wout_sign in enumerate(self.img_after_yolo_list):
            temp = list([0,2,10,11])
            img_id = temp[img_id]

            show_opencv(self.img_wout_sign, "image without sign ")
            cv2.imwrite(self.jpg_dir + '/' + str(img_id) + '_wout_sign.jpg', self.img_wout_sign)
            #print(self.img_wout_sign.shape)
            self.remove_artifacts(self.img_wout_sign)
            cv2.imwrite(self.jpg_dir + '/' + str(img_id) + '_after_artifacts2.jpg', self.img_wout_artifacts)
            
            
            self.img_crop = crop_txt_image(self.img_wout_artifacts)
            self.show_opencv(self.img_crop, title= "Cropped image...")
            cv2.imwrite(self.jpg_dir + '/' + str(img_id) + '_cropped.jpg', self.img_crop)

            self.txt = OCR(self.img_crop)
            self.txt = self.remove_space_in_txt(self.txt) ### removing spaces
            print(self.txt)


            # self.txt = pytesseract.image_to_string(self.img_wout_header)
            self.txt_file.write(self.txt)
            self.txt_file.write("==================================================================================")
            self.txt_file.write("==================================================================================\n")


        cv2.destroyAllWindows()
        self.txt_file.close()


        print("File created!!!")

if __name__ == "__main__":
    pdf_dir = "/home/surya/Desktop/Lending_Kat/Property_docs_for_MVP"
    jpg_parent_dir = "/home/surya/Desktop/Lending_Kat/Property_docs_for_MVP/eng_expt/IVP_pipeline/jpg_files"
    ocr_dir = "/home/surya/Desktop/Lending_Kat/Property_docs_for_MVP/eng_expt/IVP_pipeline/OCR"

    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--pdf", required=True, help="path of the image")
    args = vars(ap.parse_args())

    pro1 = project(pdf_dir, args['pdf'], jpg_parent_dir, ocr_dir)
    pro1.pdf2img()