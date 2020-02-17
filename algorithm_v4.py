from decipher_v2 import *

class cell:
    def __init__(self,x,y,blocked):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None
        self.blocked = blocked


class routeFind:
    def __init__(self):
        self.openList = []
        self.closedList = []
        self.cells = []
        self.gridWidth = None
        self.gridHeight = None
        

    def createGrid(self,width,height,walls,start,end):
        self.gridWidth = width
        self.gridHeight = height
        for x in range(self.gridWidth):
            for y in range(self.gridHeight):
                if (x,y) in walls:
                    blocked = True
                else:
                     blocked = False
                self.cells.append(cell(x,y,blocked))
        self.start = self.getCell(*start)
        self.end = self.getCell(*end)


    def calcG(self,cell):
        return abs(cell.x - self.end.x) + abs(cell.y - self.end.y)

    def getCell(self,x,y):
        return self.cells[x * self.gridHeight + y]

    def adjCells(self,cell):
        adj_cells = []
        if cell.x < self.gridWidth-1:
            adj_cells.append(self.getCell(cell.x+1,cell.y))
        if cell.y < self.gridHeight-1:
            adj_cells.append(self.getCell(cell.x,cell.y+1))
        if cell.x > 0:
            adj_cells.append(self.getCell(cell.x-1,cell.y))
        if cell.y > 0:
            adj_cells.append(self.getCell(cell.x,cell.y-1))
        return adj_cells

    def findPath(self):
        curCell = self.end
        path = [(curCell.x,curCell.y)]
        while curCell.parent is not self.start:
            curCell = curCell.parent
            try:
                path.append((curCell.x,curCell.y))
            except:
                print(path)
        path.reverse()
        return path

    def updateCell(self,adj,cell):
        adj.g = cell.g + 10
        adj.g = self.calcG(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def smallestF(self):
        smallest = self.openList[0]
        for cell in self.openList:
            if cell.f <= smallest.f:
                smallest = cell
        return smallest

    def algorithm(self):
        #Add starting cell to open list
        self.openList.append(self.start)
        while(len(self.openList)!=0):
            #Retrieve cell in open list with smallest F, most recently added
            curCell = self.smallestF()
            self.openList.remove(curCell)
            self.closedList.append(curCell)
            if curCell is self.end:
                return self.findPath()
            adjCells = self.adjCells(curCell)
            #Remove any unreachable cells from adj list
            for adjCell in adjCells:
                if (adjCell.blocked == False) and (adjCell not in self.closedList):
                    if (adjCell in self.openList) and adjCell.g > (curCell.g + 1):
                            self.updateCell(adjCell,curCell)
                    else:
                        self.updateCell(adjCell,curCell)
                        self.openList.append(adjCell)
        return 0
        
