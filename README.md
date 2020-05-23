# Microcontroller-Image-Sender
Introducing a simple Python GUI to resize and send via serial images to microcontrollers

![GUI of the sender](/asset/screenshot_main.png)

## How to use
To use this tool you have to install the packages in requirement.txt (you can do that via `pip install -r requirement.txt`) and then run `python Serial_Image_Sender_GUI.py`. The GUI will open and you can access all the functionalities of the program without a single line of code.

Done that, you should just click Connect! If the button turns green it means that the connection has been established and that images can be sent. Just click on _Next image_ or _Berserk mode_ to send one image or to continously send imges one after another!

## What should I input?

The GUI only requires a path to the test images folder and the COM port of the microcontroller.
Additionally, you can provide:
* The ground truth values: the file should contain in the first line the classes values separated by comma and then class numbers every new line
* Image annotations: some datasets provide X and Y coordinates of the most important part of an image. The sender can understand from this file those positions and crop accordingly the image. The file format should be X1,Y1,X2,Y2, with each entry separated by a new line.
* Image resizing: you can resize the image to the entered pixel values. In case you don't want to resize the image please enter -1 in at least one of the resize boxes

## What should I send via serial?

