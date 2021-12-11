import os, sys, random, shutil
import xml.etree.ElementTree as ET
from glob import glob
import pandas as pd
from shutil import copyfile
import pandas as pd
#from sklearn import preprocessing, model_selection
import matplotlib.pyplot as plt

from matplotlib import patches
import numpy as np
import cv2

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn
import matplotlib.pyplot as plt

sys.path.insert(0, '/home/surya/Desktop/Lending_Kat/Code/yolov5')

from models.experimental import attempt_load
from utils.datasets import LoadImages, LoadStreams
from utils.general import apply_classifier, check_img_size, check_imshow, check_requirements, check_suffix, colorstr, \
    increment_path, non_max_suppression, print_args, save_one_box, scale_coords, set_logging, \
    strip_optimizer, xyxy2xywh

from utils.augmentations import letterbox
from utils.plots import Annotator, colors
from utils.torch_utils import load_classifier, select_device, time_sync

'''
TODO : Need to retrain the model --> get a better threshold and focus on resizing the bbox for a 2200 scaled image
TODO :  can train it for a larger images .
'''


@torch.no_grad()
def run(im0_640_list, ## shrinked image for yolo modelling..
        im0_2200_list, ## resized list of images ...
        weights='/home/surya/Desktop/Lending_Kat/Code/yolov5/best.pt',  # model.pt path(s)
        imgsz=(640, 480),  # inference size (pixels)
        conf_thres=0.02,  # confidence threshold
        iou_thres=0.3,  # NMS IOU threshold
        max_det=40,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=False,  # show results
        save_txt=False,  # save results to *.txt
        save_conf=False,  # save confidences in --save-txt labels
        save_crop=False,  # save cropped prediction boxes
        nosave=False,  # do not save images/videos
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        update=False,  # update all models
        name='exp',  # save results to project/name
        exist_ok=False,  # existing project/name ok, do not increment
        line_thickness=2,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        CONST_AVG_FONT_WIDTH = 80 ## AVG_WIDTH of the font
        ):
    # Initialize
    set_logging()
    device = select_device(device)
    half &= device.type != 'cpu'  # half precision only supported on CUDA
    #print(device)

    # Load model
    w = weights[0] if isinstance(weights, list) else weights
    classify, suffix, suffixes = False, Path(w).suffix.lower(), ['.pt', '']
    check_suffix(w, suffixes)  # check weights have acceptable suffix
    pt, saved_model = (suffix == x for x in suffixes)  # backend booleans
    stride, names = 64, [f'class{i}' for i in range(1000)]  # assign defaults
    if pt:
        model = attempt_load(weights, map_location=device)  # load FP32 model
        stride = int(model.stride.max())  # model stride
        names = model.module.names if hasattr(model, 'module') else model.names  # get class names
        if half:
            model.half()  # to FP16

    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Run inference
    if pt and device.type != 'cpu':
        model(torch.zeros(1, 3, *imgsz).to(device).type_as(next(model.parameters())))  # run once
    dt, seen = [0.0, 0.0, 0.0], 0

    #t1 = time_sync()
    # padding the image ..
    sign_removed_list = []
    for i, im0 in enumerate(im0_640_list):
        #print('im0 shape',im0.shape)
        im2200 = im0_2200_list[i]
        #print('im2200 shape', im2200.shape)
        
        img = letterbox(im0, imgsz, stride=stride, auto=True)[0]
        # Convert
        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img = img / 255.0  # 0 - 255 to 0.0 - 1.0
        if len(img.shape) == 3:
            img = img[None]  # expand for batch dim
        #t2 = time_sync()
        #dt[0] += t2 - t1
        ### Inference ..
        if pt:
            visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
            pred = model(img, augment=augment, visualize=visualize)[0]

        #t3 = time_sync()
        #dt[1] += t3 - t2
        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        #dt[2] += time_sync() - t3

        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            if len(det):
                # Rescale boxes from img_size to im0 size
                #print(im2200.shape)
                #print(img.shape)

                
                '''
                det_640 = det
                det_640[:,:4] = scale_coords(img.shape[2:], det_640[:, :4], im0.shape).round()
                ### Write results for 640
                for *xyxy, conf, cls in reversed(det_640):
                    box_640 = xyxy
                    #print(box_640)
                    
                    if(int(box_640[3]) - int(box_640[1]) > (CONST_AVG_FONT_WIDTH/3.43) ):
                        #print("detected!!")
                        #print("height:", int(box[3]) - int(box[1]) )
                        #print("widht:" ,int(box[2]) - int(box[0]) )
                        p1, p2 = (int(box_640[0]), int(box_640[1])), (int(box_640[2]), int(box_640[3]))
                        cv2.rectangle(im0, p1, p2, (255, 225, 0), 1)
                cv2.imshow("removed_sign_640", cv2.resize(im0, (500, 800)) )
                cv2.waitKey(0)
                '''

                # Write results for 2200
                det_2200= det
                det_2200[:, :4] = scale_coords(img.shape[2:], det_2200[:, :4], im2200.shape).round()

                for *xyxy, conf, cls in reversed(det_2200):
                    
                    box_2200 = xyxy
                    if(int(box_2200[3]) - int(box_2200[1]) > (CONST_AVG_FONT_WIDTH) ):
                        p1, p2 = (int(box_2200[0]), int(box_2200[1])), (int(box_2200[2]), int(box_2200[3]))
                        cv2.rectangle(im2200, p1, p2, (255, 255, 255),-1)

                im2200 = cv2.cvtColor(im2200, cv2.COLOR_BGR2GRAY)
                #cv2.imshow("removed_sign_2200", cv2.resize(im2200, (500, 800)) )
                #cv2.waitKey(0)



        sign_removed_list.append(im2200)
    cv2.destroyAllWindows()
    return sign_removed_list

if __name__ == "__main__":

    im0 = cv2.imread('/home/surya/Desktop/Lending_Kat/Property docs for MVP/expt6/jpg_files/MDSD_2018/12_rgb2200.jpg')
    #'/home/surya/Desktop/Lending_Kat/Property docs for MVP/jpg_files_new4/MDSD_2018/12_after_artifacts1.jpg'
    im2200 = cv2.resize(im0, (2500, 3700))
    print(im2200.shape)
    im0 = cv2.resize(im0, (480, 640))
    run(im0_640_list = [im0], im0_2200_list = [im2200])
    print("done!!")
    '''

    direc = '/home/surya/Desktop/Lending_Kat/Property docs for MVP/jpg_files_new2/MDSD_2018'

    im0_640_list = []
    im0_2200_list = []
    for filename in os.listdir(direc):
        if (not filename.endswith('cropped.jpg')):


            print(filename)
            im0 = cv2.imread(os.path.join(direc, filename))
            im2200 = cv2.resize(im0, (1500, 2200))
            im0 = cv2.resize(im0, (480, 640))
            im0_640_list.append(im0)
            im0_2200_list.append(im2200)

            

    run(im0_640_list , im0_2200_list, line_thickness=line_thickness, conf_thres=conf_thres)
    print("done!!")
    '''
