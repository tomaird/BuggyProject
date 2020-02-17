class target():
    def __init__(self,x,y,direction,num):
        self.xPos = x           #Box position
        self.yPos = y
        self.xPos1 = x          #1 square in front of box
        self.yPos1 = y
        self.direction = direction
        self.x = x              #2 in front of box: approach coordinate
        self.y = y
        self.num = num          #Box number
        

class decipher():
    def __init__(self,string,xLen,yLen):
        self.string = string
        self.xLen = xLen
        self.yLen = yLen
        self.targets = []
        self.blockers = []
        self.marginBlockers = []

    def checkString(self):
        if self.string.startswith("*#*#*#*#") != 1:
            return False
        if self.string.endswith("*#") != 1:
            return False
        if len(self.string) != 85:
            return False
        return True


    #Deciphers target details and adds to internal array
    def decipherTargets(self):
        targetString = self.string[8:43]
        for i in range(7):
            targetX = targetString[5*i:5*i+5]
            x = int(targetX[1:3])
            y = int(targetX[3:5])
            direction = targetX[0]
            self.targets.append(target(x,y,direction,i+1))

    def getTargets(self):
        return self.targets

    def getTargetApproach(self):
        for target in self.targets:
            if target.direction == 'A': #north
                testX = target.xPos
                testY = target.yPos + 2
                if self.testTargetApproach(testX,testY):
                    target.x = testX
                    target.y = testY
                    target.yPos1 = target.yPos + 1
                else:
                    target.x = target.xPos
                    target.y = target.yPos - 2
                    target.yPos1 = target.yPos - 1
            elif target.direction == 'B': #east
                testX = target.xPos + 2
                testY = target.yPos
                if self.testTargetApproach(testX,testY):
                    target.x = testX
                    target.y = testY
                    target.xPos1 = target.xPos + 1
                else:
                    target.x = target.xPos - 2
                    target.y = target.yPos
                    target.xPos1 = target.xPos - 1
            elif target.direction == 'C': #south
                testX = target.xPos
                testY = target.yPos - 2
                if self.testTargetApproach(testX,testY):
                    target.x = testX
                    target.y = testY
                    target.yPos1 = target.yPos - 1
                else:
                    target.x = target.xPos
                    target.y = target.yPos + 2
                    target.yPos1 = target.yPos + 1
            elif target.direction == 'D': #west
                testX = target.xPos - 2
                testY = target.yPos
                if self.testTargetApproach(testX,testY):
                    target.x = testX
                    target.y = testY
                    target.xPos1 = target.xPos - 1
                else:
                    target.x = target.xPos + 2
                    target.y = target.yPos
                    target.xPos1 = target.xPos + 1

    def testTargetApproach(self,x,y):
        if x>13 or x<0 or y>9 or y<0:
            return 0
        for blocker in self.blockers:
            if blocker == (x,y):
                return 0
        for target in self.targets:
            if target.xPos == x and target.yPos == y:
                return 0
        return 1

    #Deciphers blocker details, splits into start/end coords
    def decipherBlockers(self):
        blockerString = self.string[43:83]
        for i in range(4):
            blocker1 = blockerString[10*i:10*i+5]
            blocker2 = blockerString[10*i+5:10*i+10]
            x1 = int(blocker1[1:3])
            y1 = int(blocker1[3:5])
            x2 = int(blocker2[1:3])
            y2 = int(blocker2[3:5])
            #First coord out of bounds, add second coord to edge
            if x1>self.xLen or y1>self.yLen:
                #To right edge
                if x2>=(self.xLen-3):
                    for j in range(self.xLen-x2):
                        self.blockers.append((x2+j,y2))
                #To left edge
                elif x2<=2:
                    for j in range(x2+1):
                        self.blockers.append((x2-j,y2))
                #To top edge
                elif y2>=(self.yLen-3):
                    for j in range(self.yLen-y2):
                        self.blockers.append((x2,y2+j))
                #To bottom edge
                elif y2<=2:
                    for j in range(y2+1):
                        self.blockers.append((x2,y2-j))
            #Second coord out of bounds, add first coord to edge
            elif x2>self.xLen or y2>self.yLen:
                #To right edge
                if x1>=(self.xLen-3):
                    for j in range(self.xLen-x1):
                        self.blockers.append((x1+j,y1))
                #To left edge
                elif x1<=2:
                    for j in range(x1+1):
                        self.blockers.append((x1-j,y1))
                #To top edge
                elif y1>=(self.yLen-3):
                    for j in range(self.yLen-y1):
                        self.blockers.append((x1,y1+j))
                #To bottom edge
                elif y1<=2:
                    for j in range(y1+1):
                        self.blockers.append((x1,y1-j))
            else:
                self.blockers.append((x1,y1))
                self.blockers.append((x2,y2))
                if (x1 != x2) and (y1 != y2):
                    print("error in blocker coordinate pairings")
                    return
                if x1 > x2:
                    for i in range(x1-x2):
                        self.blockers.append((x2+i,y1))
                elif x1 < x2:
                    for i in range(x2-x1):
                        self.blockers.append((x1+i,y1))
                elif y1 > y2:
                    for i in range(y1-y2):
                        self.blockers.append((x1,y2+i))
                elif y1 < y2:
                    for i in range(y2-y1):
                        self.blockers.append((x1,y1+i))

    def getBlockers(self):
        return self.blockers

    def getMarginBlockers(self):
        self.marginBlockers = []
        for box in self.targets:
            tempBlocker = []
            tempBlocker.append((box.xPos,box.yPos+1))
            tempBlocker.append((box.xPos,box.yPos-1))
            tempBlocker.append((box.xPos-1,box.yPos))
            tempBlocker.append((box.xPos+1,box.yPos))
            tempBlocker.append((box.xPos+1,box.yPos+1))
            tempBlocker.append((box.xPos+1,box.yPos-1))
            tempBlocker.append((box.xPos-1,box.yPos+1))
            tempBlocker.append((box.xPos-1,box.yPos-1))
            for block in tempBlocker:
                if (block in self.blockers): #already in list
                    pass
                elif block[0]<0 or block[0]>=self.xLen or block[1]<0 or block[1]>=self.yLen: #Out of arena
                    pass
                else:
                    self.marginBlockers.append(block)
        for blocker in self.blockers:
            tempBlocker = []
            tempBlocker.append((blocker[0],blocker[1]+1))
            tempBlocker.append((blocker[0],blocker[1]-1))
            tempBlocker.append((blocker[0]-1,blocker[1]))
            tempBlocker.append((blocker[0]+1,blocker[1]))
            tempBlocker.append((blocker[0]+1,blocker[1]+1))
            tempBlocker.append((blocker[0]+1,blocker[1]-1))
            tempBlocker.append((blocker[0]-1,blocker[1]+1))
            tempBlocker.append((blocker[0]-1,blocker[1]-1))
            for block in tempBlocker:
                if (block in self.blockers): #already in list
                    pass
                elif block[0]<0 or block[0]>=self.xLen or block[1]<0 or block[1]>=self.yLen: #Out of arena
                    pass
                else:
                    self.marginBlockers.append(block)

        return self.marginBlockers

    def swapApproach(self,target):
        tempTarget = target
        if target.x == target.xPos+2:
            tempTarget.x = tempTarget.xPos-2
        elif target.x == target.xPos-2:
            tempTarget.x = tempTarget.xPos+2
        elif target.y == target.yPos+2:
            tempTarget.y = tempTarget.yPos-2
        elif target.y == target.yPos-2:
            tempTarget.y = tempTarget.yPos+2
        if tempTarget.x >= self.xLen or tempTarget.x < 0 or tempTarget.y >=self.yLen or tempTarget.y < 0:
            return target
        return tempTarget

                


##testString = "*#*#*#*#A0507A0604D0206B0001" \
##"D1302D1000A1307*0003*0303*0405*0705*1104*1107*0600*1713*#"
##a = decipher(testString)
##a.decipherTargets()
##targets = a.getTargets()
##a.decipherBlockers()
##blockers = a.getBlockers()
##for blocker in blockers:
##    print(blocker)

    
