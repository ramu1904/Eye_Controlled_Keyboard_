# Eye Controlling Keyboard



## Overview 
The "Eye Controlling Keyboard" is an innovative project that allows users to control a virtual keyboard using only their eye movements. Developed entirely in Python with OpenCV, this application provides a hands-free way to type by leveraging real-time eye tracking and blink detection.

## Core-Logic
This project consists of two key components.
  * Eye detection: Identifying eye movements and blinks using face landmark detection.
  * Virtual keyboard: A digital keyboard displayed on the screen, where selections are made through gaze direction and blinking.

### 1.1Eye detection
Using a real-time video feed from the webcam, we implement facial landmark detection to pinpoint 68 specific facial markers. The relevant landmarks for eye tracking are:

* Left eye points: (36, 37, 38, 39, 40, 41)
* Right eye points: (42, 43, 44, 45, 46, 47)

These points help us track eye movement accurately and detect blinking.

![landmarks_points_eyes](https://user-images.githubusercontent.com/44902363/85774006-10714180-b73c-11ea-93ff-542ff0a70958.png)


### 1.2 Detecting the blinking
Once the eye is detected, we analyze its movement using two reference lines: a horizontal line and a vertical line.

* When the eye is open, the vertical line appears longer

![eye_open](https://user-images.githubusercontent.com/44902363/85774949-f2f0a780-b73c-11ea-8fce-027d367ca5be.jpg)


* When the eye is closed, the vertical line shrinks significantly.

![eye_closed](https://user-images.githubusercontent.com/44902363/85774947-f1bf7a80-b73c-11ea-85a6-815ad3ce5cf1.jpg)

By calculating the ratio between these two lines, we determine if the eye is blinking. If the ratio exceeds 5.7, it signifies a blink; otherwise, the eye remains open.

### 1.3 Gaze Detection

To enhance usability, the virtual keyboard is divided into two sections: left and right. Depending on where the user is looking, only the corresponding half of the keyboard is activated.

* If the user looks to the left, only the left side of the keyboard is highlighted.

* If the user looks to the right, only the right side is active.

![left_right_gazecontrolled_keyboard](https://user-images.githubusercontent.com/44902363/85775667-9b067080-b73d-11ea-9920-38ed79ccb7f4.png)


Hence for that we need to detect the gaze of our eyes wether they are looking in left or right differection.

![eye_gaze-1024x421](https://user-images.githubusercontent.com/44902363/85776013-ee78be80-b73d-11ea-8251-27bb4fcd1d97.png)

To achieve this, we analyze the distribution of the white part of the eye (sclera). When looking left, more sclera is visible on the right side of the eye, and vice versa. The gaze ratio is calculated based on the pixel distribution:


![eye_splitted](https://user-images.githubusercontent.com/44902363/85776329-3b5c9500-b73e-11ea-9f67-c91a6c61cbb1.png)

If the sclera is more visible on the right part, so the eye is looking at the left (our left) like in this case.Technically to detect the sclera we convert the eye into grayscale, we find a treshold and we count the white pixels.

We divide the white pixels of the left part and those of the right part and we get the gaze ratio. If the gaze ratio is smaller than 1 when looking to the right side and greater than 1.7 when the eyes are looking to the left side.



* If the gaze ratio < 1, the user is looking right.

* If the gaze ratio > 1.7, the user is looking left.

### 2.1 Virtual Keyboard

A simple on-screen keyboard is created using OpenCV and NumPy. The keyboard displays keys, and users select letters based on gaze movement and blinking.

![keyboard_left-300x180](https://user-images.githubusercontent.com/44902363/85778101-db66ee00-b73f-11ea-9dbf-ebc6a8ef6b75.jpg)


### 2.2 Letter Selection Mechanism
To ensure efficient typing:

* Letters light up sequentially every 10 frames.
* When the desired letter is highlighted, the user blinks to select it.


**Final result**

By combining real-time eye tracking, gaze detection, and blink-based selection, users can type without using their hands, offering an accessible alternative for individuals with motor impairments.


## Inspiration From

* Pyscource [blogs](https://pysource.com/category/tutorials/gaze-controlled-keyboard/) by Sergio Canu



### Author

#### Ramu (__ramu1904)

<a href="www.linkedin.com/in/ramu-r-586a52322"></a>


