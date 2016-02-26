import maya.cmds as cmds
import math
import random as rnd

cmds.file( f=True, new=True )
# clear up the scene
cmds.select(all=True)
cmds.delete()
# Create a set of simple objects for the motion path animation

# create a path, e,g, a curve
path = cmds.curve(d=3,p=[(-10, 0, 0),(-6, 0, 10),(-3, 0, -10),(10, 0, 0)],k=[0, 0, 0, 1, 1, 1])

# create an object, e.g. a sphere
leader = cmds.sphere()
cmds.group( leader[0], n='group1' )

for i in range(2,10):
    follower=cmds.instance(leader[0],smartTransform=True)
    x=rnd.randint(1,3)
    y=rnd.randint(1,3)
    z=rnd.randint(1,3)
    cmds.select(cl=True)
    cmds.select(follower[0])
    print follower[0]
    cmds.move(x,y,z)
    cmds.scale( 0.1, 0.1, 0.1 )

cmds.pathAnimation( 'group1', stu=0, etu=30, follow=True, c=path )
    

# 1. To animate the sphere along the curve, with one keyframe at
# the current time:

#cmds.pathAnimation( object[0], c=path )


# 2. To animate the sphere along the curve, from time 0 to time 30:

#cmds.pathAnimation( object[0], stu=0, etu=30, c=path )

# 3. To align the sphere to its path:

#cmds.pathAnimation( object[0], stu=0, etu=30, follow=True, c=path )


'''
# or:

cmds.select( object[0], path )
cmds.pathAnimation()

# 2. To animate the sphere along the curve, from time 0 to time 30:

cmds.pathAnimation( object[0], stu=0, etu=30, c=path )

# 3. To align the sphere to its path:

cmds.pathAnimation( object[0], stu=0, etu=30, follow=True, c=path )

# 4. To align the Z axis of sphere to the tangent of the curve, and
# to align the Y axis of the sphere to the up direction of the
# motion curve:

cmds.pathAnimation( object[0], stu=0, etu=30, fa='z', ua='y', c=path )

# 5. To align the Z axis of sphere to the tangent of the motion curve,
# to align the Y axis of sphere to the up direction of the motion
# curve, and to bank with the curvature of the motion curve:

cmds.pathAnimation( object[0], stu=0, etu=30, fa='z', ua='y', bank=True, c=path )

# 6. To change the setting on the bankScale for the motionPath1
# to negative 2.5 (i.e. bank out and multiply the computed
# bank value by 2.5):

cmds.pathAnimation( 'motionPath1', edit=True, bankScale=-2.5 )

# Notes:
# If the computed bank angles are not large enough, the user can
# specify the bankScale to amplify them. The default value is 1.

# Positive bankScale produces inward bank angle,
# negative bankScale produces outward bank angle.

# The user can also change the maximum bank angle through
# the bankThreshold option. Default value is 90 degrees.
'''
  