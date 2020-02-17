#importing tkinter modules
from tkinter import *

#importing algorithm files
from algorithm_v4 import *
from decipher_v2 import *

class GUI:
    def __init__(self,xLen,yLen,root):
        self.xLen = xLen
        self.yLen = yLen
        self.n = 5
        self.curXPos = 1
        self.curYPos = -5
        self.curDir = 'N'
        self.start = 0
        self.defaultCOM = "7"
        self.noSerial = IntVar()
        self.stringTypeVar = IntVar()
        self.overrideVar = IntVar()
        #tkinter window initialisation
        self.root = root
        self.root.title("Buggy GUI")
        #self.root.wm_iconbitmap('buggyIcon.ico')

    def createLayout(self):
        self.mainGrid = Frame(self.root,bg="red",height=self.n*110,width=self.n*150)
        self.midGrid = Frame(self.root,bg="red",height=self.n*20,width=self.n*20)
        self.startGrid = Frame(self.root,bg="red",height=self.n*40,width=self.n*40)
        self.midLeft = Frame(self.root,bg="grey",height=self.n*20,width=self.n*10)
        self.botRight = Frame(self.root,bg="grey",height=self.n*60,width=self.n*110)
        self.midRight = Frame(self.root,bg="grey",height=self.n*20,width=self.n*10)
        self.rowLabels = Frame(self.root,bg="blue",height=self.n*170,width=self.n*10)
        self.colLabels = Frame(self.root,bg="blue",height=self.n*10,width=self.n*160)
        self.infoRegion = Frame(self.root,bg="grey90",height=self.n*130,width=self.n*100)
        self.optionsRegion = Frame(self.root,bg="grey90",height=self.n*50,width=self.n*100)
        self.mainGrid.grid(row=0,column=1,columnspan=4)
        self.midGrid.grid(row=1,column=2)
        self.startGrid.grid(row=2,column=1,columnspan=3)
        self.midLeft.grid(row=1,column=1)
        self.botRight.grid(row=1,column=4,rowspan=2)
        self.midRight.grid(row=1,column=3)
        self.rowLabels.grid(row=0,column=0,rowspan=3)
        self.colLabels.grid(row=3,column=0,columnspan=5)
        self.infoRegion.grid(row=0,column=5,rowspan=2)
        self.optionsRegion.grid(row=2,column=5,rowspan=2)
        self.addGrid()
        self.addCoordLabels()
        self.addOptions()
        self.addBaseInfo()

    def addGrid(self):
        self.frame2 = Frame(self.mainGrid)
        self.frame2.pack()
        for x in range(15):
            for y in range(11):
                if (x+y)%2:
                    colour = "black"
                else:
                    colour = "white"
                newCanvas = Frame(self.frame2,bd=5,bg=colour,
                                  height=self.n*10,width=self.n*10)
                newCanvas.grid(row=y,column=x)
        self.frame3 = Frame(self.midGrid)
        self.frame3.pack()
        for x in range(2):
            for y in range(2):
                if (x+y)%2:
                    colour = "black"
                else:
                    colour = "white"
                newCanvas = Frame(self.frame3,bd=5,bg=colour,
                                  height=self.n*10,width=self.n*10)
                newCanvas.grid(row=y,column=x)
        self.frame4 = Frame(self.startGrid)
        self.frame4.pack()
        for x in range(4):
            for y in range(4):
                if (x+y)%2:
                    colour = "white"
                else:
                    colour = "black"
                newCanvas = Frame(self.frame4,bd=5,bg=colour,
                                  height=self.n*10,width=self.n*10)
                newCanvas.grid(row=y,column=x)

    def addCoordLabels(self):
        #Row labels
        self.rowFrame = Frame(self.rowLabels)
        self.rowFrame.pack()
        newLabel = Frame(self.rowFrame,
                              height=self.n*5,width=self.n*10)
        newLabel.grid(row=0,column=0)
        for y in range(16):
            labelText = 9-y
            newLabel = Frame(self.rowFrame,
                              height=self.n*10,width=self.n*10)
            newLabel.grid(row=y,column=0)
            Label(newLabel,text=labelText).place(relx=0.3,rely=0.2)
        #Column labels
        self.colFrame = Frame(self.colLabels)
        self.colFrame.pack()
        newLabel = Frame(self.colFrame,
                              height=self.n*10,width=self.n*15)
        newLabel.grid(row=0,column=0)
        for x in range(14):
            labelText = x
            newLabel = Frame(self.colFrame,
                              height=self.n*10,width=self.n*10)
            newLabel.grid(row=0,column=x+1)
            Label(newLabel,text=labelText).place(relx=0.1,rely=0.3)

    def addOptions(self):
        self.optionsFrame = Frame(self.optionsRegion) #Top level frame
        self.optionsFrame.pack()
        self.optionsTitle = Label(self.optionsFrame,text="Options",font=("Verdana",20,"bold"))  #Title
        self.optionsTitle.pack()
        self.overrideButton = Checkbutton(self.optionsFrame,text="Override string errors",variable=self.overrideVar)
        self.overrideButton.pack()
        self.stringOptionsFrame = Frame(self.optionsFrame)      #Frame for radio buttons
        self.stringOptionsFrame.pack()
        self.radio1 = Radiobutton(self.stringOptionsFrame,text="Default",variable=self.stringTypeVar,value=1)
        self.radio1.pack(side=LEFT)
        self.radio1.select()
        self.radio2 = Radiobutton(self.stringOptionsFrame,text="Random",variable=self.stringTypeVar,value=2)
        self.radio2.pack(side=LEFT)
        self.radio3 = Radiobutton(self.stringOptionsFrame,text="Input",variable=self.stringTypeVar,value=3)
        self.radio3.pack(side=LEFT)
        self.radio4 = Radiobutton(self.stringOptionsFrame,text="WiFi1",variable=self.stringTypeVar,value=4)
        self.radio4.pack(side=LEFT)
        self.radio4a = Radiobutton(self.stringOptionsFrame,text="WiFi Trial",variable=self.stringTypeVar,value=6)
        self.radio4a.pack(side=LEFT)
        self.radio5 = Radiobutton(self.stringOptionsFrame,text="Text file",variable=self.stringTypeVar,value=5)
        self.radio5.pack(side=LEFT)
        self.stringEntry = Entry(self.optionsFrame)
        self.stringEntry.pack()
        self.serialFrame = Frame(self.optionsFrame)
        self.serialFrame.pack()
        self.noSerialButton = Checkbutton(self.serialFrame,text="No serial",variable=self.noSerial,padx=30)    #No serial button
        self.noSerialButton.pack(side=LEFT)
        self.portEntry = Entry(self.serialFrame,width=3)
        self.portEntry.pack(side=LEFT)
        self.portEntry.insert(0,self.defaultCOM)
        self.portText = Label(self.serialFrame,text="COM Port",padx=5)
        self.portText.pack(side=LEFT)
        self.startButton = Button(self.optionsFrame,text="Start",command=self.setStart)     #Start button
        self.startButton.pack()

    def setStart(self):
        self.start = 1

    def getStart(self):
        return self.start

    def getNoSerial(self):
        return self.noSerial.get()

    def getStringType(self):
        return self.stringTypeVar.get()

    def getString(self):
        return self.stringEntry.get()

    def getOverride(self):
        return self.overrideVar.get()

    def getPort(self):
        return self.portEntry.get()

    def addBaseInfo(self):
        baseFont = "Verdana"
        titleFont = (baseFont,20,"bold")
        boxNameFont = (baseFont,10,"bold")
        boxValNameFont = (baseFont,10)
        boxValFont = (baseFont,10)
        unitFont = (baseFont,10)
        self.infoFrame = Frame(self.infoRegion)
        self.infoFrame.pack()
        self.titleText = Label(self.infoFrame,text="Information", font=titleFont)
        self.statusText = Label(self.infoFrame,text="Status: ", font=boxNameFont)
        self.statusVal = Label(self.infoFrame,text="idle", font=boxValNameFont)
        self.box1Name = Label(self.infoFrame,text="Box 1: ", font=boxNameFont)
        self.box1V2Name = Label(self.infoFrame,text="V2: ", font=boxValNameFont)
        self.box1V2Val = Label(self.infoFrame,text="N/A", font=boxValFont)
        self.box1V2Unit = Label(self.infoFrame,text="V", font=unitFont)
        self.box2Name = Label(self.infoFrame,text="Box 2: ", font=boxNameFont)
        self.box2R1Name = Label(self.infoFrame,text="R1: ", font=boxValNameFont)
        self.box2R2Name = Label(self.infoFrame,text="R2: ", font=boxValNameFont)
        self.box2R1Val = Label(self.infoFrame,text="N/A", font=boxValFont)
        self.box2R2Val = Label(self.infoFrame,text="N/A", font=boxValFont)
        self.box2R1Unit = Label(self.infoFrame,text="Ω", font=unitFont)
        self.box2R2Unit = Label(self.infoFrame,text="Ω", font=unitFont)
        self.box3Name = Label(self.infoFrame,text="Box 3: ", font=boxNameFont)
        self.box3R2Name = Label(self.infoFrame,text="R2: ", font=boxValNameFont)
        self.box3R3Name = Label(self.infoFrame,text="R3: ", font=boxValNameFont)
        self.box3R2Val = Label(self.infoFrame,text="N/A", font=boxValFont)
        self.box3R3Val = Label(self.infoFrame,text="N/A", font=boxValFont)
        self.box3R2Unit = Label(self.infoFrame,text="Ω", font=unitFont)
        self.box3R3Unit = Label(self.infoFrame,text="Ω", font=unitFont)
        self.box4Name = Label(self.infoFrame,text="Box 4: ", font=boxNameFont)
        self.box4R1Name = Label(self.infoFrame,text="R1: ", font=boxValNameFont)
        self.box4R3Name = Label(self.infoFrame,text="R3: ", font=boxValNameFont)
        self.box4R1Val = Label(self.infoFrame,text="N/A", font=boxValFont)
        self.box4R3Val = Label(self.infoFrame,text="N/A", font=boxValFont)
        self.box4R1Unit = Label(self.infoFrame,text="Ω", font=unitFont)
        self.box4R3Unit = Label(self.infoFrame,text="Ω", font=unitFont)
        self.box5Name = Label(self.infoFrame,text="Box 5: ", font=boxNameFont)
        self.box5R1Name = Label(self.infoFrame,text="R1: ", font=boxValNameFont)
        self.box5C1Name = Label(self.infoFrame,text="C1: ", font=boxValNameFont)
        self.box5fcName = Label(self.infoFrame,text="fc: ", font=boxValNameFont)
        self.box5R1Val = Label(self.infoFrame,text="N/A", font=boxValFont)
        self.box5C1Val = Label(self.infoFrame,text="N/A", font=boxValFont)
        self.box5fcVal = Label(self.infoFrame,text="N/A", font=boxValFont)
        self.box5R1Unit = Label(self.infoFrame,text="Ω", font=unitFont)
        self.box5C1Unit = Label(self.infoFrame,text="F", font=unitFont)
        self.box5fcUnit = Label(self.infoFrame,text="Hz", font=unitFont)
        self.box6Name = Label(self.infoFrame,text="Box 6: ", font=boxNameFont)
        self.box6R1Name = Label(self.infoFrame,text="R1: ", font=boxValNameFont)
        self.box6C1Name = Label(self.infoFrame,text="C1: ", font=boxValNameFont)
        self.box6fcName = Label(self.infoFrame,text="fc: ", font=boxValNameFont)
        self.box6R1Val = Label(self.infoFrame,text="N/A", font=boxValFont)
        self.box6C1Val = Label(self.infoFrame,text="N/A", font=boxValFont)
        self.box6fcVal = Label(self.infoFrame,text="N/A", font=boxValFont)
        self.box6R1Unit = Label(self.infoFrame,text="Ω", font=unitFont)
        self.box6C1Unit = Label(self.infoFrame,text="F", font=unitFont)
        self.box6fcUnit = Label(self.infoFrame,text="Hz", font=unitFont)
        self.box7Name = Label(self.infoFrame,text="Box 7: ", font=boxNameFont)
        self.box7R1Name = Label(self.infoFrame,text="R1: ", font=boxValNameFont)
        self.box7C1Name = Label(self.infoFrame,text="C1: ", font=boxValNameFont)
        self.box7frName = Label(self.infoFrame,text="fr: ", font=boxValNameFont)
        self.box7R1Val = Label(self.infoFrame,text="N/A", font=boxValFont)
        self.box7C1Val = Label(self.infoFrame,text="N/A", font=boxValFont)
        self.box7frVal = Label(self.infoFrame,text="N/A", font=boxValFont)
        self.box7R1Unit = Label(self.infoFrame,text="Ω", font=unitFont)
        self.box7C1Unit = Label(self.infoFrame,text="F", font=unitFont)
        self.box7frUnit = Label(self.infoFrame,text="Hz", font=unitFont)
        self.directionKey1 = Label(self.infoFrame,text="A=North, B=East,", font=boxValNameFont)
        self.directionKey2 = Label(self.infoFrame,text="C=South, D=West", font=boxValNameFont)

        self.titleText.grid(row=0,column=0,columnspan=4,ipadx=50,ipady=10)
        self.statusText.grid(row=1,column=0,ipady=10)
        self.statusVal.grid(row=1,column=1)
        self.box1Name.grid(row=2,column=0)
        self.box1V2Name.grid(row=2,column=1)
        self.box1V2Val.grid(row=2,column=2)
        self.box1V2Unit.grid(row=2,column=3)
        self.box2Name.grid(row=3,column=0)
        self.box2R1Name.grid(row=3,column=1)
        self.box2R2Name.grid(row=4,column=1)
        self.box2R1Val.grid(row=3,column=2)
        self.box2R2Val.grid(row=4,column=2)
        self.box2R1Unit.grid(row=3,column=3)
        self.box2R2Unit.grid(row=4,column=3)
        self.box3Name.grid(row=5,column=0)
        self.box3R2Name.grid(row=5,column=1)
        self.box3R3Name.grid(row=6,column=1)
        self.box3R2Val.grid(row=5,column=2)
        self.box3R3Val.grid(row=6,column=2)
        self.box3R2Unit.grid(row=5,column=3)
        self.box3R3Unit.grid(row=6,column=3)
        self.box4Name.grid(row=7,column=0)
        self.box4R1Name.grid(row=7,column=1)
        self.box4R3Name.grid(row=8,column=1)
        self.box4R1Val.grid(row=7,column=2)
        self.box4R3Val.grid(row=8,column=2)
        self.box4R1Unit.grid(row=7,column=3)
        self.box4R3Unit.grid(row=8,column=3)
        self.box5Name.grid(row=9,column=0)
        self.box5R1Name.grid(row=9,column=1)
        self.box5C1Name.grid(row=10,column=1)
        self.box5fcName.grid(row=11,column=1)
        self.box5R1Val.grid(row=9,column=2)
        self.box5C1Val.grid(row=10,column=2)
        self.box5fcVal.grid(row=11,column=2)
        self.box5R1Unit.grid(row=9,column=3)
        self.box5C1Unit.grid(row=10,column=3)
        self.box5fcUnit.grid(row=11,column=3)
        self.box6Name.grid(row=12,column=0)
        self.box6R1Name.grid(row=12,column=1)
        self.box6C1Name.grid(row=13,column=1)
        self.box6fcName.grid(row=14,column=1)
        self.box6R1Val.grid(row=12,column=2)
        self.box6C1Val.grid(row=13,column=2)
        self.box6fcVal.grid(row=14,column=2)
        self.box6R1Unit.grid(row=12,column=3)
        self.box6C1Unit.grid(row=13,column=3)
        self.box6fcUnit.grid(row=14,column=3)
        self.box7Name.grid(row=15,column=0)
        self.box7R1Name.grid(row=15,column=1)
        self.box7C1Name.grid(row=16,column=1)
        self.box7frName.grid(row=17,column=1)
        self.box7R1Val.grid(row=15,column=2)
        self.box7C1Val.grid(row=16,column=2)
        self.box7frVal.grid(row=17,column=2)
        self.box7R1Unit.grid(row=15,column=3)
        self.box7C1Unit.grid(row=16,column=3)
        self.box7frUnit.grid(row=17,column=3)
        self.directionKey1.grid(row=18,column=0,columnspan=4,ipady=5)
        self.directionKey2.grid(row=19,column=0,columnspan=4)

    def updateStatus(self,text):
        self.statusVal.config(text=str(text))

    def updateVal(self,box,parameter,value):
        if box == 1:
            self.box1V2Val.config(text=str(value))
        if box == 2:
            if parameter == "R1":
                self.box2R1Val.config(text=str(value))
            elif parameter == "R2":
                self.box2R2Val.config(text=str(value))
        if box == 3:
            if parameter == "R2":
                self.box3R2Val.config(text=str(value))
            elif parameter == "R3":
                self.box3R3Val.config(text=str(value))
        if box == 4:
            if parameter == "R1":
                self.box4R1Val.config(text=str(value))
            elif parameter == "R3":
                self.box4R3Val.config(text=str(value))
        if box == 5:
            if parameter == "R1":
                self.box5R1Val.config(text=str(value))
            elif parameter == "C1":
                self.box5C1Val.config(text=str(value))
            elif parameter == "fc":
                self.box5fcVal.config(text=str(value))
        if box == 6:
            if parameter == "R1":
                self.box6R1Val.config(text=str(value))
            elif parameter == "C1":
                self.box6C1Val.config(text=str(value))
            elif parameter == "fc":
                self.box6fcVal.config(text=str(value))
        if box == 7:
            if parameter == "R1":
                self.box7R1Val.config(text=str(value))
            elif parameter == "C1":
                self.box7C1Val.config(text=str(value))
            elif parameter == "fr":
                self.box7frVal.config(text=str(value))

    def addBlockers(self,blockers):  
        for block in blockers:
            newBlocker = Frame(self.root,bg="sienna",height=self.n*10,
                               width=self.n*10)
            newBlocker.place(x=block[0]*self.n*10+3*self.n*10/2,
                    y=(self.yLen-block[1])*self.n*10+self.n*10/2)

    def addBoxes(self,boxes):
        for box in boxes:
            displayDir = '>'
            boxCol = "yellow"
            knobCol = "black"
            if box.direction == 'A':
                displayDir = '^'
                C = Canvas(self.root,bd=0,bg=boxCol,height=40,
                       width=50)
                C.place(x=box.xPos*self.n*10+3*self.n*10/2,
                        y=(self.yLen-box.yPos)*self.n*10+9*self.n*10/16)
                K = Canvas(self.root,bd=0,bg=knobCol,height=5,
                        width=10)
                K.place(x=box.xPos*self.n*10+4*self.n*10/2,
                        y=(self.yLen-box.yPos)*self.n*10+0.5*self.n*10, anchor="center")
            elif box.direction == 'B':
                displayDir = '>'
                C = Canvas(self.root,bd=0,bg=boxCol,height=50,
                       width=40)
                C.place(x=box.xPos*self.n*10+25*self.n*10/16,
                        y=(self.yLen-box.yPos)*self.n*10+self.n*10/2)
                K = Canvas(self.root,bd=0,bg=knobCol,height=10,
                        width=5)
                K.place(x=box.xPos*self.n*10+5*self.n*10/2,
                        y=(self.yLen-box.yPos)*self.n*10+self.n*10, anchor="center")
            elif box.direction == 'C':
                displayDir = 'v'
                C = Canvas(self.root,bd=0,bg=boxCol,height=40,
                       width=50)
                C.place(x=box.xPos*self.n*10+3*self.n*10/2,
                        y=(self.yLen-box.yPos)*self.n*10+9*self.n*10/16)
                K = Canvas(self.root,bd=0,bg=knobCol,height=5,
                        width=10)
                K.place(x=box.xPos*self.n*10+4*self.n*10/2,
                        y=(self.yLen-box.yPos)*self.n*10+1.5*self.n*10, anchor="center")
            elif box.direction == 'D':
                displayDir = '<'
                C = Canvas(self.root,bd=0,bg=boxCol,height=50,
                       width=40)
                C.place(x=box.xPos*self.n*10+25*self.n*10/16,
                        y=(self.yLen-box.yPos)*self.n*10+self.n*10/2)
                K = Canvas(self.root,bd=0,bg=knobCol,height=10,
                        width=5)
                K.place(x=box.xPos*self.n*10+3*self.n*10/2,
                        y=(self.yLen-box.yPos)*self.n*10+self.n*10, anchor="center")
            boxText = str(box.num)+box.direction
            C.create_text(25,10,text=boxText)


    def displayRoute(self,path):
        if path != 0:
            for cell in path:
                if cell[2] != 'b':
                    C = Canvas(self.root,bd=0,bg="blue",height=10,
                        width=10)
                    C.place(x=cell[0]*self.n*10+4*self.n*10/2,
                        y=(self.yLen-cell[1])*self.n*10+self.n*10, anchor="center")
        else:
            messagebox.showerror("Error","No route found")

    def displayBuggy(self,x,y,direction,col="purple"):
        B = Canvas(self.root,bd=0,height=20,width=20)
        B.place(x=x*self.n*10+4*self.n*10/2,
                    y=(self.yLen-y)*self.n*10+self.n*10, anchor="center")
        if direction == 'S':
            B.create_polygon(1,0,20,0,10,20,fill=col)
        elif direction == 'N':
            B.create_polygon(1,20,20,20,10,0,fill=col)
        elif direction == 'E':
            B.create_polygon(1,0,1,20,20,10,fill=col)
        elif direction == 'W':
            B.create_polygon(20,0,20,20,0,10,fill=col)

    def overwriteBuggy(self,x,y):
        B = Canvas(self.root,bd=0,height=20,width=20)
        B.place(x=x*self.n*10+4*self.n*10/2,
                    y=(self.yLen-y)*self.n*10+self.n*10, anchor="center")

    def updateBoxDot(self,xPos,yPos):
        C = Canvas(self.root,bd=0,bg="sienna",height=10,
                        width=10)
        C.place(x=xPos*self.n*10+4*self.n*10/2,
                        y=(self.yLen-yPos)*self.n*10+self.n*10, anchor="center")
        
    def updateBuggy(self,instr):
        if instr == '1' or instr == '2' or instr == '3' or instr == '4' or instr == '5' or instr == '6' or instr == '7' or instr == 'A' or instr == 'B' or instr == 'C' or instr == 'D':
            pass
        else:
            self.overwriteBuggy(self.curXPos,self.curYPos)
            if instr == 'F':
                if self.curDir == 'N':
                    self.curYPos = self.curYPos+1
                elif self.curDir == 'S':
                    self.curYPos = self.curYPos-1
                elif self.curDir == 'E':
                    self.curXPos = self.curXPos+1
                elif self.curDir == 'W':
                    self.curXPos = self.curXPos-1
                self.displayBuggy(self.curXPos,self.curYPos,self.curDir)
            if instr == 'L':
                if self.curDir == 'N':
                    self.curDir = 'W'
                elif self.curDir == 'S':
                    self.curDir = 'E'
                elif self.curDir == 'E':
                    self.curDir = 'N'
                elif self.curDir == 'W':
                    self.curDir = 'S'
                self.displayBuggy(self.curXPos,self.curYPos,self.curDir)
            if instr == 'R':
                if self.curDir == 'N':
                    self.curDir = 'E'
                elif self.curDir == 'S':
                    self.curDir = 'W'
                elif self.curDir == 'E':
                    self.curDir = 'S'
                elif self.curDir == 'W':
                    self.curDir = 'N'
                self.displayBuggy(self.curXPos,self.curYPos,self.curDir)
            if instr == 'Q':
                if self.curDir == 'N':
                    self.curDir = 'S'
                elif self.curDir == 'S':
                    self.curDir = 'N'
                elif self.curDir == 'E':
                    self.curDir = 'W'
                elif self.curDir == 'W':
                    self.curDir = 'E'
                self.displayBuggy(self.curXPos,self.curYPos,self.curDir)
            if instr == 'S':
                self.displayBuggy(self.curXPos,self.curYPos,self.curDir,"green")

    def createGUI(self):
        #Displaying the window
        self.root.mainloop()


##newGUI = GUI(14,10)
##newGUI.createLayout()
##blockers = [(-1,1),(0,1),(1,1),(2,1)]
##newGUI.addBlockers(blockers)
##targets = [target(5,5,'A'),target(7,7,'B')]
##newGUI.addBoxes(targets)
##newGUI.createGUI()



