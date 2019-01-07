class Tile:
    def __init__(self, x, y, civ="Neutral", type=1, agrVal=1):
        self.x_ = x
        self.y_ = y
        self.Civ_ = civ
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
