import TileMap as tm
from tkinter import *
import math


class View(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.canvas = Canvas(width=1400, height=900,bg="#AFEEEE" )
        self.canvas.pack()
        self.canvas.bind("<Motion>", self.getTileByXY)



    def drawMap(self,map):
        xSize = map.getXSize()
        ySize = map.getYSize()
        if ySize %2 ==0:
            yHeight = ySize*1.5
        else:
            yHeight = math.ceil(ySize/2)*2+ySize//2


        xHeight = (2*xSize+1)*math.sqrt(3)/2
        print(yHeight, xHeight)
        a=20
        allTiles=map.getMap()

        for i in range(xSize):
            for j in range(ySize):
                self.drawTile(allTiles[i][j],a)

    def drawTile(self, tile, a):
        tileCoords = tile.getCoords()
        if tileCoords[1] % 2==0:
            startX= 20 + a * math.sqrt(3) * tileCoords[0]
        else:
            startX = 20 + a * math.sqrt(3) / 2 + a * math.sqrt(3) * tileCoords[0]
        startY = 30 + 1 / 2 * a + 1.5 * tileCoords[1] * a
        angle = 60
        coords = []
        for i in range(1,7):
            coords.append([startX, startY])
            endX = startX +  a * math.sin(math.radians(angle * i))
            endY = startY +a * math.cos(math.radians(angle * i))
            startX = endX
            startY = endY
        if tile.getType() == 1:
            color = "#FFFF66"
        else:
            color = "#3366FF"
        self.canvas.create_polygon(coords[0][0],
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


    def showTileDetails(x,y):
        print("(",x, ", ", y, ")", sep='')

    def getTileByXY(self,event):
        print(event.x,event.y)
        self.canvas.find_closest(event.x,event.y)

if __name__ =='__main__':
    view = View()
    map = tm.TileMap(7,7)
    map.getTile(3,3).type = 0
    view.drawMap(map)
    view.mainloop()







