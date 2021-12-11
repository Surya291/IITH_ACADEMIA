import cv2
import os

base_dir = '/home/surya/Desktop/Lending_Kat/sign_images/'
save_dir = '/home/surya/Desktop/Lending_Kat/sign_images_resized/images/'

max_height = 640
max_width = 480

for filename in os.listdir(base_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        print(os.path.join( filename))
        img = cv2.imread(base_dir + filename, 1)
        print(img.shape)
        page_height, page_width = img.shape[:2]
        # computes the scaling factor
        if max_height < page_height or max_width < page_width:
            scaling_factor = max_height / float(page_height)
            if max_width/float(page_width) < scaling_factor:
                scaling_factor = max_width / float(page_width)
            # scale the image with the scaling factor
            img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
            new_file_path = save_dir+ filename
            cv2.imwrite(new_file_path, img)  # write the scales image


    else:
        continue