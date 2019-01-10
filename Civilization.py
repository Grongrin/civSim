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
        self.growth_ = 0
        self.technologyLevel_ = 1
        self.tresury_ = 0
        self.taxrate_ = 0
        self.income_ = 0

    def getId(self):
        return self.id_

    def getDistance(self, coords1, coords2):
        return math.sqrt((coords1[0] - coords2[0]) ** 2 + (coords1[1] - coords2[1]) ** 2)

    def rate(self, tile):
        value = 0.
        value += tile.getAgrVal()*10
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
            if n.getType() == 1:
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
            if n.getType() == 1 and n not in self.neighbouringTiles_ and n not in self.territory_:
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
        a = 0.2
        r = soldiers**(2./10)
        return int(a * math.pi * r**2)

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

    def calcArmyWages(self):
        return math.sqrt(self.territoryAgrValue_ / self.laborers_)/2

    def calcTax(self):
        return self.agrOutput_*self.taxrate_

    def calcMinTaxRate(self):
        rate = 0.1
        while self.agrOutput_*rate < self.calcArmyWages()*self.soldiers_:
            rate += 0.01
        return rate

    def reproduce(self):
        growthRate = 0.05 * self.agrOutput_/self.population_
        self.growth_ += growthRate * self.population_
        if self.growth_ >= 1:
            self.laborers_ += int(self.growth_)
            self.growth_ -= int(self.growth_)

    def makeMove(self):
        expanded = False
        self.reproduce()
        self.balancePop()
        # self.maxTerritory_ = self.getMaxTerritory(self.soldiers_)

        newTiles = []
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

        while self.willExpand_:
            self.soldiers_ += soldiersToExpand
            self.laborers_ -= soldiersToExpand
            self.maxTerritory_ = self.getMaxTerritory(self.soldiers_)
            if self.maxTerritory_ > self.currTerritory_:
                self.takeoverTerritory(bestTile)
                newTiles.append(bestTile)
                expanded = True

            bestTile = self.neighbouringTiles_[0]
            for n in self.neighbouringTiles_:
                if self.rate(n) > self.rate(bestTile):
                    bestTile = n

            soldiersToExpand = self.calcSoldiersToExpand()
            redundantSoldiers = self.calcRedundandSoldiers()

            if self.laborers_ >= soldiersToExpand and \
                    self.getOutputs(self.laborers_ - soldiersToExpand, self.territoryAgrValue_ + bestTile.getAgrVal()) > \
                    self.getOutputs(self.laborers_ + redundantSoldiers, self.territoryAgrValue_):
                self.willExpand_ = True
            else:
                self.willExpand_ = False

        self.laborers_ += redundantSoldiers
        self.soldiers_ -= redundantSoldiers
        self.maxTerritory_ = self.getMaxTerritory(self.soldiers_)

        oldArgOutput = self.agrOutput_
        self.agrOutput_ = self.getOutputs(self.laborers_, self.territoryAgrValue_)
        self.lastMoveBenefit_ = self.agrOutput_ - oldArgOutput
        tresuryBefore = self.tresury_
        self.taxrate_ = self.calcMinTaxRate()
        self.tresury_ += self.calcTax()
        self.tresury_ -= self.calcArmyWages()*self.soldiers_
        self.income_ = tresuryBefore - self.tresury_
        #if self.income_ < 0:
        #    self.taxrate_ = self.calcMinTaxRate()

        print("Move made")
        print("Obecna populacja: ", self.population_, " Żołnierze: ", self.soldiers_, " Robotnicy: ", self.laborers_)
        print("AgrVal: ", self.territoryAgrValue_)
        print("Produkcja : ", self.agrOutput_, " Produkcja po odjęciu  kosztu armii: ", self.agrOutput_ - self.calcArmyWages()*self.soldiers_)
        print("Pozostała produkcja na robotnika: ", (self.agrOutput_ - self.calcArmyWages()*self.soldiers_)/self.laborers_)
        print("Żołnierze do rozwoju : ", soldiersToExpand, " Żołnierze zbędni : ", redundantSoldiers)
        print("Army wages per soldier: ", self.calcArmyWages())
        print("Laborers, agrValue", self.laborers_, self.territoryAgrValue_)
        print("Predicted expansion profit after move: ",
              (self.getOutputs(self.laborers_ - soldiersToExpand, self.territoryAgrValue_ + bestTile.getAgrVal()) -
               self.getOutputs(self.laborers_ + redundantSoldiers, self.territoryAgrValue_)))
        print("Max territory: ", self.maxTerritory_, " Current territory: ", self.currTerritory_)
        print("Tresury: ", self.tresury_)
        print("Tax rate: ", self.taxrate_)
        # print("Best tile :", bestTile)

        if expanded:
            return newTiles
        else:
            return None



