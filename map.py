import pytmx
import os

MAPS_DIR = 'maps'


class Map:
    def __init__(self, filename, bad_tiles, ring_tiles, finish_tiles, level):
        absolute_path = os.path.dirname(__file__)
        relative_path = f'{MAPS_DIR}/{filename}'
        full_path = os.path.join(absolute_path, relative_path)
        self.map = pytmx.load_pygame(f'{MAPS_DIR}/map{level}.tmx')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = 30
        self.solid_tiles = bad_tiles
        self.finish_tiles = finish_tiles

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tile_id(self, position) -> int:
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]

    def is_free(self, position) -> bool:
        return self.get_tile_id(position) not in self.solid_tiles
