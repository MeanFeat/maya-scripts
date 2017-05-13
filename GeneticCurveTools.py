from pymel.core import *
import random

class CurveOrganism():
	cost = 0.0
	def __init__(self, keys, tA, tW):
		self.keys = keys
		self.tangentAngles = tA
		self.tangentWeights = tW
	def SetCurve(self, bredCurve):
		keyIndexs = cmds.keyframe(bredCurve, query=True)
		for k in range(0,len(keyIndexs)):
			#cmds.keyframe(bredCurve,time=(keyIndexs[k],keyIndexs[k]), absolute=True, valueChange=self.keys[k])
			cmds.keyTangent(bredCurve, time=(keyIndexs[k],keyIndexs[k]),  absolute=True, outAngle=self.tangentAngles[k], outWeight=self.tangentWeights[k])
	def UpdateCost(self, bredCurve, Target):
		totalErr = 0.0
		self.cost = 0.0
		self.SetCurve(bredCurve)
		for i in range(int(cmds.playbackOptions(query=True, min=True)), int(cmds.playbackOptions(query=True, max=True))):
			cost = cmds.keyframe( bredCurve,query=True,time=(i,i), eval=True )[0] - Target[i][0]
			totalErr += cost * cost
		self.cost = totalErr
	

class population():
	organisms = []
	def __init__(self, count, mutChance, mutAmount, champCount):
		organisms = []
		self.maxCount = count
		self.mutationChance = mutChance
		self.mutAmount = mutAmount
		self.champCount = champCount
		for i in range(count):
			newOrg = CurveOrganism([0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0],[3.0,3.0,3.0,3.0,3.0])
			for k in range(len(newOrg.tangentAngles)):
				newOrg.tangentAngles[k] += -mutAmount + (random.random() * mutAmount * 2)
				newOrg.tangentWeights[k] += -mutAmount + (random.random() * mutAmount * 2)
			self.organisms.append(newOrg)
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
	def SortLowestCost(self):
		done = False
		sortedOrgs = []
		orgs = self.organisms
		bestOrg = orgs[0]
		while(not done):
			lowest = 1.7976931348623157e+308
			for o in orgs:
				if o.cost < lowest:
					lowest = o.cost
					bestOrg = o
			sortedOrgs.append(bestOrg)
			orgs.remove(bestOrg)
			done = True if len(orgs) == 0 else False
		self.organisms = sortedOrgs


def CaptureCurve():	
	for i in range(int(cmds.playbackOptions(query=True, min=True)), int(cmds.playbackOptions(query=True, max=True) + 1)):
	   origEval.append( cmds.keyframe( origCurve,query=True,time=(i,i), eval=True ))

def NextGen():
	sortedCosts = []
	for o in pop.organisms:
		o.UpdateCost(origCurve,origEval)
	pop.SortLowestCost()
	pop.organisms[0].SetCurve(origCurve)
	pop.BreedNextGen()



origCurve = cmds.animCurveEditor('graphEditor1GraphEd', query=True, curvesShown=True)
origEval = []
pop = None
pop = population(30,0.5,0.5,1)

'''
keyTimes = [0,15,30]
keyValues = [0.0,15,0.0]
bredCurves = cmds.createNode( 'animCurveUU', name='BredCurves')

for id in range(0,100):
    name = 'Gen' + str(5) + 'id' + str(id)
    cmds.addAttr(bredCurves, attributeType="float", ln=name, keyable=True)


for at in cmds.listAttr(bredCurves):
    if at.__contains__('7'):
        cmds.deleteAttr(bredCurves,attribute=at)
    print at

for k in range(len(keyTimes)):
    cmds.setKeyframe(bredCurves, attribute='attr', time=keyTimes[k], value=keyValues[k])


totalErr = 0.0
for i in range(int(cmds.playbackOptions(query=True, min=True)), int(cmds.playbackOptions(query=True, max=True) + 1)):
	cost = cmds.keyframe( 'pCube1_translateZ',query=True,time=(i,i), eval=True )[0] - cmds.keyframe( bredCurves, attribute='attr',query=True,time=(i,i), eval=True )[0]
	totalErr += cost * cost
    
print totalErr
'''