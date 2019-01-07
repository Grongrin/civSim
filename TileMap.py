import Tile


class TileMap:
    def __init__(self, XSize,YSize):
        self.xSize_ = XSize
        self.ySize_ = YSize
        self.map_ = []
        for i in range(self.xSize_):
            self.map_.append([])
            for j in range(self.ySize_):
                newTile = Tile.Tile(i, j)
                self.map_[i].append(newTile)
        for i in range(self.xSize_):
            for j in range(self.ySize_):
                self.setNeighbours(self.getTile(i, j))

    def getTile(self, x, y):
        return self.map_[x][y]

    def setNeighbours(self, tile):
        x = tile.getX()
        y = tile.getY()
        neighbours = []
        if y % 2 == 0:
            if x > 0:
                neighbours.append(self.getTile(x - 1, y))
                if y > 0: neighbours.append(self.getTile(x - 1, y - 1))
                if y < self.ySize_ - 1: neighbours.append(self.getTile(x - 1, y + 1))
            if x < self.xSize_ - 1: neighbours.append(self.getTile(x + 1, y))
            if y > 0: neighbours.append(self.getTile(x, y - 1))
            if y < self.ySize_ - 1: neighbours.append(self.getTile(x, y + 1))
        else:
            if x > 0: neighbours.append(self.getTile(x - 1, y))
            if y > 0: neighbours.append(self.getTile(x, y - 1))
            if y < self.ySize_ - 1: neighbours.append(self.getTile(x, y + 1))
            if x < self.xSize_ - 1:
                neighbours.append(self.getTile(x + 1, y))
                if y > 0: neighbours.append(self.getTile(x + 1, y - 1))
                if y < self.ySize_ - 1: neighbours.append(self.getTile(x + 1, y + 1))

        tile.setNeighbours(neighbours)

    def getNeighboursByCoords(self, x, y):
        return self.getTile(x, y).getNeighbours()

    def getNeighbours(self, tile):
        return tile.getNeighbours()

    def getMap(self):
        return self.map_

    def getXSize(self):
        return self.xSize_

    def getYSize(self):
        return self.ySize_
