# README #

### What is this repository for? ###

This is a set of experiments I have done in preparation for my accessibility system based on these methods (found in https://bitbucket.org/adam-barnett/blink_accessibility_project ).  

Each folder is a specific area which I've explored and many of them have contributed directly to the accessibility project.  Specifically their purposes are:

## saving_eyes_to_file 
Since many of the other methods use template matching which need an image of the eyes to work, this is a couple of different approaches to capturing the eyes using a Haar cascade to find them, or capturing the entire image and requiring further editing (for when I'm wearing my glasses)

## moving_frames
In order to allow users to select an area on the screen with limited inputs I created moving frames.  These are lines which scan across the screen from top to bottom and left to right.  Where they cross indicates where the user wants to click

## blink_detection_with_histograms
These were initial experiments using a Haar cascade to detect the eyes and then looking for difference in the histograms of the region containing the eyes from frame to frame in order to detect blinks.  I compared the different methods of comparing histograms provided by Opencv (correlation, Chi-squared, intersection and Hellinger) to actual blinks (input manually at the time of recording) to check their effectiveness.  The results of this can be seen in the Libre office spreadsheet (blink_detection_histograms.ods ).  Ultimately the results were good, but overall unreliable due to the situations which are difficult for Haar cascades (half the face in shadow and half in light for instance).  

##  blink_detection_with_template_matching
Experiments in using template matching to look for blinks.  Initially I compared the different opencv methods (compared with blink_detection_comparisons.py, with the results in template_matching.ods), finding the coefficient normed to be the most effective.  This was then adapted into full detection in blink_detection_test.py which once found to be effective was further developed into a BlinkDetector class for use in my main project.
Note that differently to some other approaches I attempt to find the eyes first using haarcascades.  If successful then I perform template matching over that area (if unsuccessful then I search the entire image).  I found this speeds up the matching somewhat and also improves the accuracy (even allowing images taken in quite different lights to be used).  Additionally, I also attempt to match both the open eyes and shut eyes, then I compare the probabilities of each.  While slower, this gives makes the detection much more accurate.

## experiments_with_different_cascades
This is a place for me to dump new facial/eye/glasses detecting cascades and test them to see how effective they are in various lights.  

## rotational_invariance
A number of experiments with different methods for finding the face even when it is rotating over time

