arucoV2.py is capable of running on a Jetson Nano if gstreamer is added as of 06/21/2024

numpySocket was used for sending data over the network because it was simple and allowed me to quickly demonstrate networking. The numpySocket files are currently working as of 06/27/2024

cameraRelativeToWoldTelative.py is some math for future referance. 

Ignore the following: dual_camera.py, simple_camera.cpp, simple_camera.py. These are a resource that I often use when using the IMX219 because I can not remember all of the settings. 

arucoV1.py does not work and arucoViaExtraLib.py works very well if the enviorment is configured properly, unfortunately the proccess of getting this library on the jetson nano is beyond the scope of this project and beyond my current abilitys. 
