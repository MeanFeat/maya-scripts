#import MirrorTools
#reload (MirrorTools)
#from MirrorTools import *
#MirrorTools.MirrorAll()

import maya.cmds as cmds
import maya.mel as mel
import maya
import sys
import maya.api.OpenMaya as om
import LayerTools as layerTools
import collections

BasisTuple = collections.namedtuple('object', ['up','forward','right'])

class axis():
	X = 0
	Y = 1
	Z = 2
	def __init__(self, Type):
		self.value = Type
	def __str__(self):
		if self.value == axis.X:
			return 'X'
		if self.value == axis.Y:
			return 'Y'
		if self.value == axis.Z:
			return 'Z'
	def __eq__(self,y):
	   return self.value==y.value

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
	cmds.animLayer(layerTools.GetSelectedLayers()[0], edit=True, addSelectedObjects=True)
	if cmds.selectKey( a ) > 0:		
		print "A has animation"
		SendAnimation( a, null, optionType)
	if cmds.selectKey( b ) > 0:
		print "B has animation"
		SendAnimation( b, a, optionType )
	if cmds.selectKey( null) > 0:
		print "Null has animation"
		SendAnimation( null, b, optionType)
	cmds.delete(null)

def SendAnimation(a,b, optionType):
	if cmds.selectKey( a ) > 0:
		if optionType==option.keys:
			cmds.cutKey( a , time=(cTime,cTime), option=option(optionType) )
		else:
			cmds.copyKey(a, option=option(optionType) );
		cmds.pasteKey( b )
 
def GetMirroredScaleMatrix():
	return

def MirrorAnimation( item, optionType ):
	attr = ("translateX","translateY","translateZ", "rotateX", "rotateY", "rotateZ")   
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
			tempLeft.append(c)
		elif ( "r_" in ctrlName ):
			tempRight.append(c)
		elif ( "c_" in ctrlName ):
			single.append(c)
	tempRight.sort()
	tempLeft.sort()
	if len(tempLeft) != len(tempRight):
		for le in tempLeft:
			L_token = le.split('_')[-1]
			for ri in tempRight: 
				R_token = ri.split('_')[-1]
				if (R_token == L_token) and ( "l_" in le ) and ("r_" in ri):
					if le not in left:
						left.append(le)
					if ri not in right:
						right.append(ri)

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

def CreateNullOnObject(item, suffix):
	tempNull = cmds.group( empty=True, name = item + suffix )
	tempPC = cmds.parentConstraint( item, tempNull, mo=False)
	cmds.delete(tempPC)
	cmds.makeIdentity(tempNull,apply=True, t=1, r=1, s=1)
	return tempNull

def BuildDirVector(item, transAxis):
	center = cmds.xform(sel[0], query=True, translation=True, worldSpace=True)
	null = CreateNullOnObject(item, '_tempNull_' + transAxis.__str__())
	cmds.move( 1,null,localSpace=True, x=(transAxis == axis(axis.X)), y=(transAxis == axis(axis.Y)), z=(transAxis == axis(axis.Z)))
	end = cmds.xform(null, query=True, translation=True, worldSpace=True)
	cmds.delete(null)
	direction = om.MVector(end[0] - center[0], end[1] - center[1], end[2] - center[2])
	direction.normalize()
	return direction

def BuildBasis(item):
	axes = []
	axes.append(BuildDirVector(item, axis(axis.X)))
	axes.append(BuildDirVector(item, axis(axis.Y)))
	axes.append(BuildDirVector(item, axis(axis.Z)))
	for a in axes:
		print a.__str__()
	#return BasisTuple( item, axes)

cmds.select('Rig:l_legCtrl')
sel = cmds.ls(selection=True)
tempBasis = BuildBasis(sel[0])
