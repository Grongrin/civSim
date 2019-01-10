import TileMap as tm
import Civilization
from tkinter import *
import math

class Tile:
    def __init__(self,x,y,a,cords,index,civ):
        self.x_ = x
        self.y_= y
        self.a_ = a
        self.cords_ = cords
        self.index_=index
        self.civilizationId_ = civ


class View(Tk):
    def __init__(self,tilemap):
        Tk.__init__(self)
        self.hexagons = []
        self.civs_ = []
        self.biggestTileX=0
        self.biggestTileY=0
        self.infoId=0
        self.canvas = Canvas(width=1400, height=900,bg="#AFEEEE" )
        self.canvas.pack()
        self.canvas.bind("<Motion>", self.getTileByXY)
        self.a_ = 0
        self.tilemap_=tilemap
        self.drawMap()

    def addCiv(self, civ):
        self.civs_.append(civ)
        for t in civ.getTerritory():
            self.drawTile(t, self.a_)

    def findCivById(self,id):
        for civ in self.civs_:
            print(civ.getId())
            if civ.getId()==id:
                return civ
        return None

    def drawMap(self):
        map=self.tilemap_
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
        self.doChanges()

    def fromRGB(self, R, G, B): # tłumaczenie koloru RGB na kolor dla tkinter
        return "#%02x%02x%02x" % (R, G, B)

    def drawTile(self,tile,a):
        if tile is None:
            return
        colors = [
            "#FFFF66",
            "#3366FF",
            "#F700FF",
            "#091e4a",
            "#00FF17",
            "#FFF000"
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
        civ = tile.getCiv()
        if (civ):
            civId = civ.getId()
        else:
            civId=-1
        hex = Tile(tile.getX(),tile.getY(),a,coords,index,civId)
        self.hexagons.append(hex)

    def civInfo(self,civilization):
        civInfo="\nCiv Id: "+str(civilization.id_)+"\n"
        civInfo +="Obecna populacja: "+str(civilization.population_)+" \nŻołnierze: "+str(civilization.soldiers_)+ " \nRobotnicy: "+str(civilization.laborers_)+"\n"
        civInfo +="AgrVal: "+str(civilization.territoryAgrValue_)+"\n"
        civInfo +="Produkcja: "+str(civilization.agrOutput_)+" \nProdukcja po odjęciu  kosztu armii: "+str(civilization.agrOutput_ - civilization.calcArmyWages()*civilization.soldiers_)+"\n"
        civInfo +="Produkcja na robotnika po odjęciu podatku: "+str((civilization.agrOutput_) * (1 - civilization.taxrate_) / civilization.laborers_)+"\n"
        civInfo +="Żołd na jednego żołnierza: "+str(civilization.calcArmyWages())+"\n"
        civInfo +="Max territory: "+str(civilization.maxTerritory_)+" \nCurrent territory: "+str(civilization.currTerritory_)+"\n"
        civInfo +="Tresury: "+ str(civilization.tresury_)+"\n"
        civInfo +="Tax rate: "+str(civilization.taxrate_)+"\n"
        return civInfo

    def showTileDetails(self,tile):
        self.canvas.delete(self.infoId)
        civId = tile.civilizationId_
        if civId==-1:
            onscreen = "Tile info:\nWspółrzędne: ("+str(tile.x_)+","+str(tile.y_)+")"+\
                       "\nŻyzność pola: "+tile.getAgrVal()
        else:
            onscreen = "Tile info:\n("+str(tile.x_)+","+str(tile.y_)+")"+"\n\n\n\nCvilization info:"+self.civInfo(self.findCivById(civId))
        self.infoId=self.canvas.create_text((700,20),anchor="nw",font=("helvetica", 12),text=onscreen)


    def findNearestTile(self,nearest):
        for i in self.hexagons:
            if i.index_ == nearest:
                return i
        return None

    def doChanges(self):
        for c in self.civs_:
            changedTiles = c.makeMove()
            if changedTiles is not None:
                for t in changedTiles:
                    self.drawTile(t, self.a_)
        self.canvas.update()
        self.canvas.after(1,self.doChanges)

    def getTileByXY(self, event):
        if (event.x<self.biggestTileX and event.y<self.biggestTileY):
            nearest = int(self.canvas.find_closest(event.x,event.y)[0])
            tile = self.findNearestTile(nearest)
            if tile:
                self.showTileDetails(tile)









