class instructions:
    def __init__(self,coords,startPos=[1,-5,'N']):
        self.path = coords
        self.instructions = [] # F = Forward one, B = Backward one, L = Rotate 90 left, R = Rotate 90 right, Q = Rotate 180, S = sense box
        self.curDirection = startPos[2] # N = North, S = South, E = East, W = West
        self.curCoord = (startPos[0],startPos[1])
        self.curType = 'm'
        self.nextCoord = (1,-4)
        self.translate()

    def translate(self):
        for i in range(-1,len(self.path)-1):
            if i != -1:
                self.curCoord = self.path[i][0:2]
                self.curType = self.path[i][2]
            self.nextCoord = self.path[i+1][0:2]
            self.nextType = self.path[i+1][2]
            if self.curType == 'b':
                self.curCoord = self.path[i-1][0:2] #After sensing, already returned to previous square
            if self.nextType == 'b':
                self.boxNum = self.path[i+1][3]
                self.boxDir = self.path[i+1][4]
                if self.nextCoord[0] == self.curCoord[0]+2: #X+1,move E
                    if self.curDirection == 'E':
                        self.instructions.append('S')
                    elif self.curDirection == 'N':
                        self.instructions.append('R')
                        self.instructions.append('S')
                    elif self.curDirection == 'S':
                        self.instructions.append('L')
                        self.instructions.append('S')
                    elif self.curDirection == 'W':
                        self.instructions.append('Q')
                        self.instructions.append('S')
                    self.curDirection = 'E'
                elif self.nextCoord[0] == self.curCoord[0]-2: #X-1,move W
                    if self.curDirection == 'W':
                        self.instructions.append('S')
                    elif self.curDirection == 'S':
                        self.instructions.append('R')
                        self.instructions.append('S')
                    elif self.curDirection == 'N':
                        self.instructions.append('L')
                        self.instructions.append('S')
                    elif self.curDirection == 'E':
                        self.instructions.append('Q')
                        self.instructions.append('S')
                    self.curDirection = 'W'
                elif self.nextCoord[1] == self.curCoord[1]+2: #Y+1,move N
                    if self.curDirection == 'N':
                        self.instructions.append('S')
                    elif self.curDirection == 'W':
                        self.instructions.append('R')
                        self.instructions.append('S')
                    elif self.curDirection == 'E':
                        self.instructions.append('L')
                        self.instructions.append('S')
                    elif self.curDirection == 'S':
                        self.instructions.append('Q')
                        self.instructions.append('S')
                    self.curDirection = 'N'
                elif self.nextCoord[1] == self.curCoord[1]-2: #Y-1,move S
                    if self.curDirection == 'S':
                        self.instructions.append('S')
                    elif self.curDirection == 'E':
                        self.instructions.append('R')
                        self.instructions.append('S')
                    elif self.curDirection == 'W':
                        self.instructions.append('L')
                        self.instructions.append('S')
                    elif self.curDirection == 'N':
                        self.instructions.append('Q')
                        self.instructions.append('S')
                    self.curDirection = 'S'
                self.instructions.append(str(self.boxNum))
                #Calculating whether facing knob or not
                self.facingDir = 'f' # f = front (knob), b = back (no knob)
                if self.curDirection == 'N':
                    if self.boxDir == 'A':
                        self.facingDir = 'b'
                    else:
                        self.facingDir = 'f'
                elif self.curDirection == 'S':
                    if self.boxDir == 'A':
                        self.facingDir = 'f'
                    else:
                        self.facingDir = 'b'
                elif self.curDirection == 'E':
                    if self.boxDir == 'B':
                        self.facingDir = 'b'
                    else:
                        self.facingDir = 'f'
                elif self.curDirection == 'W':
                    if self.boxDir == 'B':
                        self.facingDir = 'f'
                    else:
                        self.facingDir = 'b'
                self.instructions.append(self.facingDir)
            if self.nextType == 'm':
                if self.nextCoord[0] == self.curCoord[0]+1: #X+1,move E
                    if self.curDirection == 'E':
                        self.instructions.append('F')
                    elif self.curDirection == 'N':
                        self.instructions.append('R')
                        self.instructions.append('F')
                    elif self.curDirection == 'S':
                        self.instructions.append('L')
                        self.instructions.append('F')
                    elif self.curDirection == 'W':
                        self.instructions.append('Q')
                        self.instructions.append('F')
                    self.curDirection = 'E'
                elif self.nextCoord[0] == self.curCoord[0]-1: #X-1,move W
                    if self.curDirection == 'W':
                        self.instructions.append('F')
                    elif self.curDirection == 'S':
                        self.instructions.append('R')
                        self.instructions.append('F')
                    elif self.curDirection == 'N':
                        self.instructions.append('L')
                        self.instructions.append('F')
                    elif self.curDirection == 'E':
                        self.instructions.append('Q')
                        self.instructions.append('F')
                    self.curDirection = 'W'
                elif self.nextCoord[1] == self.curCoord[1]+1: #Y+1,move N
                    if self.curDirection == 'N':
                        self.instructions.append('F')
                    elif self.curDirection == 'W':
                        self.instructions.append('R')
                        self.instructions.append('F')
                    elif self.curDirection == 'E':
                        self.instructions.append('L')
                        self.instructions.append('F')
                    elif self.curDirection == 'S':
                        self.instructions.append('Q')
                        self.instructions.append('F')
                    self.curDirection = 'N'
                elif self.nextCoord[1] == self.curCoord[1]-1: #Y-1,move S
                    if self.curDirection == 'S':
                        self.instructions.append('F')
                    elif self.curDirection == 'E':
                        self.instructions.append('R')
                        self.instructions.append('F')
                    elif self.curDirection == 'W':
                        self.instructions.append('L')
                        self.instructions.append('F')
                    elif self.curDirection == 'N':
                        self.instructions.append('Q')
                        self.instructions.append('F')
                    self.curDirection = 'S'

    def getInstructions(self):
        return self.instructions

    def getFinalPos(self):
        finalPos = [self.curCoord[0],self.curCoord[1],self.curDirection]
        return finalPos

    def victoryRollPos(self):
        [x,y,dirn] = self.getFinalPos()
        xVic = x
        yVic = y
        if dirn == 'N':
            yVic = y-1
        if dirn == 'E':
            xVic = x-1
        if dirn == 'W':
            xVic = x+1
        if dirn == 'S':
            yVic = y+1
        return [xVic,yVic]

    def victoryRollAdjustR(self): # rotate 90 right
        [x,y,dirn] = self.getFinalPos()
        xVic = x
        yVic = y
        if dirn == 'N':
            xVic = x-1
        if dirn == 'E':
           yVic = y+1
        if dirn == 'W':
            yVic = y-1
        if dirn == 'S':
            xVic = x+1
        return [xVic,yVic]

    def victoryRollAdjustL(self): # rotate 90 left
        [x,y,dirn] = self.getFinalPos()
        xVic = x
        yVic = y
        if dirn == 'N':
            xVic = x+1
        if dirn == 'E':
           yVic = y-1
        if dirn == 'W':
            yVic = y+1
        if dirn == 'S':
            xVic = x-1
        return [xVic,yVic]