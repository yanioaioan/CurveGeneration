import maya.cmds as cmds
import math

numberOfTotalWholeCurves=2
curveNumber=0
curveName='curve'

curveNumber+=1
length=1
angle=0.0


while angle<360.0:
    
    x=length*math.cos(angle*(math.pi/180.0))
    y=length*math.cos(angle*(math.pi/180.0))
    
    zIncrement=angle/200.0
    
    if not cmds.objExists(curveName + str(curveNumber)):
        mycurve=cmds.curve(p=[(x,y,0),(x,y,0),(x,y,0),(x,y,0)])