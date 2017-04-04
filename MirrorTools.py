import maya.cmds as cmds
import maya.mel as mel
import maya
import sys
import maya.api.OpenMaya as om
import LayerTools as layerTools
import LayerUpdater as layerUpdater
import Snippets as snip

class basis():
	item = None
	X = om.MVector()
	Y = om.MVector()
	Z = om.MVector()
	def __init__(self, i, x, y, z):
		self.item = i
		self.X = x
		self.Y = y
		self.Z = z

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

def GetWorldRight():
	return om.MVector(1,0,0)

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
		SendAnimation( a, null, optionType)
	if cmds.selectKey( b ) > 0:
		SendAnimation( b, a, optionType )
	if cmds.selectKey( null) > 0:
		SendAnimation( null, b, optionType)
	cmds.delete(null)

def SendAnimation(a,b, optionType):
	if cmds.selectKey( a ) > 0:
		if optionType==option(option.keys):
			cmds.cutKey( a, time=(cTime,cTime), option=optionType.__str__() )
		else:
			cmds.copyKey( a, option=optionType.__str__())
		cmds.pasteKey( b, option = 'replaceCompletely')

def GetDotProducts(basis):
	prods = []
	prods.append(basis.X * GetWorldRight())
	prods.append(basis.Y * GetWorldRight())
	prods.append(basis.Z * GetWorldRight())
	return prods

def GetMirroredScaleMatrix(item):
	scaleMatrix = [1,1,1,1,1,1]
	SelectControls()
	layerUpdater.UpdateAnimLayer( GetZeroLayer() )
	itemBasis = BuildBasis(item)
	layerUpdater.UpdateSelectedAnimLayer()
	dotProds = GetDotProducts(itemBasis)
	highest = 0
	rightAxis = 0
	for idx in range(0,3):
		if abs(dotProds[idx]) > highest:
			highest = abs(dotProds[idx])
			rightAxis = idx
	scaleMatrix[rightAxis] *= -1
	for rotIdx in range(3,6):
		if rotIdx -3 != rightAxis:
			scaleMatrix[rotIdx] *= -1
	return scaleMatrix

def GetZeroLayer():	
	zeroLayer = None
	for item in cmds.ls(type='animLayer'):
		if item == 'Mirror_ZeroLayer':
			zeroLayer = item
	if zeroLayer == None:
		zeroLayer = mel.eval('animLayer -copyNoAnimation ' + layerTools.GetSelectedLayers()[0] + ' Mirror_ZeroLayer;')
		layerUpdater.UpdateAnimLayer(zeroLayer)
		mel.eval('string $layers[]={"Mirror_ZeroLayer"}; layerEditorSelectObjectAnimLayer($layers);')
		for o in cmds.ls(selection=True):
			for a in cmds.listAttr( o, keyable=True, unlocked=True ):
				tempKey = cmds.setKeyframe(o+"."+a, time= 0, value=0)
	return zeroLayer

def MirrorAnimation( item, optionType, scaleMatrix):
	attr = ["translateX","translateY","translateZ","rotateX","rotateY","rotateZ"]
	for idx, a in enumerate( attr ):
		if cmds.getAttr(item +'.'+ a, lock=True) == False:
			cmds.select(cl=True)
			key = cmds.selectKey( item, attribute=a)
			if (key > 0):
				if optionType==option(option.keys):
					cmds.selectKey( item, time=(cTime,cTime), attribute=a )
				else: #"curve"
					cmds.selectKey( item, attribute=a )
				cmds.scaleKey( valueScale = scaleMatrix[idx], valuePivot=0.0)
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


def MirrorAll(optionType = option(option.curve)):
	global cTime
	cTime = int(cmds.currentTime(query=True))
	global single
	single = []
	global right
	right = []
	global left
	left = []
	PopulateLists()
	gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar;')
	cmds.progressBar( gMainProgressBar,
				edit=True,
				beginProgress=True,
				isInterruptable=True,
				status='Mirroring Controls ...',
				maxValue=len(single) + len(left) + len(right) )
	for s in single:
		MirrorAnimation(s, optionType, GetMirroredScaleMatrix(s)) 
		cmds.progressBar(gMainProgressBar, edit=True, step=1)
	for ind in range(0,len(left)):
		SwapAnimation(left[ind],right[ind], optionType)
		MirrorAnimation(left[ind], optionType, GetMirroredScaleMatrix(left[ind])) 
		MirrorAnimation(right[ind], optionType, GetMirroredScaleMatrix(right[ind])) 
		cmds.progressBar(gMainProgressBar, edit=True, step=2)
	cmds.delete(GetZeroLayer())
	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)


def BuildDirVector(item, transAxis):
	center = cmds.xform(item, query=True, pivots=True, worldSpace=True)
	null = snip.CreateNullOnObject(item, '_tempNull_' + transAxis.__str__())
	cmds.move( 1,null,objectSpace=True, x=(transAxis == axis(axis.X)), y=(transAxis == axis(axis.Y)), z=(transAxis == axis(axis.Z)))
	end = cmds.xform(null, query=True, pivots=True, worldSpace=True)
	cmds.delete(null)
	direction = om.MVector(end[0] - center[0], end[1] - center[1], end[2] - center[2])
	direction.normalize()
	return direction

def BuildBasis(item):
	return basis(item, BuildDirVector(item, axis(axis.X)), BuildDirVector(item, axis(axis.Y)), BuildDirVector(item, axis(axis.Z)))
