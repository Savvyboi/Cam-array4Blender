A quick little Blender addon for creating an array of cameras on the faces of an object. Might work, or not :)

Steps
1. Install the cam-ar.py file by going Edit > Preferences > Add-ons menu > Install from Disk (little arrow on the upper right corner).
2. You can access the panel in the View3D > Sidebar > Camera Array Generator menu
3. Delete all other cameras in the scene (or it wont work)
4. Change the focal length > Select the object use wish to use as an array and hit Generate!
5. Go into wireframe mode to see your cameras

Beware:
1. If you end up scaling/rotating the object before generating the array, make sure to also apply the changes in Object > Apply > All transforms
2. Max amount of cameras is 999
3. The cameras will always face towards the origin of the object
4. Rendering a lot of cameras will take a while, and the Render Viewport might seem frozen 
