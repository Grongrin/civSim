import Tile
import TileMap
import math


class Civilization:
    def __init__(self, id=-1):
        self.id_ = id
        self.territory_ = []
        self.neighbouringTiles_ = []
        self.population_ = 100
        self.laborers_ = 50
        self.soldiers_ = 50
        self.maxTerritory_ = 1
        self.soldiersNeededToExpand = 0
        self.currTerritory_ = 0
        self.territoryAgrValue_ = 0
        self.agrOutput_ = 0
        self.lastMoveBenefit_ = 0
        self.willExpand_ = True
        self.territoryCenter_ = []

    def getId(self):
        return self.id_

    def getDistance(self, coords1, coords2):
        return math.sqrt((coords1[0] - coords2[0]) ** 2 + (coords1[1] - coords2[1]) ** 2)

    def rate(self, tile):
        value = 0.
        value += tile.getAgrVal()
        value -= (self.getDistance(tile.getCoords(), self.territoryCenter_) / self.getDistance(self.territoryCenter_, [self.territoryCenter_[0], (self.territoryCenter_[1]+(math.sqrt(self.currTerritory_/math.pi)))]))
        # for n in tile.getNeighbours():
        #    if n in self.territory_:
        #        value += 0.5
        return value

    def setStartingTile(self, tile):
        if tile.getCiv():
            tile.getCiv().looseTerritory(tile)
        tile.setCiv(self)
        self.territory_.append(tile)
        for n in tile.getNeighbours():
            self.neighbouringTiles_.append(n)
        self.currTerritory_ += 1
        self.territoryAgrValue_ += tile.getAgrVal()
        self.territoryCenter_ = [float(tile.getX()), float(tile.getY())]

    def takeoverTerritory(self, tile):
        print("Taking over territory")
        if tile.getCiv() is not None:
            if tile.getCiv() == self:
                print("Error: Trying to takeover own tile!")
            tile.getCiv().looseTerritory(tile)
        tile.setCiv(self)
        self.territory_.append(tile)
        self.neighbouringTiles_.remove(tile)
        for n in tile.getNeighbours():
            if n not in self.neighbouringTiles_ and n not in self.territory_:
                self.neighbouringTiles_.append(n)
        self.currTerritory_ += 1
        self.territoryAgrValue_ += tile.getAgrVal()
        self.territoryCenter_[0] = (self.territoryCenter_[0] * (self.currTerritory_ - 1) + tile.getX()) / self.currTerritory_
        self.territoryCenter_[1] = (self.territoryCenter_[1] * (self.currTerritory_ - 1) + tile.getY()) / self.currTerritory_

    def looseTerritory(self, tile):
        self.territory_.remove(tile)
        tile.setCiv(None)
        self.territoryAgrValue_ -= tile.getAgrVal()
        for n in tile.getNeighbours():
            d = True
            for n2 in n.getNeighbours():
                if n2 in self.territory_:
                    d = False
                    break
            if d:
                self.neighbouringTiles_.remove(n)

    def balancePop(self):
        self.population_ = self.laborers_+self.soldiers_

    def getOutputs(self, laborers, agrValue):
        if laborers < 1:
            return 0
            print("ERROR: liczba robotników ujemna!")
        return math.sqrt(laborers * agrValue)

    def getMaxTerritory(self, soldiers):
        a = 0.5
        return int(a*math.pi*(soldiers**(4./5)))

    def calcSoldiersToExpand(self):
        need = 0
        while self.getMaxTerritory(self.soldiers_+need) <= self.currTerritory_:
            need += 1
        return need

    def calcRedundandSoldiers(self):
        redundant = 1
        while self.getMaxTerritory(self.soldiers_-redundant) >= self.currTerritory_:
            redundant += 1
        return redundant-1

    def reproduce(self):
        self.laborers_ += int(0.01 * self.population_)

    def makeMove(self):
        expanded = False
        # self.maxTerritory_ = self.getMaxTerritory(self.soldiers_)
        bestTile = self.neighbouringTiles_[0]
        for n in self.neighbouringTiles_:
            if self.rate(n) > self.rate(bestTile):
                bestTile = n
        soldiersToExpand = self.calcSoldiersToExpand()
        redundantSoldiers = self.calcRedundandSoldiers()

        if self.laborers_ >= soldiersToExpand and \
                self.getOutputs(self.laborers_-soldiersToExpand, self.territoryAgrValue_+bestTile.getAgrVal()) > \
                self.getOutputs(self.laborers_+redundantSoldiers, self.territoryAgrValue_):
            self.willExpand_ = True
        else:
            self.willExpand_ = False

        if self.willExpand_:
            self.soldiers_ += soldiersToExpand
            self.laborers_ -= soldiersToExpand
            self.maxTerritory_ = self.getMaxTerritory(self.soldiers_)
            if self.maxTerritory_ > self.currTerritory_:
                self.takeoverTerritory(bestTile)
                expanded = True
        else:
                self.laborers_ += redundantSoldiers
                self.soldiers_ -= redundantSoldiers
                self.maxTerritory_ = self.getMaxTerritory(self.soldiers_)
        oldArgOutput = self.agrOutput_
        self.agrOutput_ = self.getOutputs(self.laborers_, self.territoryAgrValue_)
        self.lastMoveBenefit_ = self.agrOutput_ - oldArgOutput
        self.reproduce()
        self.balancePop()
        print("Move made")
        print(self.territory_)
        print("Current population:", self.population_)
        print("Soldiers: ", self.soldiers_)
        print("Current predicted expansion profit: ", (self.getOutputs(self.laborers_ - soldiersToExpand, self.territoryAgrValue_ + bestTile.getAgrVal()) -
              self.getOutputs(self.laborers_ + redundantSoldiers, self.territoryAgrValue_)))
        print("Max territory: ", self.maxTerritory_)
        print("Current territory: ", self.currTerritory_)
        print("Best tile :", bestTile)
        print("Robotnicy: ", self.laborers_)
        print("AgrVal: ", self.territoryAgrValue_)
        if expanded:
            return bestTile
        else:
            return None



