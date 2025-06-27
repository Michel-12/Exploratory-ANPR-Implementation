from detection import plate_detection
from ui import start_ui
import threading

if __name__ == "__main__":                  
    detect_thread = threading.Thread(target=plate_detection)    #Setup Multitasking
    detect_thread.start()                                       #Start License plate detection
    start_ui()                                                  #Start UI
