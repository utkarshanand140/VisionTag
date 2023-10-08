
# VisionTag

**VisionTag** is a GUI application made using OpenCV & PyQt5 library in Python. It uses Computer Vision techniques to automate the annotation process of images for training Deep Learning models. The application provides a graphical user interface (GUI) to annotate images in a more user-friendly manner.

**TechStack**:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![Qt](https://img.shields.io/badge/Qt-%23217346.svg?style=for-the-badge&logo=Qt&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)

<center><img src = "https://media.discordapp.net/attachments/1160317501519953990/1160317596919410718/ss.png?ex=653438f8&is=6521c3f8&hm=20eb706883d8159b10064841261cd1ac39b15420481fef5dc576e6e045561e8a&="/></center>

- [What? (Features)](#what)
- [Why?](#why)
- [Installation Instructions](#install)
  - [Requirements](#requirements)
- [User Guide](#userguide)

## <a name="what"></a>What? (Features)

***Annotate your images and generate labels for them automatically.*** Here's what this script does, step by step:

1. Takes the images stored in the 'Images' folder and asks user for first manual annotation to mark the objects.
2. Uses various object tracking and other computer vision techniques to automatically annotate the same objects in all the other images present in the folder.
3. The followings things can be generated:
   1. Generate Result images with the objects marked.
   2. Generate the Cropped Images of the objects.
   3. Generate labels for the objects in various formats such as COCO, YOLO, JSON, XML etc.



## <a name="why"></a>Why?

This project was developed to reduce the time spent on labelling images while preparing dataset for deep learning model training, by automating the whole process. Though, 3rd Party Commercial softwares are available, but there are situations and / or organiztions where some datasets are confidential and they cannot be shared outside the organization's internal network.

## <a name=install></a>Installation Instructions

- Download [this ZIP file](https://github.com/utkarshanand140/VisionTag/archive/refs/heads/master.zip)
- Download the required python libraries using the following command 

```bash
pip3 install -r requirements.txt
```

- Note the [Requirements](#requirements) for additional details!
- When you're done, refer to the [User Guide](#userguide) below.

### <a name="requirements"></a>Requirements

- Windows or Mac or Linux
- Python v3.7+ installed ([download it from python.org](https://www.python.org/downloads/))
- Support for other scripting languages may follow. Contributions are welcome!

## <a name="userguide"></a>User Guide

Using `VisionTag` is supereasy:

*Optional* 
- If you have your input dataset in the form of a video, and you want to convert it into a set of images, users can use the **video_to_frames.py** script file for it.
- Simply, put the full file path of your video into the *vid_capture* instance.

```python
vid_capture = cv2.VideoCapture('')
```
- Run the python scirpt and your images will be generated in the *Images* folder.

```bash
python3 video_to_capture.py
```

**Name Format for Images**
Make sure that all of you images are named in the following format,
`frame<index>.png`

Example:- frame0.png, frame1.png, frame2.png
Default indexing starts from **0** and default extension used is **.png**

*Note:-*
**frame0.png** will be used as the reference image to initially annotate the object. To use any other image, accordingly change the reference image path in the **app.py** file. If your images are not named using the convention given above, application will throw errors. If you want to use other naming conventions or if you want to use other image format other than PNG, you have to change the code in the **app.py** file accordingly.


**Steps to use VisionTag**
1. Run the **app.py** file in terminal using the following command:
```bash
python3 app.py
```

2. The VisionTag software will open, use the folder button to choose the location where the input images are stored.

3. Select the tracker which you want to use for your application. Following is the information about he different trackers:

|**Tracker**|**Information**|
|:-:|:-:|
|KCF|<div align='left'> Kernelized Correlation Filters (KCF) algorithm is based on correlation filters and uses a kernel function to compute the correlation between the object template and the image patches. The KCF algorithm has a high tracking speed and is robust to occlusion and changes in scale and rotation. **Recommended** </div>|
|MOSSE|<div align='left'> The minimum Output Sum of Squared Error or MOSSE algorithm is a simple and efficient tracking algorithm that uses a template update scheme to adapt to changes in the object's appearance. The MOSSE algorithm is robust to changes in scale, rotation, and illumination, but it may not be able to handle occlusion and significant changes in appearance. </div>|
|CSRT|<div align='left'> CSRT algorithm which uses spatial reliability maps for adjusting the filter support to the part of the selected region from the frame for tracking, gives an ability to increase the search area and track non-rectangular objects. </div>|
|MEDIANFLOW|<div align='left'> The MedianFlow algorithm is based on the Lucas-Kanade method. The algorithm tracks the movement of the object in the forward and backward directions in time and estimates the error of these trajectories, which allows the tracker to predict the further position of the object in real time. </div>|
|TLD|<div align='left'> Tracking-Learning-Detection or TLD algorithm combines object tracking with object detection and learning to track the object of interest over time. The TLD algorithm can handle occlusions and changes in appearance, but it can be computationally expensive. </div>|
|BOOSTING|<div align='left'> BOOSTING algorithm is based on the AdaBoost algorithm The algorithm increases the weights of the incorrectly classified objects, which allows a weak classifier to focus on their detection. </div>|

4. Enter the object class ID of your selected object. For Deep Learning training purpose, each class of object has to be given a unique ID.

5. Select the “**Generate Labels**” box if you want to generate labels for your images. Labels will be generated in the **YOLO** format and will be stores in the **Labels/** folder.

6. Select the “**Save Cropped Results**” box if you want to save the cropped image of the object from each frame. Images will be stored in the **Cropped-Images/** folder.

7. Click on the **START** button. As soon as you click on the **START** button, your Reference image will appear and it will ask you to initially manually annotate the object in the image.


<center><img src = "https://media.discordapp.net/attachments/1160317501519953990/1160317714338943128/manual.png?ex=65343914&is=6521c414&hm=b3b698d3c45c1fb4c916269272585cc13610b6bcff9b2210f66dc5e46c245668&="/></center>

After marking the object using the cursor, press **ENTER** / **SPACE** to start the annotating process. You can also press “**C**” on your keyboard if you don’t want to annotate your reference image. In that case, you Annotation process will exit and you would have to start again.

8. During the annotation process, If you want to Quit the annotation process at any given point of time, you can simple **Press and Hold** the “**Q**” key on your keyboard and your annotation process and exit back to the Main HomeScreen.

9. If the tracker looses the object, it will automatically ask you to manually annotate the image again. If you feel that the tracker is loosing the object or that if it is not working properly, you can manually annotate the image again and re-initialize the tracker. To do so, just **Press and Hold** the “**M**” key on the keyboard during the annotation process to stop it and manually annotate the image.

After manually annotating the images, similar to above, either press the **ENTER** / **SPACE** key to start the process or ” **C** “ to end it.

10.  Once the Annotation process is complete, the Resultant Images can be found in the **Results/** folder.


*Disclaimer: Please use at your own risk. This tool is neither officially supported by AUTHOR in any way. See also the full [GPL-3.0 license](/LICENSE).*