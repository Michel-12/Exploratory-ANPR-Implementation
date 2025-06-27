import tkinter as tk
import numpy as np
from utils import create_image, update_img, copy

# Globals
veh_1_id = veh_2_id = veh_3_id = -1                                                     #Set Veh_ids to -1
veh_1_frame = np.zeros((120, 160, 3), dtype=np.uint8)                                   #Set default imgs
veh_2_frame = np.zeros((120, 160, 3), dtype=np.uint8)
veh_3_frame = np.zeros((120, 160, 3), dtype=np.uint8)
veh_1_score = veh_2_score = veh_3_score = -1                                            #Set img scores to -1
veh_1_a = veh_1_b = veh_1_c = ''                                                        #Set empty strings for predictions
veh_2_a = veh_2_b = veh_2_c = ''
veh_3_a = veh_3_b = veh_3_c = ''
veh_1_a_score = veh_1_b_score = veh_1_c_score = -1                                      #Set prediction scores to -1
veh_2_a_score = veh_2_b_score = veh_2_c_score = -1
veh_3_a_score = veh_3_b_score = veh_3_c_score = -1

def start_ui():
    '''
    Sets up and runs tkinter window with 2 cols and 9 rows
    Shows 3 images with 3 buttons each.
    Images contain recent veh, with top 3 predictions in buttons.
    Pressing a button copies the prediction to clipboard.
    '''
    global root, v1_label, v2_label, v3_label
    global but_1a, but_1b, but_1c, but_2a, but_2b, but_2c, but_3a, but_3b, but_3c

    root = tk.Tk()                                                                      #Initialize UI window
    root.title("Plate Detector")

    root.grid_columnconfigure(0, minsize=160)                                           #Setup UI Column and Row sizes
    root.grid_columnconfigure(1, minsize=40)
    for row in range(9):
        root.grid_rowconfigure(row, minsize=40)

    v1_tk = create_image(veh_1_frame)                                                   #Setup Image 1
    v1_label = tk.Label(root, image=v1_tk)
    v1_label.grid(row=0, column=0, rowspan=3)

    v2_tk = create_image(veh_2_frame)                                                   #Setup Image 2
    v2_label = tk.Label(root, image=v2_tk)
    v2_label.grid(row=3, column=0, rowspan=3)

    v3_tk = create_image(veh_3_frame)                                                   #Setup Image 3
    v3_label = tk.Label(root, image=v3_tk)
    v3_label.grid(row=6, column=0, rowspan=3)

    but_1a = tk.Button(root, text=veh_1_a, command=lambda: copy(veh_1_a))               #Create Buttons
    but_1b = tk.Button(root, text=veh_1_b, command=lambda: copy(veh_1_b))
    but_1c = tk.Button(root, text=veh_1_c, command=lambda: copy(veh_1_c))
    but_2a = tk.Button(root, text=veh_2_a, command=lambda: copy(veh_2_a))
    but_2b = tk.Button(root, text=veh_2_b, command=lambda: copy(veh_2_b))
    but_2c = tk.Button(root, text=veh_2_c, command=lambda: copy(veh_2_c))
    but_3a = tk.Button(root, text=veh_3_a, command=lambda: copy(veh_3_a))
    but_3b = tk.Button(root, text=veh_3_b, command=lambda: copy(veh_3_b))
    but_3c = tk.Button(root, text=veh_3_c, command=lambda: copy(veh_3_c))

    buttons = [but_1a, but_1b, but_1c, but_2a, but_2b, but_2c, but_3a, but_3b, but_3c]
    for idx, button in enumerate(buttons):                                              #Put Buttons in grid
        button.grid(row=idx, column=1)

    root.mainloop()

