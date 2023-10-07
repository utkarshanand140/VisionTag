'''
Software Name: VisionTag
Version: 1.0
Author: Utkarsh Anand (https://www.linkedin.com/in/utkarsh-anand-93260617b/)
For Queries: utkarshanand221@gmail.com
'''


# Import Python Libaries (Given in Requirements.txt file)
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os
import cv2
from pathlib import Path

# x-------------------------------------- GUI SECTION --------------------------------------------x

# Define the class for GUI support
class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("GUI/main.ui", self) # load the main.ui file designed using Qt Designer
        self.show()

        # Connect the GUI buttons to their respective class methods
        self.pushButton.clicked.connect(self.annotate)
        self.pushButton_3.clicked.connect(self.open_Results)
        self.pushButton_2.clicked.connect(self.open_Crop)
        self.pushButton_4.clicked.connect(self.open_Label)
        self.toolButton.clicked.connect(self.chooseFolder)

    # Start Annotations Process on clicking the START button
    def annotate(self): 
        self.send_info() 
        execute()
        cv2.destroyAllWindows()

    # open the results folder
    def open_Results(self): 
        os.system("open Result/")

    # open the cropped images folder
    def open_Crop(self): 
        os.system("open Cropped-Images/")

    # opens the label folder
    def open_Label(self): 
        os.system("open Labels/")

     # Selects the folder where images are located.
    def chooseFolder(self):
        dialog = QFileDialog()
        folder_path = str(dialog.getExistingDirectory(None, "Select Folder"))
        self.lineEdit.setText(folder_path)

    
    # Takes information entered by the user through GUI and sends it to the Annotation Script
    def send_info(self): 

        # Global variables defined so that they could be used anywhere in the script
        global path, tracker_type, obj_id, label, crop 
        path = str(self.lineEdit.text())
        tracker_type = str(self.comboBox.currentText())
        try:
            obj_id = int(self.lineEdit_2.text())
        except ValueError:
            pass
        label = bool(self.checkBox.isChecked())
        crop = bool(self.checkBox_2.isChecked())



# x-------------------------------------- ANNOTATION SECTION --------------------------------------------x

# draws the bounding box around the object in the image
def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)
    cv2.putText(
        img, "Tracking", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
    )

# Crops the image according to the bounding box locations
def cropImage(img,frame,bbox,dir_path):
    x,y,w,h = [int(i) for i in bbox]
    new_img = img[y:y+h,x:x+w]
    write_path = str(dir_path) + "/" + frame
    cv2.imwrite(write_path,new_img)


# gets the index of the image from the image name
def get_index(string):
    s1 = string.split(".")
    s2 = s1[0].split("e")
    return int(s2[1])


# Selects the Tracker in the script depending upon the one selected by the user
def getTrackerType(tracker_type):

    if tracker_type == "BOOSTING":
        tracker = cv2.legacy.TrackerBoosting_create()
    elif tracker_type == "MIL":
        tracker = cv2.legacy.TrackerMIL_create()
    elif tracker_type == "KCF":
        tracker = cv2.legacy.TrackerKCF_create()
    elif tracker_type == "TLD":
        tracker = cv2.legacy.TrackerTLD_create()
    elif tracker_type == "MEDIANFLOW":
        tracker = cv2.legacy.TrackerMedianFlow_create()
    elif tracker_type == "CSRT":
        tracker = cv2.legacy.TrackerCSRT_create()
    elif tracker_type == "MOSSE":
        tracker = cv2.legacy.TrackerMOSSE_create()
    else:
        tracker = None

    if tracker != None:
        print(f"\nTracker Algorithm Used: {tracker_type}\n")

    return tracker


# Generates the labels for the images in the YOLO Format
def text_generator(n, bbox, result_path_txt):
    label_txt = f"{n} {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}"
    with open(result_path_txt, "w") as f:
        f.write(label_txt)
        f.write("\n")


