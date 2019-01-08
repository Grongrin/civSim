class Tile:
    def __init__(self, x, y, civ=None, type=1, agrVal=1):
        self.x_ = x
        self.y_ = y
        self.civ_ = civ
        if self.civ_ is not None:
            self.civId_ = self.civ_.getId
        else:
            self.civId_ = -1
        self.type_ = type
        self.neighbours_ = None
        self.agrVal_ = agrVal

    def getCoords(self):
        return (self.x_, self.y_)

    def getX(self):
        return self.x_

    def getY(self):
        return self.y_

    def printCoords(self):
        print("(", self.x_, ", ", self.y_, ")", sep='')

    def getType(self):
        return self.type_

    def setType(self, t):
        self.type_ = t

    def getNeighbours(self):
        return self.neighbours_

    def setNeighbours(self, neighbours):
        self.neighbours_ = neighbours

    def getAgrVal(self):
        return self.agrVal_

    def setCiv(self, civ):
        self.civ_ = civ
        if civ is not None:
            self.civId_ = civ.getId()
        else:
            self.civId_ = -1

    def getCiv(self):
        return self.civ_

    def getCivId(self):
        return self.civId_
