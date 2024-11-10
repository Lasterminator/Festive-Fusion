import pygame

class TileKind:
    def __init__(self, name, image, is_solid):
        self.name = name
        self.image = pygame.image.load(image)
        self.is_solid = is_solid


class Map:
    def __init__(self, map_file, tile_kinds, tile_size):
        self.tile_kinds = tile_kinds

        file = open(map_file, "r")
        data = file.read()
        file.close()

        self.tiles = []

        for line in data.split("\n"):
            row = []
            for tile_number in line:
                row.append(int(tile_number))
            self.tiles.append(row)

        self.tile_size = tile_size


    def draw(self, screen):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                location = (x * self.tile_size, y * self.tile_size)
                image = self.tile_kinds[tile].image
                screen.blit(image, location)