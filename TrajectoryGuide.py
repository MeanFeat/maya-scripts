import maya.cmds as cmds
import maya as maya

#Button/Hotkey code
#import TrajectoryGuide 
#reload(TrajectoryGuide)
#from TrajectoryGuide import * 

def SetToMotionTrail():
    print "Switching to : MotionTrail"
    origSelection = cmds.ls(selection=True)
    cmds.setAttr( "TrajectoryGuideShape.ghosting", 0)
    cmds.select( tGuide )
    cmds.CreateMotionTrail()
    cmds.setAttr( "motionTrail1Handle.trailDrawMode", 1)
    cmds.select(origSelection)
    
def SetToGhosting():
    print "Switching to : Ghosting"
    origSelection = cmds.ls(selection=True)
    framesVal = cmds.intSliderGrp('framesSlider', q=True, v=True)
    cmds.select( tGuide )
    cmds.setAttr( "TrajectoryGuideShape.ghosting", 0)
    maya.mel.eval('doGhost "3" { "1", "0", "2", %s, %s, "1", " 3 1 10 20", "1", "120", "0", "1", "1", "0", "0"};' %(framesVal,framesVal))
    cmds.select(origSelection)
    trails = cmds.ls( "motionTrail*")
    cmds.delete(trails)
    

def UpdateVal():
    cmds.setAttr( pc[0] +".target[0].targetOffsetTranslateX", cmds.floatSliderGrp('XoffsetSlider', q=True, v=True) * unitAdjust)
    cmds.setAttr( pc[0] +".target[0].targetOffsetTranslateY", cmds.floatSliderGrp('YoffsetSlider', q=True, v=True) * unitAdjust)
    cmds.setAttr( pc[0] +".target[0].targetOffsetTranslateZ", cmds.floatSliderGrp('ZoffsetSlider', q=True, v=True) * unitAdjust)
    cmds.parentConstraint( pc, edit=True, mo=True)
    UpdateFrames()
  
def UpdateSize():
    sizeVal = cmds.floatSliderGrp('sizeSlider', q=True, v=True)
    sizeAttr = tGuide[0] + ".scaleX"
    cmds.setAttr( sizeAttr, sizeVal* unitAdjust)
    sizeAttr = tGuide[0] + ".scaleY"
    cmds.setAttr( sizeAttr, sizeVal* unitAdjust)
    sizeAttr = tGuide[0] + ".scaleZ"
    cmds.setAttr( sizeAttr, sizeVal* unitAdjust)

def UpdateFrames():    
    if cmds.getAttr( "TrajectoryGuideShape.ghosting") == 1:
        origSelection = cmds.ls(selection=True)
        framesVal = cmds.intSliderGrp('framesSlider', q=True, v=True)
        cmds.select( tGuide )
        cmds.setAttr( "TrajectoryGuideShape.ghosting", 0)
        maya.mel.eval('doGhost "3" { "1", "0", "2", %s, %s, "1", " 3 1 10 20", "1", "120", "0", "1", "1", "0", "0"};' %(framesVal,framesVal))
        cmds.select(origSelection)
  
def getCurrentCamera():
    pan = cmds.getPanel(wf=True)
    cam = cmds.modelPanel(pan, q=True, camera=True)
    return cam

def DeleteGuides():
    guides = cmds.ls( "TrajectoryGuide*" )
    cmds.delete(guides)
       
def GetUnitAdjust(x):
    return {
            'm' : 1,
            'cm' : 100,
            'mm' : 1000
    }.get(x, 1)

def UpdateConstraintOffset():
    pc = cmds.parentConstraint( owner, tGuide, edit=True, mo=True)
    
def TGMenu():
    global tGuide
    global tGuideGrp    
    global owner
    global pc
    global menuWin
    global motionTrail
    global unitAdjust
    unitAdjust = GetUnitAdjust(cmds.currentUnit(query=True, linear=True))
    selection = cmds.ls( selection=True)
    if len(selection) == 0:
        DeleteGuides()
        cmds.deleteUI( menuWin, window=True)
    else:
        owner = selection[0]
        tGuide = cmds.spaceLocator(n="TrajectoryGuide")
        cmds.setKeyframe(tGuide, v=1, at="v")
        tGuideGrp = cmds.group( n="TrajectoryGuideGroup")
        pc = cmds.parentConstraint( owner, tGuide )
        cmds.parent( tGuide, owner)
        menuWin = cmds.window( title="Trajectory Guide", iconName='TrajectoryGuide', resizeToFitChildren=True, te=100,le=1200)
        cmds.columnLayout( adjustableColumn=True )
        attr = pc[0] + ".target[0].targetOffsetTranslateX"
        cmds.separator(bgc=(0.75, 0, 0))
        cmds.floatSliderGrp( 'XoffsetSlider', field = True, width=300, min=-100, max=100,value=0, changeCommand=('UpdateVal()'), dragCommand=('UpdateVal()'))
        cmds.separator(bgc=(0, 0.75, 0))
        cmds.floatSliderGrp( 'YoffsetSlider', field = True, width=300, min=-100, max=100,value=0,changeCommand=('UpdateVal()'), dragCommand=('UpdateVal()'))
        cmds.separator(bgc=(0, 0, 0.75))
        cmds.floatSliderGrp( 'ZoffsetSlider', field = True, width=300, min=-100, max=100,value=0,changeCommand=('UpdateVal()'), dragCommand=('UpdateVal()'))
        cmds.radioButtonGrp( numberOfRadioButtons=2, label='Type:', cal=(1,"left"), cw3=(25,75,25), labelArray2=['MotionTrail', 'Ghosting'], sl=1,on1=('SetToMotionTrail()'),on2=('SetToGhosting()'))
        SetToMotionTrail()
        cmds.intSliderGrp( 'framesSlider', label='Frames:', width=200, min=1, max=35,value=5, dragCommand=('UpdateFrames()'))
        cmds.floatSliderGrp( 'sizeSlider', label='Size:',field = True, width=200, min=0.15, max=5,value=1, dragCommand=('UpdateSize()'))
        cmds.button(label='UpdateConstraintOffset', command=('UpdateConstraintOffset()'))
        cmds.setParent( '..' )
        cmds.showWindow( menuWin )
        cmds.select(owner)
        UpdateSize()
       






