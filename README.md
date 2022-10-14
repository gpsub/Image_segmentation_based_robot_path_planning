# Image Segmentation based Robot path planning

In this project,the drivable area for an experimental robot car (powered by Raspberry Pi 4 and motor driver) has been detected using Image Segmentation and the binary output mask is obtained. The midpoints of the row-wise maximum width sections of the binary output mask have been joined to create a path which the car can follow. This prediction keeps running and changes dynamically according to the image stream recieved from the robot car. 

## Packages Used: 
- Opencv-python
- tensorflow
- pixellib

Download model weights from [here](https://github.com/ayoolaolafenwa/PixelLib/releases/download/1.3/deeplabv3_xception65_ade20k.h5)