def display_results(lp_text, lp_score, frame, score_veh, id_veh):
    '''
    Takes the cropped frame on which a veh with plate is detected along with its
    unique id, conf score and text + score.
    If veh not displayed on UI, adds it on top spot.
    If veh already displayed, updates its entries.
    Then refreshes UI
    '''    
    global veh_1_id, veh_2_id, veh_3_id
    if not id_veh in (veh_1_id, veh_2_id, veh_3_id):                                    #If vehicle is not yet displayed, place it on top
        add_vehicle(id_veh, frame, score_veh, lp_text, lp_score)
    elif id_veh == veh_1_id:                                                            #If 1st displayed vehicle, update frame and text with better findings
        update_vehicle(1, frame, score_veh, lp_text, lp_score)
    elif id_veh == veh_2_id:                                                            #If 2nd displayed vehicle, update frame and text with better findings
        update_vehicle(2, frame, score_veh, lp_text, lp_score)          
    elif id_veh == veh_3_id:                                                            #If 3rd displayed vehicle, update frame and text with better findings
        update_vehicle(3, frame, score_veh, lp_text, lp_score)

def add_vehicle(id_veh, frame, score_veh, lp_text, lp_score):
    '''
    Adds unseen vehicle to 1st display spot, moving the other 2 down
    '''
    global veh_1_id, veh_1_frame, veh_1_score, veh_1_a, veh_1_a_score, veh_1_b, veh_1_b_score, veh_1_c, veh_1_c_score
    global veh_2_id, veh_2_frame, veh_2_score, veh_2_a, veh_2_a_score, veh_2_b, veh_2_b_score, veh_2_c, veh_2_c_score
    global veh_3_id, veh_3_frame, veh_3_score, veh_3_a, veh_3_a_score, veh_3_b, veh_3_b_score, veh_3_c, veh_3_c_score

    veh_3_id, veh_3_frame, veh_3_score = veh_2_id, veh_2_frame, veh_2_score             
    update_img(veh_3_frame, v3_label)                                                   #Set 2nd pos veh to 3rd pos
    veh_3_a, veh_3_b, veh_3_c = veh_2_a, veh_2_b, veh_2_c
    but_3a.config(text=veh_3_a)
    but_3b.config(text=veh_3_b)
    but_3c.config(text=veh_3_c)
    veh_3_a_score, veh_3_b_score, veh_3_c_score = veh_2_a_score, veh_2_b_score, veh_2_c_score

    veh_2_id, veh_2_frame, veh_2_score = veh_1_id, veh_1_frame, veh_1_score
    update_img(veh_2_frame, v2_label)                                                   #Set 1st pos veh to 2nd pos
    veh_2_a, veh_2_b, veh_2_c = veh_1_a, veh_1_b, veh_1_c
    but_2a.config(text=veh_2_a)
    but_2b.config(text=veh_2_b)
    but_2c.config(text=veh_2_c)
    veh_2_a_score, veh_2_b_score, veh_2_c_score = veh_1_a_score, veh_1_b_score, veh_1_c_score

    veh_1_id, veh_1_frame, veh_1_score = id_veh, frame, score_veh
    update_img(veh_1_frame, v1_label)                                                   #Set veh to 1st pos
    veh_1_a, veh_1_b, veh_1_c = lp_text, '', ''
    but_1a.config(text=veh_1_a)
    but_1b.config(text=veh_1_b)
    but_1c.config(text=veh_1_c)
    veh_1_a_score, veh_1_b_score, veh_1_c_score = lp_score, -1, -1

def update_vehicle(slot, frame, score_veh, lp_text, lp_score):
    '''
    Takes a frame with veh location + conf score and text + score for veh_1
    If veh detection has higher conf score, image is replaced.
    Text detection is placed in top 3 depending on score. 
    '''
    if slot == 1:
        global veh_1_frame, veh_1_score, veh_1_a, veh_1_a_score, veh_1_b, veh_1_b_score, veh_1_c, veh_1_c_score
        if score_veh > veh_1_score:                                                     #Set new frame as display image if conf score is higher
            veh_1_frame = frame
            update_img(veh_1_frame, v1_label)
            veh_1_score = score_veh
        _update_lp(slot, lp_text, lp_score)
    elif slot == 2:
        global veh_2_frame, veh_2_score, veh_2_a, veh_2_a_score, veh_2_b, veh_2_b_score, veh_2_c, veh_2_c_score
        if score_veh > veh_2_score:
            veh_2_frame = frame
            update_img(veh_2_frame, v2_label)
            veh_2_score = score_veh
        _update_lp(slot, lp_text, lp_score)
    elif slot == 3:
        global veh_3_frame, veh_3_score, veh_3_a, veh_3_a_score, veh_3_b, veh_3_b_score, veh_3_c, veh_3_c_score
        if score_veh > veh_3_score:
            veh_3_frame = frame
            update_img(veh_3_frame, v3_label)
            veh_3_score = score_veh
        _update_lp(slot, lp_text, lp_score)

