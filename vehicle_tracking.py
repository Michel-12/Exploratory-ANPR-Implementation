import numpy as np
from config import veh_model, veh_tracker, vehicles

def detect_vehicle(frame):
    '''
    Uses YOLOv11n model with COCO dataset to detect vehicles: Car, Motorbike, Bus, Truck.
    If vehicle is found, its location is stored and tracked across the screen.
    Function returns vehicle position with unique id.
    '''
    detections = veh_model(frame)[0]                                #Capture all detections in the frame
    object_locations = []
    for detection in detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = detection                 #Retrieve coordinates, conf. score and class id from detection
        if int(class_id) in vehicles:                               #Remember the object if it is a vehicle
            object_locations.append([x1, y1, x2, y2, score])
    veh_ids = veh_tracker.update(np.asarray(object_locations))      #Different vehicles that are tracked aross frames
    return veh_ids

def find_veh(plate, veh_ids):
    '''
    Takes the location of all detected license plates and vehicles to see which vehicles have plates.
    All vehicles with license plates detected in their bounding boxes are returned.
    '''
    xl1, yl1, xl2, yl2, _, _ = plate                                #Get the location of the license plates
    for i in range(len(veh_ids)):
        xv1, yv1, xv2, yv2, veh_id, score = veh_ids[i]              #Get the location of the visible vehicles
        if xl1 > xv1 and yl1 > yv1 and xl2 < xv2 and yl2 < yv2:     #If the license plate is located on the car, save the car index
            return veh_ids[i]                                       #Return the location of the car if found
    return -1, -1, -1, -1, -1, -1
