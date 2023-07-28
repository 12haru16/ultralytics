import cv2
import datetime
import os
import shutil
from ultralytics import YOLO
from hantei import hantei

def camera():
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        cv2.imshow("frame", frame)
        # qが押されたら
        if cv2.waitKey(1) & 0xFF == ord('q'):
            #保存
            time = datetime.datetime.now()
            timestr = time.strftime("%Y_%m_%d_%H_%M_%S")
            #print(str(timestr) + ".jpg")
            cv2.imwrite('image_wait/'+str(timestr) + ".jpg", frame)
        if cv2.waitKey(1) & 0xff==ord('w'):#wを押されたら停止
            break

def kiridasi():
    model = YOLO('runs/detect/train/last.pt')#画像を切り出し
    model("image_wait/",save_crop=True, conf=0.2, iou=0.5)

    start_dir='runs/detect/predict/crops/kyuri'#移動して消去
    end_dir='kiridasi/'
    for p in os.listdir(start_dir):
        shutil.move(os.path.join(start_dir, p), end_dir)
    shutil.rmtree('runs/detect/predict/')#predictの下を消す

def photo_save():
    start_dir2='image_wait/'#画像を移動
    end_dir2='image_hozon/'
    for p in os.listdir(start_dir2):
        shutil.move(os.path.join(start_dir2, p), end_dir2)

def kiridasi_save():
    start_dir2='kiridasi_wait/'#画像を移動
    end_dir2='kiridasi_hozon/'
    for p in os.listdir(start_dir2):
        shutil.move(os.path.join(start_dir2, p), end_dir2)

#camera()
#kiridasi()
#photo_save()
#hantei()
#kiridasi_save()
    