# *SYNTH_OF_SELF*

An interactive media project investigating the influence of sound and visuals upon the ways we navigate and relate to space.
What this software does is map participants' poisiton in a room to the pitch and modulation of synthesizers, which then drive visuals generated using TouchDesigner.   


This was inspired by curiosities into how audio might impact the way people interact with their surroundings and fellow participants; do we tend towards harmony? How might this effect vary with volume, or permanent objects establishing a "base tone"?  
Do people have a tendency to form chords in their arrangement? At what point is this influence considered conscious / unconscious?

Features that are currently working:  
- OpenCV code to detect objects in the current webcam frame  
- Python code to translate the positons of these objects into synthesizer tones in real time  
- TCP / IP scripts to transmit position data to another computer  
- A TouchDesigner project that can recieve this data, and update a table which is used to control visual parameters in real time  

Features needing work:  
- Optimizing the Python synthesizers  
- Making more interesting / intuitive visuals in TouchDesigner  
- Detecting chords from current audio output  
- Convincing someone to let me put this in an exhibit space   

There is another branch of this project named 444, dedicated to more critical exploration of computer vision via experimental art; feel free to give it a look!

