#import MirrorTools
#reload (MirrorTools)
#from MirrorTools import *
#MirrorTools.MirrorAll()

import maya.cmds as cmds
import maya.mel as mel
import maya
import sys

class option():
    keys = 0
    curve = 1
    def __init__(self, Type):
        self.value = Type
    def __str__(self):
        if self.value == option.keys:
            return 'keys'
        if self.value == option.curve:
            return 'curve'
    def __eq__(self,y):
       return self.value==y.value


def SelectControls():
    for item in cmds.ls(type='animLayer'):
        if (cmds.animLayer(item,q=True,selected=True)):
            mel.eval('string $layers[]={"'+item+'"};')
            mel.eval('layerEditorSelectObjectAnimLayer($layers);')

def SwapAnimation(a, b, optionType):
	null = cmds.spaceLocator(name="tempCopyNull")
	cmds.select(null,r=True)
	cmds.animLayer(addSelectedObjects=True)
	if cmds.selectKey( a ) > 0:
		SendAnimation( a, null[0], optionType) 
	if cmds.selectKey( b ) > 0:
		SendAnimation( b, a, optionType )
	if cmds.selectKey( null[0] ) > 0:
		SendAnimation( null[0], b, optionType)
	cmds.delete(null)

def SendAnimation(a,b, optionType):
	if cmds.selectKey( a ) > 0:
		if optionType==option.keys:
			cmds.cutKey( a , time=(cTime,cTime), option=option(optionType) )
		else:
			cmds.copyKey(a, option=option(optionType) );
		cmds.pasteKey( b )
  
def MirrorAnimation( item, optionType ):
	attr = ("translateY", "rotate", "rotateZ")    
	for a in attr:
		cmds.select(cl=True)
		key = cmds.selectKey( item, attribute=a)
		if (key > 0):
			if optionType==option.keys:
				cmds.selectKey( item, time=(cTime,cTime), attribute=a )
			else: #"curve"
				cmds.selectKey( item, attribute=a )
			cmds.scaleKey( valueScale = -1.0, valuePivot=0.0)
	cmds.select( item )

def PopulateLists():
    SelectControls()
    ctrls = cmds.ls(selection=True)
    tempLeft=[]
    tempRight=[]
    for c in ctrls:
        ctrlName = c.split(':') #ignore Namespace
        ctrlName = ctrlName[len(ctrlName)-1]
        if ( "l_" in ctrlName ):
            left.append(c)
        elif ( "r_" in ctrlName ):
            right.append(c)
        elif ( "c_" in ctrlName ):
            single.append(c)
    tempRight.sort()
    tempLeft.sort()
    if len(tempRight) != len(tempRight):
        for le in tempLeft:
            L_token = le.split('_')[-1]
            for ri in tempRight: 
                R_token = ri.split('_')[-1]
                if (R_token == L_token) and ( "l_" in le ) and ("r_" in ri):
                    if le not in left:
                        left.append(le)
                    if ri not in right:
                        right.append(ri)
        cmds.error("Sides are not symetrical")

def MirrorAll(optionType = option.keys):
    global cTime
    cTime = int(cmds.currentTime(query=True))
    global single
    single = []
    global right
    right = []
    global left
    left = []
    PopulateLists()
    for ind in range(0,len(left)):
        SwapAnimation(left[ind],right[ind], optionType)        
    for s in single:
        MirrorAnimation(s, optionType) 

