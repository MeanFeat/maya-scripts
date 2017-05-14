from pymel.core import *
import random

class CurveOrganism():
	keyCurve = None
	cost = 0.0
	def __init__(self, keys):
		self.keyCurve = keys
		self.cost = 0.0
	def UpdateCost(self, Target):
		self.cost = 0.0
		for i in range(int(cmds.playbackOptions(query=True, min=True)), int(cmds.playbackOptions(query=True, max=True) + 1)):
			cost = cmds.keyframe( GetBredCurves(), attribute=self.keyCurve ,query=True,time=(i,i), eval=True )[0] - cmds.keyframe( Target, query=True, time=(i,i), eval=True )[0]
			self.cost += cost * cost
	

class population():
	def __init__(self, count, mutChance, mutAmount, champCount):
		self.maxCount = count
		self.mutationChance = mutChance
		self.mutAmount = mutAmount
		self.champCount = champCount
		self.organisms =[]		
		keyTimes = [0,15,30]
		keyValues = [0.0,13,0.0]
		for id in range(0,count):
			name = 'Bred_Gen' + str(5) + '_id' + str(id)
			cmds.addAttr(GetBredCurves(), attributeType="float", ln=name, keyable=True)
		for a in cmds.listAttr(GetBredCurves()):
			if a.__contains__('Bred'):
				for k in range(len(keyTimes)):
					mutation = -mutAmount + (random.random() * mutAmount * 2) if random.random() < self.mutationChance else 0.0
					cmds.setKeyframe(GetBredCurves(), attribute=a, time=keyTimes[k], value=keyValues[k] + mutation)
				self.organisms.append(CurveOrganism(a))
	def Sort(self):
		self.organisms = sorted(self.organisms, cmp=lambda x, y: cmp(x.cost, y.cost))
	def BreedChild(self, p1, p2 ):
		child = CurveOrganism(p1.keys, p1.tangentAngles, p1.tangentWeights)
		for k in range(len(p1.tangentAngles)):
			#child.keys[k] = p1.keys[k] if random.randint(0,1) else p2.keys[k]
			child.tangentAngles[k] = p1.tangentAngles[k] if random.randint(0,1) else p2.tangentAngles[k]
			child.tangentWeights[k] = p1.tangentWeights[k] if random.randint(0,1) else p2.tangentWeights[k]
			#if random.random() < self.mutationChance:
			#	child.keys[k] += -self.mutAmount + (random.random() * self.mutAmount * 2)				
			if random.random() < self.mutationChance:
				child.tangentAngles[k] += -self.mutAmount + (random.random() * self.mutAmount * 2)				
			if random.random() < self.mutationChance:
				child.tangentWeights[k] += -self.mutAmount + (random.random() * self.mutAmount * 2)
		return child
	def BreedNextGen(self):
	    champions = []
	    champ = CurveOrganism(self.organisms[0].keys, self.organisms[0].tangentAngles, self.organisms[0].tangentWeights)
	    for c in range(self.champCount):
	        champions.append(self.organisms[c])
	    self.organisms = []
	    self.organisms.append(champ)
	    for o in range(0,self.maxCount):
	        #p1 = champions[random.randint(0, self.champCount)]
	        #p2 = champions[random.randint(0, self.champCount)]
	        self.organisms.append(self.BreedChild(champ,champ))

def GetBredCurves():	
	for item in cmds.ls(type='animCurveUU'):
		if item == 'BredCurves':
			return item	
	return cmds.createNode( 'animCurveUU', name='BredCurves')

def NextGen():
	sortedCosts = []
	for o in pop.organisms:
		o.UpdateCost(origCurve)
	pop.Sort()
	pop.BreedNextGen()


origCurve = cmds.animCurveEditor('graphEditor1GraphEd', query=True, curvesShown=True)
pop = None
pop = population(30,0.5,0.5,1)


for o in pop.organisms:
    o.UpdateCost('pCube1_translateY')

pop.Sort()
    
for o in pop.organisms:
    print o.cost   