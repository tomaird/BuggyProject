from random import *

#testString = "*#*#*#*#A0507A0604D0206B0001D1302D1000A1307*0003*0303*0405*0705*1104*1107*0600*1713*#"

class coordGen:
    def __init__(self):
        self.preamble = "*#*#*#*#"
        self.postamble = "*#"
        self.directions = ['A','B','C','D']
        self.maxX = 13
        self.maxY = 9
        self.finalBlockers = []

        self.genBlockers()
        self.translateBlockers()
        self.genTargets()
        self.translateTargets()
    
    def genBlockers(self):
        i = 0
        while True:
            tempBlockers = []
            startX = randint(0,self.maxX)
            startY = randint(0,self.maxY)
            tempBlockers.append((startX,startY))
            direction = randint(0,3) #0=North, 1=East, 2=South, 3=West
            if direction == 0: #North
                tempBlockers.append((startX,startY+1))
                tempBlockers.append((startX,startY+2))
                tempBlockers.append((startX,startY+3))
            elif direction == 1: #East
                tempBlockers.append((startX+1,startY))
                tempBlockers.append((startX+2,startY))
                tempBlockers.append((startX+3,startY))
            elif direction == 2: #South
                tempBlockers.append((startX,startY-1))
                tempBlockers.append((startX,startY-2))
                tempBlockers.append((startX,startY-3))
            elif direction == 3: #West
                tempBlockers.append((startX-1,startY))
                tempBlockers.append((startX-2,startY))
                tempBlockers.append((startX-3,startY))
            if self.testBlockers(tempBlockers):
                for blocker in tempBlockers:
                    self.finalBlockers.append(blocker)
                i+=1
            if i>3:
                break
            
    def getFinal(self):
        return self.finalBlockers

    def translateBlockers(self):
        self.blockerString = ""
        for i in range(4):
            x1 = self.finalBlockers[4*i][0]
            y1 = self.finalBlockers[4*i][1]
            x2 = self.finalBlockers[4*i+3][0]
            y2 = self.finalBlockers[4*i+3][1]
            newBlocker = "*" + str(x1).zfill(2) + str(y1).zfill(2) + "*" + str(x2).zfill(2) + str(y2).zfill(2)
            self.blockerString = self.blockerString + newBlocker

    def testBlockers(self,blockers):
        for blocker in blockers:
            if blocker[0]>self.maxX or blocker[0]<0 or blocker[1]>self.maxY or blocker[1]<0:
                return False
            elif blocker in self.finalBlockers:
                return False
        return True

    def genTargets(self):
        i = 0
        self.finalTargets = []
        while True:
            targetX = randint(0,self.maxX)
            targetY = randint(0,self.maxY)
            direction = self.directions[randint(0,3)]
            if self.testTarget(targetX,targetY,direction):
                self.finalTargets.append((targetX,targetY,direction))
                i+=1
            if i>6:
                break

    def translateTargets(self):
        self.targetString = ""
        for target in self.finalTargets:
            x = target[0]
            y = target[1]
            dirn = target[2]
            newTarget = dirn + str(x).zfill(2) + str(y).zfill(2)
            self.targetString = self.targetString + newTarget


    def testTarget(self,x,y,direction):
        if x>self.maxX or x<0 or y>self.maxY or y<0:
            return False
        elif (x,y) in self.finalBlockers:
            return False
        elif (x,y,direction) in self.finalTargets:
            return False
        else:
            return True

    def getFinalString(self):
        self.finalString = self.preamble + self.targetString + self.blockerString + self.postamble
        return self.finalString

##newGen = coordGen()
##newString = newGen.getFinalString()
##print(newString)
