from ultralytics import YOLO
from sort.sort import Sort
import easyocr

veh_model = YOLO("yolo11n.pt")                          #Vehicle detection model based on COCO dataset
lp_model = YOLO("lp_trained.pt")                        #License plate detection model based on Roboflow license plate dataset

reader = easyocr.Reader(['en'], gpu=False)              #Initialize reader for English language and no GPU

veh_tracker = Sort()                                    #Create vehicle tracker                    
vehicles = [2, 3, 5, 7]                                 #Set the classes of all vehicles
