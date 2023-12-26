# Object Confidence level (1-99)
float32 confidence 

# object centroid position
float32[3] position

# Label of the Object
string label 

# 2d bounding box projected from Camera
# The bounding box is an array with four 
#values that haves the coordinates of the 
# position of the box corners in the following way
#
#
#[0]---------[1]
#|             |
#|             |
#|             |
#[2]---------[3]
float32[4] bounding_box_2d