import TileMap
import Tile
import math
import View
import Civilization
from tkinter import *

# mapa = TileMap.TileMap(10, 10)
# sasiedzi = mapa.getNeighboursByCoords(4, 4)


# for n in sasiedzi:
#    n.printCoords()

view = View.View()
map = TileMap.TileMap(100,170)
m = map.getMap()

x = 70
y = 50
civ1 = Civilization.Civilization(0)
while map.getTile(x, y).getType() != 1:
    x -= 1
civ1.setStartingTile(map.getTile(x, y))

x = 20
y = 40
civ2 = Civilization.Civilization(1)
while map.getTile(x, y).getType() != 1:
    y += 1
civ2.setStartingTile(map.getTile(x, y))

view.addCiv(civ1)
view.addCiv(civ2)
#for i in m:
#    for j in i:
#        j.printCoords()
view.drawMap(map)
print(len(view.hexagons))
view.mainloop()
