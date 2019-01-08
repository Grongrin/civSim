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
        self.currTerritory_ = 0
        self.territoryAgrValue_ = 0
        self.agrOutput_ = 0
        self.lastMoveBenefit_ = 0
        self.willExpand_ = True

    def getId(self):
        return self.id_

    def rate(self, tile):
        value = 0.
        value += tile.getAgrVal()
        for n in tile.getNeighbours():
            if n in self.territory_:
                value += 0.5
        return value

    def setStartingTile(self, tile):
        if tile.getCiv():
            tile.getCiv().looseTerritory(tile)
        tile.setCiv(self)
        self.territory_.append(tile)
        for n in tile.getNeighbours():
            self.neighbouringTiles_.append(n)
        self.currTerritory_ += 1
        self.agrOutput_ += tile.getAgrVal()

    def takeoverTerritory(self, tile):
        if tile.getCiv():
            tile.getCiv().looseTerritory(tile)
        tile.setCiv(self)
        self.territory_.append(tile)
        self.neighbouringTiles_.remove(tile)
        for n in tile.getNeighbours():
            if n not in self.neighbouringTiles_:
                self.neighbouringTiles_.append(n)
        self.currTerritory_ += 1
        self.agrOutput_ += tile.getAgrVal()

    def looseTerritory(self, tile):
        self.territory_.remove(tile)
        tile.setCiv(None)
        self.agrOutput_ -= tile.getAgrVal()
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

    def getOutputs(self):
        self.agrOutput_ = math.sqrt(self.laborers_ * self.territoryAgrValue_)

    def getMaxTerritory(self, soldiers):
        a = 1.
        return int(a*math.pi*(soldiers**(2./3)))

    def reproduce(self):
        self.laborers_ += int(0.02 * self.population_)

    def makeMove(self):
        expanded = False
        self.maxTerritory_ = self.getMaxTerritory(self.soldiers_)
        bestTile = self.neighbouringTiles_[0]
        for n in self.neighbouringTiles_:
            if self.rate(n) > self.rate(bestTile):
                bestTile = n
        if self.lastMoveBenefit_ < 0:
            self.willExpand_ = not self.willExpand_
        if self.willExpand_:
            if self.maxTerritory_ > self.currTerritory_:
                self.takeoverTerritory(bestTile)
                expanded = True
            else:
                self.soldiers_ += 1
                self.laborers_ -= 1
        else:
            if self.getMaxTerritory(self.soldiers_-1) >= self.currTerritory_:
                self.laborers_ += 1
                self.soldiers_ -= 1
        oldArgOutput = self.agrOutput_
        self.getOutputs()
        self.lastMoveBenefit_ = self.agrOutput_ - oldArgOutput
        self.reproduce()
        self.balancePop()
        print("Move made")
        print(self.territory_)
        if(expanded):
            return bestTile
        else:
            return None



