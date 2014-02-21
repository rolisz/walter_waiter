walter_waiter
=============

This is the actual repo for Walter. Here we will have the code that is running. Also here we will post the issues and bugs. The code uses Python 2.7 and OpenCV 3

States
- loadGlasses
    - detect and go after glass
    - position arm
    - grab and put on tray (also reset arm position)
        - run thread for each glass (per color), compare distances and choose closest one
    - if tray is not full loaded => loadGlasses
        - else => offerGlasses
- offerGlasses
    - detect people (spin until face detection)
    - follow face
        - face out => offerGlasses
    - face exit up => waitForGlassPickup
- waitForGlassPickup
    - wait:
        - register for no_cups_on_tray
        - when happens, unregister no_cups_on_tray and face det
            - go to table (???)
            - register cup det