# Notifications Dialogue Box
def popup(mssg):
    message = QMessageBox()
    message.setText(mssg)
    message.exec_()


# Executes the Annotation Process
def execute():

    # Initialize the Directory Paths for the Input, Result, Labels and Cropped Images
    dir_result = Path("Result")
    dir_label = Path("Labels")
    dir_crop = Path("Cropped-Images")
    dir_img = path

    # Deletes any previous files which were stored in these directories
    os.system("rm -rf Result/*")
    os.system("rm -rf Labels/*")
    os.system("rm -rf Cropped-Images/*")


    # Check if the Input Image path was selected by the user or not
    try:
        assert os.path.exists(dir_img)
    except (AssertionError):
        popup("Select Images Folder !!")
        return

    # Initialize the the path of the reference image
    reference_image_path = str(dir_img) + "/frame0.png" # Change for a different reference image

    tracker = getTrackerType(tracker_type)

    #check for proper selection of tracker
    if tracker == None:
        popup("Tracker Not Selected, Try Again!")
        return

    # Check if Reference Image exists at the path specified and read the reference image
    try:
        assert os.path.exists(reference_image_path)
        img = cv2.imread(reference_image_path)
    except (AssertionError):
        popup("Unable to Read Reference Image")
        return

    
    cv2.putText(
        img, "Not Tracking", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2
    )

    # Select the Region of Interest by the user around the object.
    bbox = cv2.selectROI("Tracking", img, False)

    # Initalize the tracker on the image
    try:
        tracker.init(img, bbox)
    except (cv2.error):
        return

    # Sort the Images in the directory according to their respective indexes
    i = -1
    list_img = [x for x in os.listdir(dir_img) if x != ".DS_Store"]
    list_img.sort(key=get_index)

    # Iterate over each Image in the directory
    for frame in list_img:
        
        # Hold 'q' key to exit the annotation process at any given time.
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

        i = i + 1

        # Define the different image paths
        image_path = str(dir_img) + "/" + frame
        result_path = str(dir_result) + "/" + frame
        result_path_txt = str(dir_label) + "/" + f"frame{i}.txt"

        # Chec and read the input image
        try:
            assert os.path.exists(image_path)
            img = cv2.imread(image_path)
        except AssertionError:
            popup("Unable to Read Image")
            # run = False
            return

        # Update the tracker
        try:
            success, bbox = tracker.update(img)
        except (cv2.error):
            popup("Tracker Initialization Failed")
            # run = False
            return

        # Hold 'm' key to manually annotate the image
        if cv2.waitKey(25) & 0xFF == ord("m"):
            success = False

        if success:
            drawBox(img, bbox)

            # Write the annotated image
            cv2.imwrite(result_path, img)

            # Generate label if user wants
            if label:
                text_generator(obj_id, bbox, result_path_txt)

            # Save the cropped image if user wants
            if crop:
                cropImage(img, frame, bbox, dir_crop)

        else:
            
            # Manually annotate the image
            popup("Manually Mark Bounding Box")
            cv2.putText(
                img,
                "Not Tracking",
                (75, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )
            bbox = cv2.selectROI("Tracking", img, False)
            drawBox(img, bbox)
            cv2.imwrite(result_path, img)

            if label:
                text_generator(obj_id, bbox, result_path_txt)

            if crop:
                cropImage(img, frame, bbox, dir_crop)

            tracker = getTrackerType(tracker_type)

            try:
                tracker.init(img, bbox)
            except (cv2.error, IndexError):
                print("Error in Selecting Tracker")
                return

        cv2.imshow("Tracking", img)

    popup("Execution Complete !")



# x---------------------------------------- MAIN SECTION --------------------------------------------x

def main():
    
    # Initialize Qt Application
    app = QApplication([])
    window = MyGUI()

    # Execute the application
    app.exec_()


if __name__ == "__main__":
    main()
