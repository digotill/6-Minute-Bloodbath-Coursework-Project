import pygame
import os
from PIL import Image
import io


class AssetManager:
          def __init__(self):
                    self.assets = {}
                    self.load_all_assets()

          def load_all_assets(self):
                    assets_dir = "Assets"
                    for root, dirs, files in os.walk(assets_dir):
                              for file in files:
                                        file_path = os.path.join(root, file)
                                        file_name, file_ext = os.path.splitext(file)

                                        if "tileset" in file_name.lower():
                                                  self.import_tileset(file_path, file_name)
                                        elif file_ext.lower() in ['.png', '.jpg', '.jpeg']:
                                                  self.load_image(file_path, file_name)
                                        elif file_ext.lower() == '.gif':
                                                  self.import_gif(file_path, file_name)
                                        elif file_ext.lower() in ['.wav', '.ogg', '.mp3']:
                                                  self.load_sound(file_path, file_name)
                                        elif file_ext.lower() in ['.ttf']:
                                                  self.load_font(file_path, file_name)

          def import_gif(self, path, name):
                    frames = []
                    with Image.open(path) as gif:
                              for frame_index in range(gif.n_frames):
                                        gif.seek(frame_index)
                                        frame_rgba = gif.convert("RGBA")
                                        pygame_image = pygame.image.fromstring(
                                                  frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
                                        )
                                        frames.append(pygame_image)
                    self.assets[name] = frames

          def load_image(self, file_path, name, res=None, *color_keys):
                    img = pygame.image.load(file_path).convert_alpha()
                    if res:
                              img = pygame.transform.scale(img, res)
                    for color_key in color_keys:
                              img.set_colorkey(color_key)
                    self.assets[name] = img

          def load_sound(self, file_path, name):
                    sound = pygame.mixer.Sound(file_path)
                    self.assets[name] = sound

          def import_tileset(self, filepath, name):
                    tileset_image = pygame.image.load(filepath).convert_alpha()
                    tile = pygame.Surface((16, 16), pygame.SRCALPHA)
                    array = ["1212", "2201", "1010", "1022", "2222", "1001", "0000", "0110", "2121", "0122", "0101", "2210", "", "1221", "2222", "2112"]
                    dictionary = {}  # "top", "bottom", "right", "left"
                    for i in range(4):
                              for j in range(4):
                                        self.add_tile(tile, (j, i), dictionary, array, tileset_image, i * 4 + j)
                    temp_array = ["2201", "1022", "0122", "2210"]
                    temp_array2 = ["1101", "1011", "0111", "1110"]
                    for item in dictionary.copy().keys():
                              if item in temp_array:
                                        key = temp_array2[temp_array.index(item)]
                                        dictionary[key] = dictionary[item]
                    array = ["1000", "0100", "0010", "0001"]
                    for i in range(4):
                              self.add_tile(tile, (2, 1), dictionary, array, tileset_image, i)
                    self.assets[name] = dictionary


          @staticmethod
          def add_tile(tile, position, dictionary, array, tileset_image, count):
                    tile.fill((0, 0, 0, 0))
                    tile.blit(tileset_image, (0, 0), (16 * position[0], 16 * position[1], 16, 16))
                    dictionary[array[count]] = [tile.copy()]


          def load_font(self, file_path, name):
                    self.assets[name] = pygame.font.Font(file_path, int(name[4:]))