def _update_lp(slot, lp_text, lp_score):
    '''
    Takes license plate prediction and score. 
    Depending on score of current vs past predictions, it is placed on 1,2 or 3rd slot. 
    '''
    global veh_1_a, veh_1_a_score, veh_1_b, veh_1_b_score, veh_1_c, veh_1_c_score
    global veh_2_a, veh_2_a_score, veh_2_b, veh_2_b_score, veh_2_c, veh_2_c_score
    global veh_3_a, veh_3_a_score, veh_3_b, veh_3_b_score, veh_3_c, veh_3_c_score

    if slot == 1:
        a, b, c = veh_1_a_score, veh_1_b_score, veh_1_c_score
        if lp_score > a:
            veh_1_c, veh_1_b, veh_1_a = veh_1_b, veh_1_a, lp_text
            veh_1_c_score, veh_1_b_score, veh_1_a_score = veh_1_b_score, veh_1_a_score, lp_score
            but_1a.config(text=veh_1_a)
            but_1b.config(text=veh_1_b)
            but_1c.config(text=veh_1_c)
        elif lp_score > b:
            veh_1_c, veh_1_b = veh_1_b, lp_text
            veh_1_c_score, veh_1_b_score = veh_1_b_score, lp_score
            but_1b.config(text=veh_1_b)
            but_1c.config(text=veh_1_c)
        elif lp_score > c:
            veh_1_c, veh_1_c_score = lp_text, lp_score
            but_1c.config(text=veh_1_c)
    elif slot == 2:
        a, b, c = veh_2_a_score, veh_2_b_score, veh_2_c_score
        if lp_score > a:
            veh_2_c, veh_2_b, veh_2_a = veh_2_b, veh_2_a, lp_text
            veh_2_c_score, veh_2_b_score, veh_2_a_score = veh_2_b_score, veh_2_a_score, lp_score
            but_2a.config(text=veh_2_a)
            but_2b.config(text=veh_2_b)
            but_2c.config(text=veh_2_c)
        elif lp_score > b:
            veh_2_c, veh_2_b = veh_2_b, lp_text
            veh_2_c_score, veh_2_b_score = veh_2_b_score, lp_score
            but_2b.config(text=veh_2_b)
            but_2c.config(text=veh_2_c)
        elif lp_score > c:
            veh_2_c, veh_2_c_score = lp_text, lp_score
            but_2c.config(text=veh_2_c)
    elif slot == 3:
        a, b, c = veh_3_a_score, veh_3_b_score, veh_3_c_score
        if lp_score > a:
            veh_3_c, veh_3_b, veh_3_a = veh_3_b, veh_3_a, lp_text
            veh_3_c_score, veh_3_b_score, veh_3_a_score = veh_3_b_score, veh_3_a_score, lp_score
            but_3a.config(text=veh_3_a)
            but_3b.config(text=veh_3_b)
            but_3c.config(text=veh_3_c)
        elif lp_score > b:
            veh_3_c, veh_3_b = veh_3_b, lp_text
            veh_3_c_score, veh_3_b_score = veh_3_b_score, lp_score
            but_3b.config(text=veh_3_b)
            but_3c.config(text=veh_3_c)
        elif lp_score > c:
            veh_3_c, veh_3_c_score = lp_text, lp_score
            but_3c.config(text=veh_3_c)
