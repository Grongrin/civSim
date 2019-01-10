import TileMap as tm
import Civilization
from tkinter import *
import math

class Tile:
    def __init__(self,x,y,a,cords,index):
        self.x_ = x
        self.y_= y
        self.a_ = a
        self.cords_ = cords
        self.index_=index


class View(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.hexagons = []
        self.civs_ = []
        self.biggestTileX=0
        self.biggestTileY=0
        self.infoId=0
        self.canvas = Canvas(width=1400, height=900,bg="#AFEEEE" )
        self.canvas.pack()
        self.canvas.bind("<Motion>", self.getTileByXY)
        self.canvas.create_text(1100,10,text="Tile info:")
        self.a_ = 0

    def addCiv(self, civ):
        self.civs_.append(civ)

    def drawMap(self,map):
        xSize = map.getXSize()
        ySize = map.getYSize()
        if ySize %2 ==0:
            yHeight = ySize*1.5
        else:
            yHeight = math.ceil(ySize/2)*2+ySize//2
        xHeight = (2*xSize+1)*math.sqrt(3)/2
        print(yHeight, xHeight)
        if yHeight>xHeight:
            self.a_=1100/yHeight*0.9
        else:
            self.a_=900/xHeight*0.9

        #allTiles=map.getMap()
        for i in range(xSize):
            for j in range(ySize):
                self.drawTile(map.getTile(i, j), self.a_)

    def fromRGB(self, R, G, B): # tłumaczenie koloru RGB na kolor dla tkinter
        return "#%02x%02x%02x" % (R, G, B)

    def drawTile(self,tile,a):
        if tile is None:
            return
        colors = [
            "#FFFF66",
            "#3366FF",
            "#e63813",
            "#091e4a",
            "#0d98a8",
            "#720da8"
        ]
        tileCoords = tile.getCoords()
        if tileCoords[1] % 2 == 0:
            startX = 1.5*a + a * math.sqrt(3) * tileCoords[0]
        else:
            startX = 1.5*a + a * math.sqrt(3) / 2 + a * math.sqrt(3) * tileCoords[0]
        startY = 1.5*a + 1 / 2 * a + 1.5 * tileCoords[1] * a
        angle = 60
        coords = []
        for i in range(1, 7):
            coords.append([startX, startY])
            endX = startX + a * math.sin(math.radians(angle * i))
            endY = startY + a * math.cos(math.radians(angle * i))
            startX = endX
            startY = endY
        if tile.getCiv() is not None:
            id = tile.getCivId()
            color = colors[id+2]
        else:
            if tile.getType() == 1:
                #color = colors[0]
                color = self.fromRGB(int(tile.getAgrVal()*255), int(tile.getAgrVal()*255), int(tile.getAgrVal()*255))
            else:
                color = colors[1]

        index = self.canvas.create_polygon(coords[0][0],
                                   coords[0][1],
                                   coords[1][0],
                                   coords[1][1],
                                   coords[2][0],
                                   coords[2][1],
                                   coords[3][0],
                                   coords[3][1],
                                   coords[4][0],
                                   coords[4][1],
                                   coords[5][0],
                                   coords[5][1],
                                   fill=color,
                                   outline="gray",
                                   )

        for i in coords:
            if i[0]>self.biggestTileX:
                self.biggestTileX = i[0]
            if i[1]>self.biggestTileY:
                self.biggestTileY=i[1]
        print("(",tile.getX(), ", ", tile.getY(),", ",index, ")", sep='')

        hex = Tile(tile.getX(),tile.getY(),a,coords,index)
        self.hexagons.append(hex)


    def showTileDetails(self,tile):
        self.canvas.delete(self.infoId)
        onscreen = "("+str(tile.x_)+","+str(tile.y_)+")"
        self.infoId=self.canvas.create_text(1100,20,text=onscreen)
        print("(", tile.x_, ", ", tile.y_, ")", sep='')


    def findNearestTile(self,nearest):
        for i in self.hexagons:
            if i.index_ == nearest:
                return i
        return None

    def getTileByXY(self, event):
        for c in self.civs_:
            changedTiles = c.makeMove()
            if changedTiles is not None:
                for t in changedTiles:
                    self.drawTile(t, self.a_)
        print(event.x, event.y)
        if (event.x<self.biggestTileX and event.y<self.biggestTileY):
            nearest = int(self.canvas.find_closest(event.x,event.y)[0])
            print(nearest)
            tile = self.findNearestTile(nearest)
            if tile:
                self.showTileDetails(tile)


if __name__ =='__main__':
    view = View()
    map = tm.TileMap(100,170)
    m = map.getMap()
    for i in m:
        for j in i:
            j.printCoords()
    view.drawMap(map)
    print(len(view.hexagons))
    view.mainloop()







