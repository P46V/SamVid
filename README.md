#     SamVid
Implementing [OpenSfM](https://github.com/mapillary/OpenSfM/tree/master/opensfm) and patch trackers in OpenCV to track objects in a video and then make 3D images of them. The implementation of this has been done in two steps:
* Tracking multiple Patches using patch trackers in OpenCV
* Converting the Patches to 3D Image Reconstructions using OpenSfM
For this project,We have implemented the code on [this video](https://youtu.be/MZFL6t0vX8o)
##  Pre-Requisites:
* [opencv-contrib-python](https://github.com/mapillary/OpenSfM/tree/master/opensfm)
* Python with OpenCV library installed.
## Tracking Patches
For tracking any of the patch trackers available in OpenCV can be used. We have prefered to use KCF but that is upto the choice of the user.The tracknpatch contains the code for 3 different methods implemented for tracking objects:

* **Single Track**: This is implemented on the afformentioned video where the motion of the car is tracked and the subsequent patches are stored in a folder named patches.To run the file make sure to change the location of the video_path and path_to_save according to where it is stored in your laptop.


* **Multitrack** : In this various objects can be selected in the frame manually by making the track boxes around them in the initial frame and then the patches of each object are stored in a hence created multipt folder in an integer named folder.To run again we have to make sure to change the location of the video_path and path_tosave accordingly


* **FlexiMultiTracker** : In this unlike the previous methods, the objects can be selected at any point in the video. Upon running the file,the video would start playing and to pause on any frame simply type the letter 's' and select the track box of the object of interest and press space to continue the video.The patches would be saved in multipt folder and make similar location changes

## 3D Image Reconstruction
After obtaining the necessary patches using OpenCV from the video our next aim was to make 3D reconstructions of the selected objects for this we utilized OpenSfM link of which we have provided above.
## Next Target
We will now try to extract mesh from the 3D objects and later on animate the Meshes.



