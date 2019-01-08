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
civ1 = Civilization.Civilization(0)
print("tile 10,10 civ id: ", map.getTile(10, 10).getCivId())
civ1.setStartingTile(map.getTile(10,10))
print("Civ1 id: ", civ1.getId())
print("tile 10,10 civ id: ", map.getTile(10, 10).getCivId())
view.addCiv(civ1)
#for i in m:
#    for j in i:
#        j.printCoords()
view.drawMap(map)
print(len(view.hexagons))
view.mainloop()
