from buggyGUI_v4 import *
from algorithm_v4 import *
from decipher_v2 import *
from instructions import *
from coordGen import *
from wifi import *
from calculate import *

from tkinter import messagebox
import serial
import time

class mainApp():
    def __init__(self):
        self.stepTime = 100
        self.maxX = 13
        self.maxY = 9
        self.start = (1,0)
        self.finalPath = [(1,-5,'m'),(1,-4,'m'),(1,-3,'m'),(1,-2,'m'),(1,-1,'m'),(1,0,'m')]
        self.finalPos = [1,-5,'N']
        #self.defaultString = "*#*#*#*#A0507A0604D0206C0103D1302D0900A1307*0004*0304*0405*0705*1104*1107*1300*1713*#"
        self.defaultString = "*#*#*#*#A0507A0604D0206C0102D1302D0900A1307*0004*0304*0405*0705*1104*1107*1300*1713*#"
        self.string = self.defaultString
        self.root = Tk()
        self.updateNum = 0
        self.noSerial = 0

        self.displayBaseGUI()

    def displayBaseGUI(self):
        self.newGUI = GUI(self.maxX,self.maxY,self.root)
        self.newGUI.createLayout()
        self.root.after(self.stepTime,self.waitForStart)
        self.newGUI.createGUI()

    def waitForStart(self):
        if self.newGUI.getStart() == 0:
            self.root.after(self.stepTime,self.waitForStart)
        else:
            if self.newGUI.getNoSerial() == 0:
                self.noSerial = 0
            else:
                self.noSerial = 1
            if self.newGUI.getStringType() == 1: #Default
                self.string = self.defaultString
            elif self.newGUI.getStringType() == 2: #Random
                newGen = coordGen()
                self.string = newGen.getFinalString()
            elif self.newGUI.getStringType() == 3: #Input
                self.string = self.newGUI.getString()
            elif self.newGUI.getStringType() == 4: #WiFi
                newWifi = wificlass()
                newWifi.connect("maze_beacon_1")
                time.sleep(10)
                self.string = newWifi.getString()
            elif self.newGUI.getStringType() == 5: #TextFile
                file = open("maze_string.txt")
                self.string = file.read()
            elif self.newGUI.getStringType() == 6: #WiFi Trial
                newWifi = wificlass()
                newWifi.connect("maze_beacon")
                time.sleep(10)
                self.string = newWifi.getString() 
            self.root.after(self.stepTime,self.decipherString())

    def decipherString(self):
        self.dec1 = decipher(self.string,self.maxX+1,self.maxY+1)
        if self.dec1.checkString() == 0:
            if self.newGUI.getOverride() == 0:
                messagebox.showerror("Error", "Invalid Coordinate String")
                quit()
            else:
                 messagebox.showerror("Error", "Invalid coordinate string. Continuing anyway...")
        self.dec1.decipherBlockers()
        self.dec1.decipherTargets()
        self.dec1.getTargetApproach()
        self.displayBlockers = self.dec1.getBlockers()
        self.allBlockers = self.displayBlockers[:]
        self.targets = self.dec1.getTargets()
        self.marginBlockers = self.dec1.getMarginBlockers()
        for blocker in self.marginBlockers:
            self.allBlockers.append(blocker)
        for target in self.targets:
            self.allBlockers.append((target.xPos,target.yPos))
        self.remainingTargets = self.targets[:]
        self.displayLocations()

    def displayLocations(self):
        self.newGUI.addBlockers(self.displayBlockers)
        self.newGUI.addBoxes(self.targets)
        self.newGUI.displayBuggy(1,-5,'N')
        self.newGUI.updateStatus("Initiating connection")
        self.root.update()
        self.root.after(self.stepTime,self.initConnection)

    def initConnection(self):
        self.newGUI.updateStatus("Initiating connection")
        comNum = self.newGUI.getPort()
        serPort = "COM"+comNum
        #serPort = "COM20"
        baudRate = 38400
        timeout = 0
        self.ser = serial.Serial()
        self.ser.baudrate = baudRate
        self.ser.port = serPort
        self.ser.timeout = timeout
        if self.noSerial == 0:
            try:
                self.ser.open()
            except:
                messagebox.showerror("Error", "Error opening %s." % self.ser.name)
                #quit()
            #Send test to Arduino to check it is online
            initString = "T"
            while(1):
                self.ser.reset_input_buffer()
                self.ser.write(initString.encode())
                startTime = time.clock()
                timedOut = 0
                while self.ser.inWaiting() == 0:
                    curTime = time.clock()
                    if curTime > startTime + 7:
                        timedOut = 1
                        break
                if timedOut == 0:
                    break
            recvdData = self.ser.readline().decode().strip()
            self.newGUI.updateStatus("Connected")
        self.planFirstRoute()

    def planFirstRoute(self):
        #Find closest box from start point
        possiblePaths = [] #Paths to all possible boxes
        pathLengths = [] #Lengths of routes to each box to compare to find shortest
        #Work out which box is closest to start
        for i in range(len(self.remainingTargets)):
            if self.start == (self.remainingTargets[i].x,self.remainingTargets[i].y):
                pathX = []
            else:
                newRoute = routeFind()
                newRoute.createGrid(self.maxX+1,self.maxY+1,self.allBlockers,self.start,
                            (self.remainingTargets[i].x,self.remainingTargets[i].y))
                pathX = newRoute.algorithm()
            if pathX == 0:
                self.remainingTargets[i] = self.dec1.swapApproach(self.remainingTargets[i])
                newRoute = routeFind()
                newRoute.createGrid(self.maxX+1,self.maxY+1,self.allBlockers,self.start,
                            (self.remainingTargets[i].x,self.remainingTargets[i].y))
                pathX = newRoute.algorithm()
                if pathX == 0:
                    messagebox.showerror("Error", "No route found")
                    quit()
            possiblePaths.append(pathX)
            pathLengths.append(len(pathX))
        #Select path to closes box and add to final route
        shortestPathIndex = pathLengths.index(min(pathLengths))
        shortestPath = possiblePaths[shortestPathIndex]
        for coord in shortestPath:
            self.finalPath.append(coord.__add__(tuple('m'))) #add coords to final path, appending 'm'
        closestBox = self.remainingTargets[shortestPathIndex]
        self.finalPath.append((closestBox.xPos,closestBox.yPos,'b',closestBox.num,closestBox.direction))
        #Remove selected target from remainingTargets
        self.nextStartX = closestBox.x
        self.nextStartY = closestBox.y
        self.closestBox = closestBox
        self.remainingTargets.remove(self.closestBox)
        
        self.displayRoute()

    def displayRoute(self):
        self.root.after(self.stepTime,self.translateInstr)
        self.newGUI.displayRoute(self.finalPath)

    def translateInstr(self):
        self.trans = instructions(self.finalPath,self.finalPos)
        self.instructions = self.trans.getInstructions()
        self.finalPos = self.trans.getFinalPos()
        self.newGUI.updateStatus("Sending instructions")
        self.root.after(self.stepTime,self.sendInstructions)

    def sendInstructions(self):
        instr = self.instructions[self.updateNum]
        if self.noSerial == 0:
            self.ser.reset_input_buffer()
            ## SEND INSTRUCTION
            self.ser.write(instr.encode())
            #print("Sent "+str(instr))
            ## WAIT FOR ACKNOWLEDGEMENT
            while self.ser.inWaiting() == 0:
                pass
            recvdData = self.ser.readline().decode().strip()
            expectedAck = str(instr) + " Done"
        #if recvdData != expectedAck:
            #messagebox.showerror("Error", "Incorrect acknowledgement received")
        #print("Received from Arduino: "+recvdData)
        self.newGUI.updateBuggy(instr)
        self.updateNum += 1
        if self.updateNum >= len(self.instructions)-1:
            instr = self.instructions[self.updateNum]
            self.updateNum = 0
            self.newGUI.updateStatus("Sensing")
            self.root.update()
            self.root.after(self.stepTime,self.senseData(instr))
        else:
            self.root.after(self.stepTime,self.sendInstructions)

    def senseData(self,finalInstr):
        if self.noSerial == 0:
            self.ser.reset_input_buffer()
            self.ser.write(finalInstr.encode()) # Send final part of sense instruction (direction)
            #print("Sensing data. Box: "+str(self.closestBox.num)+" Direction: "+self.closestBox.direction)
            recvdData = []
            while(1):
                while self.ser.inWaiting() == 0:
                    pass
                recvdByte = self.ser.readline().decode().strip()
                if recvdByte == ">":
                    break
                else:
                    recvdData.append(recvdByte)
            newCalc = calculate()
            try:
                calcVals = newCalc.calcValues(self.closestBox.num,self.closestBox.direction,recvdData)
                for i in range(int(len(calcVals)/2)):
                    param = calcVals[2*i]
                    val = calcVals[2*i+1]
                    self.newGUI.updateVal(self.closestBox.num,param,val)
            except:
                #messagebox.showerror("Error", "Unable to read values")
                pass
        self.newGUI.updateBoxDot(self.closestBox.xPos,self.closestBox.yPos)
        if self.noSerial == 0:
            while self.ser.inWaiting() == 0:
                pass
            recvdData = self.ser.readline().decode().strip()
            expectedAck = str(instr) + " Done"
        if len(self.remainingTargets) == 0:
            self.newGUI.updateStatus("Victory rolling")
            self.root.after(self.stepTime,self.victoryRoll)
        else:
            self.root.after(self.stepTime,self.planNextRoute)

    def planNextRoute(self):
        self.finalPath = []
        possiblePaths = [] #Paths to all possible boxes
        pathLengths = [] #Lengths of routes to each box to compare to find shortest
        #Work out which box is closest to start
        for i in range(len(self.remainingTargets)):
            newRoute = routeFind()
            newRoute.createGrid(self.maxX+1,self.maxY+1,self.allBlockers,
                (self.nextStartX,self.nextStartY),
                    (self.remainingTargets[i].x,self.remainingTargets[i].y))
            pathX = newRoute.algorithm()
            if pathX == 0:
                    messagebox.showerror("Error", "No route found")
                    quit()
            possiblePaths.append(pathX)
            pathLengths.append(len(pathX))
        #Select path to closest box and add to final route
        shortestPathIndex = pathLengths.index(min(pathLengths))
        shortestPath = possiblePaths[shortestPathIndex]
        for coord in shortestPath:
            self.finalPath.append(coord.__add__(tuple('m'))) #add coords to final path, appending 'm'
        closestBox = self.remainingTargets[shortestPathIndex]
        self.finalPath.append((closestBox.xPos,closestBox.yPos,'b',closestBox.num,closestBox.direction))
        #Remove selected target from remainingTargets
        self.nextStartX = closestBox.x
        self.nextStartY = closestBox.y
        self.closestBox = closestBox
        self.remainingTargets.remove(self.closestBox)

        self.displayRoute()

    def victoryRoll(self):
        [xVic,yVic] = self.trans.victoryRollPos()
        if (xVic,yVic) in self.allBlockers or xVic>self.maxX or xVic<0 or yVic>self.maxY or yVic<0: #Can't do forward roll
            [xVic,yVic] = self.trans.victoryRollAdjustL()
            addInstr = 'L'
            if (xVic,yVic) in self.allBlockers or xVic>self.maxX or xVic<0 or yVic>self.maxY or yVic<0: #Can't do L
                [xVic,yVic] = self.trans.victoryRollAdjustR()
                addInstr = 'R'
                if (xVic,yVic) in self.allBlockers or xVic>self.maxX or xVic<0 or yVic>self.maxY or yVic<0: #Can't do R
                    messagebox.showerror("Error", "Unable to do victory roll")
                    quit()
            if self.noSerial == 0:
                self.ser.reset_input_buffer()
                self.ser.write(addInstr.encode())
                #print("Sent "+str(addInstr))
                while self.ser.inWaiting() == 0:
                    pass
                recvdData = self.ser.readline().decode().strip()
                expectedAck = str(addInstr) + " Done"
            #if recvdData != expectedAck:
                #messagebox.showerror("Error", "Incorrect acknowledgement received")
            #print("Received from Arduino: "+recvdData)
        instr = 'V'
        if self.noSerial == 0:
            self.ser.reset_input_buffer()
            self.ser.write(instr.encode())
            #print("Sent "+str(instr))
            while self.ser.inWaiting() == 0:
                pass
            recvdData = self.ser.readline().decode().strip()
            expectedAck = str(instr) + " Done"
        #if recvdData != expectedAck:
            #messagebox.showerror("Error", "Incorrect acknowledgement received")
        #print("Received from Arduino: "+recvdData)
        self.newGUI.updateStatus("Finished")
        

#testString = "*#*#*#*#A0507A0604D0206B0001D1302D1000A1307*0003*0303*0405*0705*1104*1107*0600*1713*#"
#testString2 = "*#*#*#*#B0600A0602D0004B1309D0607D1105A0308*0201*0501*0802*1102*0009*0309*0609*1713*#"

main = mainApp()


