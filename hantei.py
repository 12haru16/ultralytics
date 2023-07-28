import os
import glob
import predict

from keras.models import Sequential,load_model
from keras.layers import Conv2D,MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
import numpy as np
import keras,sys
import tensorflow
from PIL import Image
from sql import data_insert

def hantei():
    #path = r'kiridasi/'
    #extension = '*.jpg'
    #path_search = os.path.join(path, extension)

    #file_path = glob.glob(path_search)
    #file = [os.path.basename(f) for f in file_path]
    #print(file[1])

    initial_count=0
    dir="kiridasi_wait"
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir,path)):
            initial_count+=1
    print(initial_count)

    a=0 
    b=0
    c=0
    for i in range(initial_count):
        classes=predict.main(i)
        if classes=="magari":
            a+=1
        if classes=="sakibutori":
            b+=1
        if classes=="seijyo":
            c+=1

    print("magari:",a)
    print("sakibutori:",b)
    print("seijyo:",c)

    data_insert(a,b,c)
        
#hantei()
    # ['pic1.jpg', 'pic2.jpg', 'pic3.jpg']
