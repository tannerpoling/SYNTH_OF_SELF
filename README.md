# SYNTH_OF_SELF is an interactive media project created by Tanner Poling  

The basic premise of this project is to represent the physical location and movement of people via sound,
exploring harmony through spatial arrangement.  

**HOW TO USE**  
Required packages: OpenCV 3.0+, audiolazy, numpy, matplotlib  
./synthofself.py runs the main program  
object recognition parameters can be modified within vidmodule.py  
synth volume can be modified within synthmodule.py  
min/max frequency, sampling rate, additional gain, min/max modulation can be changed in synthofself.py  

What's next:  
- using more sophisticated / robust object recognition and tracking  
- increasing flexibility, current implementation has 4 synths constantly running  
- want to be more efficient / less hacked together  
- add heatmap of detected objects
