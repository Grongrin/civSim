import math
import random


class Tile:
    def __init__(self, x, y, civ=None, type=1, agrVal=0):
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
        self.height_ = 0
        self.randomized_ = False

    def getCoords(self):
        return [self.x_, self.y_]

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

    def isRandomized(self):
        return self.randomized_

    def getHeight(self):
        return self.height_

    def setAgrVal(self, val):
        self.agrVal_ = val

    def randomizeTerrain(self):
        random.seed()

        gen = random.randrange(-8, 26)  # generacja typu
        for n in self.neighbours_:
            if n.isRandomized():
                gen += n.getType()
        self.type_ = gen
        if gen < 0:
            self.height_ = -1
        if self.type_ < -14:
            self.type_ = -14
        if self.type_ > 3:
            self.type_ = 3

        gen = random.normalvariate(400, 800)    # generacja wysokości
        while gen < 0:
            gen = random.normalvariate(2000, 8000)
        self.height_ = gen


        gen = random.random()   # generacja żyzności gleby (0 - 1)
        self.agrVal_ = gen

        a = 0
        surroundingHeight = 0
        surroundingFertility = 0
        for n in self.neighbours_:  # uśrednianie wygenerowanych wartości z otoczeniem
            if n.isRandomized() and n.getType() > 0:
                surroundingHeight += n.getHeight()
                surroundingFertility += n.getAgrVal()
                a += 1
            if a > 0:
                self.height_ = (self.height_ + (surroundingHeight / a)) / 2
                if random.random() > 0.4:
                    self.agrVal_ = (self.agrVal_ + (surroundingFertility / a)) / 2
        if self.agrVal_ < 0.6 and random.random()<0.1:
            self.agrVal_ += 0.05

        self.randomized_ = True

