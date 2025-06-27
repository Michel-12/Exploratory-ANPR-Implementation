import cv2
from PIL import Image, ImageTk
import pyperclip

def create_image(frame):
    '''
    Convert a numpy image array to a PhotoImage for Tkinter.
    '''
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)                    #Convert BGR image to RGB
    img_pil = Image.fromarray(rgb).resize((160, 120))               #Turn np array into image and resize
    return ImageTk.PhotoImage(img_pil)                                   

def update_img(frame, label):
    '''
    Takes a numpy array frame and updates it on the given label.
    '''
    new_image = create_image(frame)                                 #Convert frame to formatted image
    label.config(image=new_image)                                   #Set image to label
    label.image = new_image                                         #Update label

def copy(string):
    '''
    Takes a string and copies it to the computer clipboard
    '''
    pyperclip.copy(string)
