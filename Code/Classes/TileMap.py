from pygame import Vector2

from Code.Utilities.Grid import *


class Tile:
          def __init__(self, tile_type, position):
                    self.tile_type = tile_type
                    self.position = Vector2(position)
                    self.size = General_Settings['tilemap_size']
                    self.rect = pygame.Rect(self.position.x, self.position.y, self.size, self.size)
                    self.images = Tile_Images[tile_type]

          def draw(self, surface, offset, frame):
                    draw_position = self.position - offset
                    surface.blit(self.images[int(frame % len(self.images))], draw_position)

class TileMap:
          def __init__(self, game):
                    self.game = game

                    self.tile_size = 16
                    self.grid = HashMap(game, self.tile_size)
                    self.width = GAME_SIZE[0] // self.tile_size + 1
                    self.height = GAME_SIZE[1] // self.tile_size + 1

                    self.animation_speed = Tile_Images["animation_speed"]
                    self.frames = {tile_type: 0 for tile_type in ["Water_Tile"]}

                    self.terrain_generator()
                    self.grass_generator()

                    self.grid.rebuild()

          def add_tile(self, tile_type, grid_position):
                    pixel_position = (grid_position[0] * self.tile_size, grid_position[1] * self.tile_size)
                    tile = Tile(tile_type, pixel_position)
                    self.grid.insert(tile)

          def draw(self):
                    if not self.game.changing_settings:
                              for tile_type in self.frames:
                                        self.frames[tile_type] += self.game.dt * self.animation_speed
                    for tile in self.grid.window_query():
                              if tile.tile_type in self.frames:
                                        tile.draw(self.game.display_screen, self.game.camera.offset_rect.topleft,
                                                  self.frames[tile.tile_type])
                              else:
                                        tile.draw(self.game.display_screen, self.game.camera.offset_rect.topleft, 0)

          @staticmethod
          def get_tile_type(x, y):
                    noise_value = Perlin_Noise["1 octave"]([x * 0.05, y * 0.05])
                    for tile in Tiles_Congifig["Tile_Ranges"].keys():
                              if noise_value < Tiles_Congifig["Tile_Ranges"][tile]:
                                        return tile

          def _get_cell(self, position):
                    return int(position[0] // self.cell_size), int(position[1] // self.cell_size)

          def tile_collision(self, rect, *tile_types):
                    for tile in self.grid.query(rect):
                              for tile_type in tile_types:
                                        if tile.tile_type == tile_type:
                                                  return True
                    return False

          def get(self, grid_position):
                    pixel_position = (grid_position[0] * self.tile_size, grid_position[1] * self.tile_size)
                    tile = self.grid.grid.get(grid_position, None)
                    if isinstance(tile, list) and tile:
                              for i in tile:
                                        if i.rect.topleft == pixel_position:
                                                  return i
                    return None

          def apply_transition_tiles(self):
                    directions = ["top", "right", "bottom", "left", "topleft", "topright", "bottomleft", "bottomright"]
                    for tile in self.grid.items:
                              if tile.tile_type == "Water_Tile":
                                        grid_x, grid_y = int(tile.position.x // self.tile_size), int(
                                                  tile.position.y // self.tile_size)
                                        neighbors = [
                                                  self.get((grid_x + dx, grid_y + dy))
                                                  for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]
                                        ]

                                        if any(neighbor and neighbor.tile_type == "Grass_Tile" for neighbor in neighbors
                                               if neighbor):
                                                  black_image = pygame.Surface((self.tile_size, self.tile_size))
                                                  black_image.fill((0, 0, 0))

                                                  tile.images = [black_image] * len(tile.images)

          def terrain_generator(self):
                    for x in range(self.width):
                              for y in range(self.height):
                                        tile_type = self.get_tile_type(x, y)
                                        self.add_tile(tile_type, (x, y))

                    self.apply_transition_tiles()

          def grass_generator(self):
                    for tile in self.grid.items:
                              if tile.tile_type == "Grass_Tile":
                                        v = random.random()
                                        if v < Grass["Density"]:
                                                  self.game.grass_manager.place_tile(
                                                            (tile.position.x // Grass["Grass_Settings"]["tile_size"],
                                                             tile.position.y // Grass["Grass_Settings"]["tile_size"]),
                                                            int(v * 12),
                                                            [0, 1, 2, 3, 4])
