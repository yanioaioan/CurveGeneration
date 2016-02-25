import maya.cmds as cmds
import math

cmds.file( f=True, new=True )
# clear up the scene
cmds.select(all=True)
cmds.delete()

numberOfTotalWholeCurves=1
curveNumber=1
curveName='pPlane1'#curve1
numberOfWholeCircleRotations=1

lengthCircleRadius=5
angle=0.0
springCoefficient=400.0
angleIncrementCircleSegments=20

mycurve=''
#for i in range(numberOfTotalWholeCurves):
#    curveNumber+=1
#    angle=0.0

planeList=[]

while angle<numberOfWholeCircleRotations*360.0:
    
    x=length*math.cos(angle*(math.pi/180.0))
    y=length*math.sin(angle*(math.pi/180.0))
    
    springzIncrement=(angle/springCoefficient)
    
    ''' + str(curveNumber)'''
    if not cmds.objExists(curveName ):
        #mycurve=cmds.curve(p=[(x,y,springzIncrement),(x,y,springzIncrement),(x,y,springzIncrement),(x,y,springzIncrement)])
        
        mycurve=cmds.polyPlane(sx=1,sy=1)
        cmds.move(x,y,0)
        cmds.rotate(0,0,90)
        planeList.append(mycurve[0])
        
        cmds.select(all=True)
        cmds.delete(ch=True)
    else:
        #cmds.curve(mycurve, append=True, p=[(x,y,springzIncrement)])
        
        mycurve=cmds.polyPlane(sx=1,sy=1)
        cmds.move(x,y,0)
        cmds.rotate(0,0,90+angle)
        planeList.append(mycurve[0])
        
        cmds.select(all=True)
        cmds.delete(ch=True)
        
    angle+=angleIncrementCircleSegments
    
    #cmds.refresh()




for i in planeList:
    #facenormals=cmds.polyInfo( fn=True )
    facepositionWS=cmds.xform(i+".f[:]", query=True, translation=True, worldSpace=True)
    print facepositionWS
    
    '''get normals of each face'''
    #Cannot use the following command since it will return the initial plane creation normal, not the one after we performed the 'cmds.rotate' command
    #facenormals=cmds.polyInfo( fn=True )
        
    #so..we can actually calculate each plane's normal from cross(vertex2-vertex1, vertex3-vertex1), since they all line on the same plane
    v1=cmds.xform(i+".vtx[0]", query=True, translation=True, worldSpace=True)
    v2=cmds.xform(i+".vtx[1]", query=True, translation=True, worldSpace=True)
    v3=cmds.xform(i+".vtx[2]", query=True, translation=True, worldSpace=True)
    
    #v2-v1
    sideVector1=[ v2[0]-v1[0], v2[1]-v1[1], v2[2]-v1[2] ]
    #v3-v1
    sideVector2=[ v3[0]-v1[0], v3[1]-v1[1], v3[2]-v1[2] ]
    
    #Now we can feed them to the cross product function
    planeNormal=cross(sideVector1,sideVector2)
    
    #find center of face (average the face's vertex posiitons)
    sumX=0
    sumY=0
    sumZ=0
    
    #4 vertices (12_all_coordinates / 3_coordinates_each vertex in 3d)
    faceVertices=len(facepositionWS)/3
    vertexElements=3
    #print "faceVertices=%d"%(faceVertices)
    for v in range(0,len(facepositionWS),vertexElements):
        sumX=sumX + facepositionWS[v]
        sumY=sumY + facepositionWS[v+1]
        sumZ=sumZ + facepositionWS[v+2]
        
    #average position of vertices of each faces    
    faceCenter = [sumX/faceVertices, sumY/faceVertices, sumZ/faceVertices]
        
    #place cone
    c=cmds.polyLine( n='myCone', sx=5, sy=5, sz=5)
    cmds.move( faceCenter[0], faceCenter[1], faceCenter[2], c, absolute=True )
    cmds.scale(0.3,0.3,0.3, c, absolute=True)
    
    #split polyinfo unicode , to get normals of each face
    #fnormal= []
    #label, vertex, x, y, z = facenormals[i].split()    
    #fnormal.append(float(x))
    #fnormal.append(float(y))
    #fnormal.append(float(z))
    fnormal=planeNormal
    
    fnormalNormalized=[]
    #normalize vector from point on sphee to origin of sphere
    
    mag=math.sqrt( fnormal[0]*fnormal[0] + fnormal[1]*fnormal[1] + fnormal[2]*fnormal[2] )
    if mag==0:
        mag=1

    #calculate axis-angle 
    upVec=[0,1,0]    
    axis=cross(upVec, fnormal)
            
    axisNormalized=[]
    mag=math.sqrt( axis[0]*axis[0] + axis[1]*axis[1] + axis[2]*axis[2] )
    if mag==0:
        mag=1
        
    axisNormalized.append(axis[0]/mag)
    axisNormalized.append(axis[1]/mag)
    axisNormalized.append(axis[2]/mag)
    
    #print "dot(upVec,fnormalNormalized)=%f"%(dot(upVec,fnormal))
    #normalize if fnormal is not normalized
    
    if (fnormal[0]>1 or fnormal[0]<-1) or (fnormal[1]>1 or fnormal[1]<-1) or ((fnormal[2]>1 or fnormal[2]<-1)):
        mag=math.sqrt( fnormal[0]*fnormal[0] + fnormal[1]*fnormal[1] + fnormal[2]*fnormal[2] )
        fnormalNormalized.append(fnormal[0]/mag)
        fnormalNormalized.append(fnormal[1]/mag)
        fnormalNormalized.append(fnormal[2]/mag)
        fnormal=fnormalNormalized
           
    
    angle=math.acos( dot(upVec,fnormal) )
        
    bank,heading,attitude = toEuler(axisNormalized[0],axisNormalized[1],axisNormalized[2],angle)
        
    heading*=(180/math.pi)
    attitude*=(180/math.pi)
    bank*=(180/math.pi)
    
    '''
    if fnormal[1]<0 and fnormal[2]<0 and fnormal[0]>0:
        heading=heading+90
        attitude=-attitude    
    if fnormal[1]<0 and fnormal[2]<0 and fnormal[0]<0:
        heading=-heading+90
        attitude=-attitude
    elif fnormal[1]<0:
        attitude=-attitude
    ''' 
    
    
    '''
    mag=math.sqrt( axis[0]*axis[0] + axis[1]*axis[1] + axis[2]*axis[2] )
    if fnormal==[0,-0.5,0]:
        attitude=attitude+180
        print 1
        
    '''
    
    #print "heading=%f"%(heading)
    #print "attitude=%f"%(attitude)
    #print "bank=%f"%(bank)
    r = math.sqrt(fnormal[0]*fnormal[0] + fnormal[1]*fnormal[1] + fnormal[2]*fnormal[2])
    fi = (math.acos(fnormal[1])/r) * (180.0/math.pi)
    theta = math.atan2(fnormal[0],fnormal[2]) * (180.0/math.pi)  
       
     
    #cmds.rotate( bank, heading, attitude,  absolute=True, r=True )
    cmds.rotate(fi, theta, 0)
    
    cmds.delete(i,ch=True)

