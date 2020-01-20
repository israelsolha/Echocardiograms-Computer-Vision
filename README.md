# Echocardiograms-Computer-Vision
Using Computer Vision to select and compute the greatest area of a Mitral Grid from an Echocardiogram video

This project is part of my Master's Research at the Federal University of Paraiba. The process of determining the area of a fully expanded Mitral Grid is almost always done manually by a professional physician and can takes several minutes to be computed. This program takes a video of an Echocardiogram, separates it into frames, detects the area of the mitral grid, detect the frame with the highest area and computes it. Finally, a new video with the borders detected by the program is created, and a report is presented to the user. Note that the starting path must be changed to match whatever the user's path for the original video and destination will be. 

Below is an example of the GUI interface, where the user is prompted for a video file, and a destination folder. The results are the maximum area in mm2, the frame with the biggest area, and the timestamp of that frame, along with the frame with the highlighted detected border.

<p align="center">
  <img src="https://i.imgur.com/4RZXkTy.png">
</p>
