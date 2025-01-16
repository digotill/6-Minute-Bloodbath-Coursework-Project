from Code.Classes.Buttons import *
from Code.Classes.Entities import *
from Code.Utilities.Grid import *
from Code.Utilities.Particles import Spark
from pygame.math import Vector2 as v2
from perlin_noise import PerlinNoise
import pygame, math, random


class EnemyManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game, General_Settings["hash_maps"][0])  # Spatial hash grid for efficient enemy management
                    self.enemy_pool = set()  # Pool of inactive enemies for reuse
                    self.spawn_cooldown = General_Settings["enemies"][1]
                    self.last_spawn = - General_Settings["enemies"][1]
                    self.enemy_multiplier = 1  # Multiplier for enemy attributes (e.g., health, damage)

          def update(self):
                    # Update all enemies and apply separation forces
                    for enemy in self.grid.items:
                              enemy.update()
                              separation_force = self.calculate_separation(enemy)
                              enemy.apply_force(separation_force)

                    self.remove_dead_enemies()  # Remove enemies with no health
                    self.add_enemies("enemy1")  # Spawn new enemies if conditions are met
                    self.grid.rebuild()  # Rebuild the spatial hash grid

          def add_enemies(self, enemy_type):
                    # Check if it's time to spawn a new enemy and if the max enemy limit hasn't been reached
                    if (self.last_spawn + self.spawn_cooldown < self.game.game_time and
                            len(self.grid.items) < General_Settings["enemies"][0] and not General_Settings[
                                      "peaceful_mode"]):
                              self.last_spawn = self.game.game_time

                              # Generate random coordinates for the new enemy
                              coordinates = random_xy(
                                        pygame.Rect(0, 0, GAME_SIZE[0], GAME_SIZE[1]),
                                        self.game.camera.rect, AM.assets[enemy_type][0].width, AM.assets[enemy_type][0].height
                              )

                              # Reuse an enemy from the pool if available, otherwise create a new one
                              if self.enemy_pool:
                                        enemy = self.enemy_pool.pop()
                                        enemy.reset(coordinates, Enemies[enemy_type])
                              else:
                                        enemy = Enemy(self.game, coordinates, Enemies[enemy_type])

                              self.grid.insert(enemy)  # Add the enemy to the spatial hash grid

          def remove_dead_enemies(self):
                    # Remove enemies with no health and add them back to the pool
                    for enemy in self.grid.items.copy():
                              if enemy.health <= 0:
                                        enemy.dead = True
                              if enemy.dead:
                                        self.grid.items.remove(enemy)
                                        self.enemy_pool.add(enemy)

          def calculate_separation(self, enemy):
                    # Calculate separation force to prevent enemies from clustering too closely
                    steering = v2(0, 0)
                    total = 0
                    nearby_enemies = self.grid.query(
                              enemy.rect.inflate(enemy.separation_radius * 2, enemy.separation_radius * 2))

                    for other in nearby_enemies:
                              if other != enemy:
                                        distance = enemy.pos.distance_to(other.pos)
                                        if distance < enemy.separation_radius:
                                                  diff = (enemy.pos - other.pos).normalize() / distance
                                                  steering += diff
                                                  total += 1

                    if total > 0:
                              steering = (steering / total).normalize() * enemy.vel - enemy.vel_vector
                              if steering.length() > enemy.vel:
                                        steering = steering.normalize() * enemy.vel

                    return steering * enemy.separation_strength


class BulletManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game, General_Settings["hash_maps"][1])
                    self.bullet_pool = set()

          def update(self):
                    current_time = self.game.game_time
                    for bullet in self.grid.items:
                              bullet.update()
                              if current_time - bullet.creation_time > bullet.lifetime:
                                        bullet.dead = True
                    self.check_for_collisions()
                    self.check_dead_bullets()
                    self.grid.rebuild()

          def draw(self):
                    offset_x, offset_y = self.game.camera.offset_rect.topleft
                    for bullet in self.grid.window_query():
                              self.game.display_screen.blit(bullet.image,
                                                            (bullet.rect.x - offset_x, bullet.rect.y - offset_y))

          def add_bullet(self, pos, angle, name, spread):
                    if self.bullet_pool:
                              bullet = self.bullet_pool.pop()
                              bullet.reset(pos, angle, spread)
                    else:
                              bullet = Bullet(self.game, self.game.player.gun, pos, angle, name, spread, self.game.player.gun.noise_map)
                    self.grid.insert(bullet)
                    array = Screen_Shake[self.game.player.gun.name]
                    self.game.camera.add_screen_shake(array[1], array[0])

          def check_dead_bullets(self):
                    for bullet in self.grid.items.copy():
                              if bullet.dead:
                                        self.grid.items.remove(bullet)
                                        self.bullet_pool.add(bullet)

          def check_for_collisions(self):
                    for bullet in self.grid.items:
                              for enemy in self.game.enemy_manager.grid.query(bullet.rect):
                                        if bullet.rect.colliderect(enemy.rect) and not bullet.dead:
                                                  enemy.deal_damage(bullet.damage)
                                                  bullet.check_if_alive()
                                                  self.game.particle_manager.create_spark(270 - bullet.angle,
                                                                                          bullet.pos,
                                                                                          Sparks_Settings[
                                                                                                    'enemy_hit'])


class ParticleManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game, General_Settings["hash_maps"][5])
                    self.spark_pool = set()

          def update(self):
                    for spark in self.grid.items:
                              spark.move()
                    self.check_if_remove()
                    self.grid.rebuild()

          def draw(self):
                    for spark in self.grid.window_query():
                              spark.draw()

          def create_spark(self, angle, pos, dictionary):
                    for _ in range(dictionary['amount']):
                              spark_angle = math.radians(random.randint(
                                        int(angle) - dictionary['spread'],
                                        int(angle) + dictionary['spread']
                              ))
                              spark_velocity = random.randint(dictionary["min_vel"], dictionary["max_vel"])
                              if len(self.spark_pool) == 0:
                                        self.grid.insert(
                                                  Spark(self.game, pos, spark_angle, spark_velocity,
                                                        dictionary['colour'], dictionary['scale']))
                              else:
                                        spark = self.spark_pool.pop()
                                        spark.reset(pos, spark_angle, spark_velocity, dictionary["colour"],
                                                    dictionary['scale'])
                                        self.grid.insert(spark)

          def check_if_remove(self):
                    for spark in self.grid.items.copy():
                              if not spark.alive:
                                        self.grid.items.remove(spark)
                                        self.spark_pool.add(spark)


class ObjectManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game, General_Settings["hash_maps"][4])
                    self.biome_noise = PerlinNoise(octaves=Perlin_Noise["biome_map"][1], seed=random.randint(0, 100000))
                    self.density_noise = PerlinNoise(octaves=Perlin_Noise["density_map"][1], seed=random.randint(0, 100000))
                    self.generate_objects()

          def generate_objects(self):

                    # Generate biome and density maps
                    biome_map = self.generate_noise_map(self.biome_noise, Perlin_Noise["biome_map"][0])
                    density_map = self.generate_noise_map(self.density_noise, Perlin_Noise["density_map"][0])

                    size = Objects_Config["tree"][1]
                    sorted_biomes = sorted(Biomes_Config.items(), key=lambda x_: x_[1])
                    # Generate trees based on biome and density
                    for y in range(0, GAME_SIZE[1], size):
                              for x in range(0, GAME_SIZE[0], size):
                                        biome_value = biome_map[y // size][x // size]
                                        density_value = density_map[y // size][x // size]
                                        biome_density_factor = 1

                                        biome = "green"
                                        for biome_name, data in sorted_biomes:
                                                  if biome_value < data[0]:
                                                            biome = biome_name
                                                            biome_density_factor = data[1]
                                                            break


                                        # Check if we should place a tree based on density
                                        if random.random() < density_value * Objects_Config["tree"][0] * biome_density_factor:  # Adjust 0.1 to control overall tree density
                                                  tree_image = random.choice(self.game.assets[biome + "_tree"])
                                                  pos = self.generate_valid_position(tree_image.size, x, y)
                                                  if pos:
                                                            self.grid.insert(
                                                                      Object(self.game, tree_image, tree_image.size,
                                                                             pos, True))

                    for _ in range(Objects_Config["rock"][0]):
                              image = random.choice(AM.assets["rock"])
                              pos = self.generate_valid_position(image.size)
                              if pos:
                                        self.grid.insert(Object(self.game, image, image.size, pos, Objects_Config["rock"][1]))

                    self.grid.rebuild()

          def generate_valid_position(self, size, base_x=None, base_y=None):
                    if base_x is None or base_y is None:
                              base_x, base_y = random.randint(0, GAME_SIZE[0]), random.randint(0, GAME_SIZE[1])

                    v = Objects_Config["placement"][0]
                    for _ in range(10):
                              x = base_x + random.randint(-v, v)
                              y = base_y + random.randint(-v, v)
                              if 0 <= x < GAME_SIZE[0] - size[0] and 0 <= y < GAME_SIZE[1] - size[1]:
                                        rect = pygame.Rect(x - size[0] * 0.25, y + size[1] * 0.5, size[0] / 2, size[1] / 10)
                                        if not self.game.tilemap.tile_collision(rect, "water_tile"):
                                                  return v2(x, y)
                    return None

          @staticmethod
          def generate_noise_map(noise, scale):
                    size = Objects_Config["tree"][1]
                    width, height = GAME_SIZE[0] // size, GAME_SIZE[1] // size
                    noise_map = [[noise([i * scale, j * scale]) for j in range(width)] for i in range(height)]
                    return (np.array(noise_map) + 1) / 2  # Normalize to [0, 1]


class SoundManager:
          def __init__(self, game):
                    self.game = game


class ButtonManager:
          def __init__(self, game):
                    self.game = game

                    self.buttons = {}
                    self.sliders = {}

                    self._create_buttons()
                    self._create_sliders()

                    self.cooldown = General_Settings['cooldowns'][0]
                    self.last_pressed_time = - General_Settings['cooldowns'][0]

                    self.value_cooldown = General_Settings['cooldowns'][1]
                    self.last_value_set = -General_Settings['cooldowns'][1]

          def _create_buttons(self):
                    button_configs = AllButtons
                    for name, config in button_configs["In_Game"].items():
                              self.buttons[name] = Button(
                                        self.game,
                                        copy.deepcopy(config)
                              )

          def _create_sliders(self):
                    button_configs = AllButtons
                    for name, config in button_configs["Sliders"].items():
                              self.sliders[name] = Slider(
                                        self.game,
                                        copy.deepcopy(config)
                              )

          def update(self):
                    all_elements = list(self.buttons.values()) + list(self.sliders.values())
                    for buttons in all_elements:
                              buttons.active = self.game.changing_settings
                              buttons.update()
                              buttons.changeColor()

                    if self.game.changing_settings and self.game.mouse_state[
                              0] and pygame.time.get_ticks() / 1000 - self.last_pressed_time > self.cooldown:
                              temp_time = self.last_pressed_time
                              self.last_pressed_time = pygame.time.get_ticks() / 1000
                              if self.buttons['resume'].check_for_input():
                                        self.game.changing_settings = False
                              elif self.sliders['fps'].update_value:
                                        self.game.fps = self.sliders['fps'].value
                              elif self.sliders['brightness'].update_value:
                                        self.game.ui_manager.brightness = self.sliders['brightness'].value
                              elif self.buttons['fullscreen'].check_for_input():
                                        pygame.display.toggle_fullscreen()
                              elif self.buttons['quit'].check_for_input():
                                        self.game.immidiate_quit = True
                              elif self.buttons['return'].check_for_input():
                                        self.game.restart = True
                              else:
                                        self.last_pressed_time = temp_time

                    if self.game.changing_settings and pygame.time.get_ticks() / 1000 - self.last_value_set > self.value_cooldown:
                              self.game.fps = self.sliders['fps'].value
                              self.game.ui_manager.brightness = self.sliders['brightness'].value
                              self.last_value_set = pygame.time.get_ticks() / 1000

          def draw(self):
                    all_elements = list(self.buttons.values()) + list(self.sliders.values())

                    # Sort all elements by their y position
                    sorted_elements = sorted(all_elements, key=lambda element: element.pos.y)
                    for button in sorted_elements:
                              button.draw()


class RainManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = HashMap(game, General_Settings["hash_maps"][3])
                    self.cooldown = Rain_Config['spawn_rate']
                    self.last_spawn = - Rain_Config['spawn_rate']

                    self.grid.rebuild()

          def update(self):
                    for rain_droplet in self.grid.items:
                              rain_droplet.update()
                              if rain_droplet.hit_ground:
                                        rain_droplet.update_frame()
                                        self.game.drawing_manager.drawables.append(rain_droplet)
                    self.create()
                    self.check_dead()
                    self.grid.rebuild()

          def draw(self):
                    for rain_droplet in self.grid.window_query():
                              if not rain_droplet.hit_ground:
                                        rain_droplet.draw()

          def create(self):
                    if self.game.game_time - self.last_spawn > self.cooldown:
                              for _ in range(Rain_Config['amount_spawning']):
                                        self.grid.insert(Rain(self.game, Rain_Config))
                                        self.last_spawn = self.game.game_time

          def check_dead(self):
                    for rain_droplet in self.grid.items.copy():
                              if rain_droplet.frame >= len(rain_droplet.animation):
                                        self.grid.items.remove(rain_droplet)


class DrawingManager:
          def __init__(self, game):
                    self.game = game
                    self.drawables = []

          def transparent_objects(self):
                    for thing in self.game.object_manager.grid.query(self.game.player.rect):
                              if thing.rect.colliderect(self.game.player.rect):
                                        dx = thing.rect.bottom - self.game.player.rect.bottom
                                        dy = thing.rect.bottom - self.game.player.rect.bottom
                                        squared_distance = dx * dx + dy * dy
                                        greatest_side = thing.image.get_height()
                                        alpha = max(100,
                                                    min(squared_distance / (greatest_side * greatest_side) * 255, 255))
                                        if self.game.player.rect.bottom > thing.rect.bottom: alpha = 255
                                        thing.image = thing.original_image.copy()
                                        thing.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
                              else:
                                        thing.image = thing.original_image.copy()

          def draw(self):
                    self.transparent_objects()
                    for obg in self.game.object_manager.grid.window_query():
                              self.game.drawing_manager.drawables.append(obg)

                    for enemy in self.game.enemy_manager.grid.window_query():
                              self.game.drawing_manager.drawables.append(enemy)

                    self.game.drawing_manager.drawables.append(self.game.player)

                    self.drawables.sort(key=lambda obj: obj.rect.bottom)
                    for drawable in self.drawables:
                              drawable.draw()
                    self.drawables = []
