import numpy as np
import cv2
from PIL import Image
import pytesseract
from pytesseract import Output
import os
import argparse
import matplotlib.pyplot as plt

from skimage import measure, morphology
from skimage.color import label2rgb
from skimage.measure import regionprops

import pdf2image
from pdf2image import convert_from_path

