#Author-FernandoFigueiredo
#Description-Creates lofting profiles for a double envoloping worm gear

import adsk.core, adsk.fusion, traceback
import math


def run(context):
    Pi = 3.141592654


    ####################################################
    ## Parameters (distances in cm angles in degrees)
    ####################################################
    pitch = 1.2         #Pitch (cm)
    starts = 1          #Number of starts
    whPteeth = 12       #Nuber of teeth on wheel
    pressAngle =  14.5  #Pressure Angle (deg) 14.5 or 20
    woRes = 36          #Worm Resolution
    
    
    
    redRatio = whPteeth /starts  #reduction ration

    pressAngleRads = pressAngle/180*Pi

    
    
    

    woResAng = 2*Pi/ (woRes)
    whResAng = woResAng / redRatio
    print('OutRotAng =', whResAng * woRes)
    print ('RedRatio:', redRatio)
    print ('woResAng:', woResAng)
    print ('whResAng:', whResAng)
    woLength = 5
    woDp = 1.5 # Worm Pitch Diameter
    toothHeight = 0.5
    woDo = woDp + toothHeight #Worm Out Diameter
    woDr = woDp - toothHeight #Worm Root Diameter
    woDm = 2.5 #Worm Max Diameter
    whDp = whPteeth * pitch / Pi 
    whAngPitch = 2 * Pi /(whPteeth)
    WhDo = woDp + whDp - woDr
    WhDi = woDp + whDp - woDo   
    cD = (whDp + woDp) /2
    
    print('WheelTeeth =' , whPteeth)
    print('WheelPitchDiameter =' , whDp)

    
    
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        #doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        
        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create a new sketch on the xy plane.
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane

        
        #circlePitch = circles.addByCenterRadius(adsk.core.Point3D.create(cD, 0, 0), whDp/2)

        #oCircle = circles.addByCenterRadius(adsk.core.Point3D.create(cD, 0, 0), WhDo/2)


        for i in range(0, woRes+1):
            sketch = sketches.add(xyPlane)
            #sketch = sketches[0]
    
    
    
            # Draw a rectangle by two points.
            lines = sketch.sketchCurves.sketchLines;  
            #wormCenterLine = lines.addByTwoPoints(adsk.core.Point3D.create(0, -woLength/2-20, 0), adsk.core.Point3D.create(0, woLength/2+20, 0))                  
    
            # Draw some circles.
            circles = sketch.sketchCurves.sketchCircles
            iCircle = circles.addByCenterRadius(adsk.core.Point3D.create(cD, 0, 0), WhDi/2)

            
            #oCircle = oCircle.trim (adsk.core.Point3D.create(cD+WhDo/2, 0, 0))        
            recLines = lines.addTwoPointRectangle(adsk.core.Point3D.create(0, -woLength/2, 0), adsk.core.Point3D.create(woDm/2, woLength/2, 0))
            geoms2 = adsk.core.ObjectCollection.create()
            geoms2.add(recLines[1])
            geoms2.add(iCircle)
            
            for j in range(0, int(whPteeth)): 
                toothProf1 = lines.addByTwoPoints(adsk.core.Point3D.create(woDo/2*1.2, -pitch/4-(woDo-woDp)*math.tan(pressAngleRads)/2*1.2 , 0), adsk.core.Point3D.create(woDr/2, -pitch/4+(woDp-woDr)/2*math.tan(pressAngleRads), 0))                          
                toothProf2 = lines.addByTwoPoints(adsk.core.Point3D.create(woDo/2*1.2, +pitch/4+(woDo-woDp)*math.tan(pressAngleRads)/2*1.2 , 0), adsk.core.Point3D.create(woDr/2, +pitch/4-(woDp-woDr)/2*math.tan(pressAngleRads), 0))                  
                toothProf3 = lines.addByTwoPoints(toothProf1.endSketchPoint, toothProf2.endSketchPoint)                  


                geoms1 = adsk.core.ObjectCollection.create()
                geoms1.add(toothProf1)
                geoms1.add(toothProf2)
                geoms1.add(toothProf3)
                rotationAxis1 = adsk.core.Vector3D.create(0, 0, 1)
                rotationCenter1 = adsk.core.Point3D.create(cD, 0, 0)        
                rotationMatrix1 = adsk.core.Matrix3D.create()
                rotationMatrix1.setToRotation(whResAng *i + whAngPitch *j, rotationAxis1, rotationCenter1)
                sketch.move(geoms1, rotationMatrix1)            
                geoms2.add(toothProf1)
                geoms2.add(toothProf2)   
   

            

            
            ##geoms.add(oCircle)
            

            
            #print(i)
            

            
            
       
                

    
            rotationAxis2 = adsk.core.Vector3D.create(0, 1, 0)
            rotationCenter2 = adsk.core.Point3D.create(0, 0, 0)
            rotationMatrix2 = adsk.core.Matrix3D.create()
            rotationMatrix2.setToRotation(woResAng * i, rotationAxis2, rotationCenter2)
            
            sketch.move(geoms2, rotationMatrix2)
            #sketch.move(toothProf2, rotationMatrix2)   
            #sketch.move(iCircle, rotationMatrix2)
            #sketch.move(recLines, rotationMatrix2)          

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))