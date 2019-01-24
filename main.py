import TileMap
import Tile
import math
import View as View
import Civilization
from tkinter import *

# mapa = TileMap.TileMap(10, 10)
# sasiedzi = mapa.getNeighboursByCoords(4, 4)


# for n in sasiedzi:
#    n.printCoords()

map = TileMap.TileMap(100,170)
#m = map.getMap()

x = 30
y = 50
civ1 = Civilization.Civilization(0)
while map.getTile(x, y).getType() != 1:
    x -= 1
civ1.setStartingTile(map.getTile(x, y))

x = 50
y = 70
civ2 = Civilization.Civilization(1)
while map.getTile(x, y).getType() != 1:
    y += 1
civ2.setStartingTile(map.getTile(x, y))

x = 80
y = 80
civ3 = Civilization.Civilization(2)
while map.getTile(x, y).getType() != 1:
    x -= 1
civ3.setStartingTile(map.getTile(x, y))

x = 90
y = 30
civ4 = Civilization.Civilization(3)
while map.getTile(x, y).getType() != 1:
    y += 1
civ4.setStartingTile(map.getTile(x, y))



#for i in m:
#    for j in i:
#        j.printCoords()
view = View.View(map)


civ1.setAgrRateVal(10)      # ustawienia cywilizacji różowej
civ1.setTechPriority(3)     # bazowo 1, max 10, wartość <=0 oznacza że cywilizacja nie będzie dążyła do rozwoju
                            # technologicznego a zamiast tego będzie skupiać się na wzroście populacji
civ1.setConcentrationRateVal(10)
view.addCiv(civ1)

civ2.setAgrRateVal(10)  # ustawienia cywilizacji niebieskiej
civ2.setConcentrationRateVal(1.5)
civ2.setTechPriority(4)
view.addCiv(civ2)

civ3.setAgrRateVal(10)  # ustawienia cywilizacji zielonej
civ3.setConcentrationRateVal(1.5)
civ3.setTechPriority(0)
view.addCiv(civ3)

civ4.setAgrRateVal(10)  # ustawienia cywilizacji pomarańczowej
civ4.setConcentrationRateVal(3)
civ4.setTechPriority(8)
view.addCiv(civ4)
print(len(view.hexagons))
view.mainloop()
