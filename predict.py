from keras.models import Sequential,load_model
from keras.layers import Conv2D,MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
import numpy as np
import keras,sys
import tensorflow
from PIL import Image
#from zikken import file
import os
import glob


classes=["magari","sakibutori","seijyo"]
num_classes=len(classes)
image_size=50

def build_model():
    #model=Sequential()
    #model.add(Conv2D(32,(3,3),padding='same',input_shape=X.shape[1:]))
    #model.add(Activation('relu'))
    #model.add(Conv2D(32,(3,3)))
    #model.add(Activation('relu'))
    #model.add(MaxPooling2D(pool_size=(2,2)))
    #model.add(Dropout(0,25))

    model = Sequential()
    model.add(Conv2D(32,(3,3), padding='same',input_shape=(50,50,3)))
    model.add(Activation('relu'))
    model.add(Conv2D(32,(3,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))

    #model.add(Conv2D(64,(3,3),padding='same'))
    #model.add(Activation('relu'))
    #model.add(Conv2D(64,(3,3)))
    #model.add(Activation('relu'))
    #model.add(MaxPooling2D(pool_size=(2,2)))
    #model.add(Dropout(0,25))

    model.add(Conv2D(64,(3,3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64,(3,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))

    #model.add(Flatten())
    #model.add(Dense(512))
    #model.add(Activation('relu'))
    #model.add(Dropout(0,5))
    #model.add(Dense(3))
    #model.add(Activation('softmax'))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(3))
    model.add(Activation('softmax'))

    opt=tensorflow.keras.optimizers.RMSprop(lr=0.0001,decay=1e-6)

    model.compile(loss='categorical_crossentropy',optimizer=opt,metrics=['accuracy'])


    #?¿½?¿½?¿½f?¿½?¿½?¿½Ì??¿½?¿½[?¿½h
    model=load_model('./kyuri_cnn_aug.h5')

    return model

def main(i):
    path = r'kiridasi_wait/'
    extension = '*.jpg'
    path_search = os.path.join(path, extension)

    file_path = glob.glob(path_search)
    file = [os.path.basename(f) for f in file_path]
    print(file[i])

    image=Image.open("kiridasi_wait/"+file[i])
    image=image.convert('RGB')
    image=image.resize((image_size,image_size))
    deta=np.asarray(image)
    X=[]
    X.append(deta)
    X=np.array(X)
    model=build_model()

    result=model.predict([X])[0]
    predicted=result.argmax()
    percentage=int(result[predicted]*100)
    print("{0}({1}%)".format(classes[predicted],percentage))

    return classes[predicted]
    
    

#if __name__ =="__main__":
#    main()
