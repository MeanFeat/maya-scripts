import maya.cmds as cmds

def PinTranslate( sel ):
    for s in sel:
        pinName = s+"_TranslatePin"
        if cmds.ls( pinName):
            cmds.delete(pinName)
        else:        
            tempNull = cmds.spaceLocator( name=pinName)
            tempPC = cmds.pointConstraint( s, tempNull, mo=False)
            cmds.delete(tempPC)
            tempPC = cmds.pointConstraint( tempNull, s, mo=True)
            cmds.select(sel)

def PinRotate( sel ):
    for s in sel:
        pinName = s+"_RotatePin"
        if cmds.ls( pinName):
            cmds.delete(pinName)
        else:        
            tempNull = cmds.spaceLocator( name=pinName)
            tempPC = cmds.parentConstraint( s, tempNull, mo=False)
            cmds.delete(tempPC)
            tempPC = cmds.orientConstraint( tempNull, s, mo=True)
            cmds.select(sel)