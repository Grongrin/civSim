import TileMap

mapa = TileMap.TileMap(10, 10)
sasiedzi = mapa.getNeighboursByCoords(4, 4)


for n in sasiedzi:
    n.printCoords()