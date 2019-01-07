import Tile
import TileMap
import math


class Civilization:
    def __init__(self, id, map):
        self.id_ = id
        self.map_ = map
        self.territory_ = []
        self.neighbouringTiles_ = []
        self.population_ = 100
        self.laborers_ = 50
        self.soldiers_ = 50
        self.maxTerritory_ = 1
        self.currTerritory_ = 0
        self.territoryAgrValue = 0
        self.agrOutput_ = 0

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
        self.agrOutput_ = self.laborers_*self.territoryAgrValue
