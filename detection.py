import cv2
from config import lp_model, reader
from vehicle_tracking import detect_vehicle, find_veh
from ui import display_results
import re


def read_lp(plate):
    '''
    Takes a processed frame and reads it using EasyOCR reader.
    Characters are then uppercased with spaces removed.
    Returns predicted text with confidence score.
    '''
    characters = reader.readtext(plate)                                                     #Read the characters from the plate
    if characters:
        for _, ctext, cscore in characters:                                                 #Retrieve the text and conf of each character
            clean_text = re.sub(r'[^a-zA-Z0-9]', '', ctext)                                 #Remove any symbols
            return clean_text.upper().replace(' ', ''), cscore                              #Uppercase the text and remove spaces
    return None, None

def detect_license(frame, veh_ids):
    '''
    Takes a frame and used License Plate model to detect plates.
    With the location of plates and vehicles, it matches plates vehicles.
    If plates are found on vehicles, the plates are processed and read.
    Any read plates and vehicles are displayed if useful.
    '''
    plates = lp_model(frame)[0]                                                             #Find all the plates in a frame
    for plate in plates.boxes.data.tolist():
        xl1, yl1, xl2, yl2, box_score, id_lp = plate                                        #Get the location for each plate
        xv1, yv1, xv2, yv2, id_veh, score_veh = find_veh(plate, veh_ids)                    #Find the location of the vehicle associated with the plate
        if id_veh != -1:                                                                    #If a car is found
            lp_crop = frame[int(yl1):int(yl2), int(xl1):int(xl2), :]                        #Crop frame to just the license plate
            lp_crop_bw = cv2.cvtColor(lp_crop, cv2.COLOR_BGR2GRAY)                          #Turn image black and white
            _, lp_crop_contrast = cv2.threshold(lp_crop_bw, 70, 255, cv2.THRESH_BINARY_INV) #Increase contrast by turning color values <82 to 255 and >82 to 0
            lp_text, lp_score = read_lp(lp_crop_contrast)                                   #Get the text and confidence score from lp
            if lp_text and len(lp_text) > 6:                                                #When a plate is read, save entry of car to dict
                veh_frame = frame[int(yv1):int(yv2), int(xv1):int(xv2), :]
                display_results(lp_text, lp_score, veh_frame, score_veh, id_veh)            #Show the 3 recent vehicles with top 3 guesses as clickable buttons

def plate_detection():
    '''
    Function that runs the detection loop.
    '''
    frame_nr = -1
    cap = cv2.VideoCapture('Data/Production/traf_big.mp4')                                                #Capture the videoframes
    while cap.isOpened():
        success, frame = cap.read()                                                         #Read the frame
        if not success:                                                                     #If a frame is received do the following:
            break                                                                           
        frame_nr += 1                                                                       #Count the frame
        veh_ids = detect_vehicle(frame)                                                     #Detect unique vehicles in frame
        detect_license(frame, veh_ids)                                                      #Detect, Read and Save license plates of vehicles in Dict
    cap.release()                                                                           #Release the capture device
