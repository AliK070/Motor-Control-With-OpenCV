 # Motor Control w/OpenCV

## A bit about the program:
Motor PWM control using the OpenCV library to track my hands and the tips of my pinkey to thumb (the distance). The power outputed to the motors are based off of this distance value, the greater the distance the greater the motor speed will be and vice versa. This is done through the pyfirmata2 library, in which I use python to communicate with the Arduino. 

The distance `d` between two points `(x₁, y₁)` and `(x₂, y₂)` in a 2D plane is:


d = √((x₂ - x₁)² + (y₂ - y₁)²)

The programmed version of this is: 

```py

   distance = round(
        100
        * math.sqrt(
            ((thumb_tip.x - pinky_tip.x) ** 2 + (thumb_tip.y - pinky_tip.y) ** 2)
        )
    )
    dist_val = distance 


```


## What to look at: 

Refer to the program code to see how everything works, its not too complicated and the code itself is quite understandable, refer to the hand landmarks to see where they are marked and positioned on the hands itself.

## Functions within the code: 

There are only two primary functions that are quite important: 

```py

drawFPS(); #draws the FPS to the frame of the input.

drawLineTP(); #draws the lines between the thumb and pinky all while calculating the distance between these two points.


#The rest of the code is quite simple, if video input is recived than it runs through everything and
#communicates with the Arduino. 


```
## A demo of the program: 

You can watch this video to see a working demo: 


https://github.com/user-attachments/assets/a2a45f53-4c09-42c0-b851-c849b2a36fd4



