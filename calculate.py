class calculate:
    def __init__(self):
        self.e24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
        self.e12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
        self.Rk = 976
        self.pi = 3.1415926536897

    def calcValues(self,boxNum,direction,array):
        for i in range(len(array)):
            array[i]=float(array[i])
        if boxNum == 1:
            V2 = array[0]*(8.66/4.11)
            return ['V1',V2]
        elif boxNum == 2:
            R1 = (self.Rk*array[0])/(5-array[0])
            R2 = (self.Rk*array[1])/(5-array[1])
            R1e24 = self.getE24Val(R1)
            R2e24 = self.getE24Val(R2)
            return ['R1',R1e24,'R2',R2e24]
        elif boxNum == 3:
            if direction == 'f':
                R2 = (self.Rk*array[0])/(array[1]-array[0])
                R3 = array[2]*R2/(array[3]-array[2])
            elif direction == 'b':
                R2 = self.Rk*(array[0]-array[1])/array[1]
                R3 = R2*(array[3]-array[2])/array[2]
            R2e24 = self.getE24Val(R2)
            R3e24 = self.getE24Val(R3)
            return ['R2',R2e24,'R3',R3e24]
        elif boxNum == 4:
            R1 = array[0] * (self.Rk + 1200) / (5-array[0])
            R3 = array[1] * (self.Rk + 1200) / (5-array[1])
            R1e24 = self.getE24Val(R1)
            R3e24 = self.getE24Val(R3)
            return ['R1',R1e24,'R3',R3e24]
        elif boxNum == 5:
            R1 = array[0] * self.Rk / (5-array[0])
            C1 = array[1]
            R1e24 = self.getE24Val(R1)
            C1e12 = self.getE12Val(C1)
            fc = 1/(2*self.pi*R1e24*C1e12)
            return ['R1',R1e24,'C1',C1e12,'fc',fc]
        elif boxNum == 6:
            R1 = array[0] * self.Rk / (5-array[0])
            C1 = array[1]
            R1e24 = self.getE24Val(R1)
            C1e12 = self.getE12Val(C1)
            fc = 1/(2*self.pi*R1e24*C1e12)
            return ['R1',R1e24,'C1',C1e12,'fc',fc]
        elif boxNum == 7:
            R1 = array[0] * self.Rk / (5-array[0])
            C1 = array[1]
            R1e24 = self.getE24Val(R1)
            C1e12 = self.getE12Val(C1)
            fr = 1/(2*self.pi*R1e24*C1e12)
            return ['R1',R1e24,'C1',C1e12,'fr',fr]

        
    def getE24Val(self,val):
        print(val)
        strVal = str(val).split('.')[0]
        valPower = len(strVal)-1
        e24Val = self.searchE24(val,valPower)
        if str(e24Val)[:2] == "91" or str(e24Val)[:2] == "9.1":
            curDif = abs(val-9.1*(10**valPower))
            newDif = abs(val-10*(10**valPower))
            if newDif < curDif:
                e24Val = int(10*(10**valPower))
        print(e24Val)
        return e24Val

    def getE12Val(self,val):
        strVal = str(val).split('.')[0]
        valPower = len(strVal)-1
        e12Val = self.searchE12(val,valPower)
        if str(e12Val)[:2] == "91" or str(e12Val)[:2] == "9.1":
            curDif = abs(val-9.1*(10**valPower))
            newDif = abs(val-10*(10**valPower))
            if newDif < curDif:
                e12Val = int(10*(10**valPower))
        print(e12Val)
        return e12Val

    def searchE24(self,newVal,power):
        curDif = 10*100
        bestDif = 10*100
        bestVal = 1.0
        for val in self.e24:
            powVal = val*(10**power)
            curDif = abs(powVal-newVal)
            if curDif < bestDif:
                bestDif = curDif
                bestVal = powVal
        return bestVal

    def searchE12(self,newVal,power):
        curDif = 10*100
        bestDif = 10*100
        bestVal = 1.0
        for val in self.e12:
            powVal = val*(10**power)
            curDif = abs(powVal-newVal)
            if curDif < bestDif:
                bestDif = curDif
                bestVal = powVal
        return bestVal


#newCalc = calculate()


