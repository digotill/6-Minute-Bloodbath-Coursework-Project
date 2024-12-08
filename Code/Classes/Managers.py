from Code.Classes.Buttons import *
from Code.Classes.Entities import *
from Code.Utilities.Grid import *
from Code.Utilities.Particles import Spark
import pygame, math, random


class EnemyManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = SpatialHash(game)
                    self.enemy_pool = set()
                    self.spawn_cooldown = 1
                    self.last_spawn = 0
                    self.enemy_multiplier = 1
                    self.separation_radius = General_Settings["enemy_separation_radius"]
                    self.separation_strength = General_Settings["enemy_separation_strength"]

          def update_enemies(self):
                    for enemy in self.grid.items:
                              separation_force = self.calculate_separation(enemy)
                              enemy.apply_force(separation_force)
                              enemy.update()
                    self.remove_dead_enemies()
                    self.add_enemies(Enemies["enemy1"])
                    self.grid.rebuild()

          def draw_enemies(self):
                    for enemy in self.grid.window_query():
                              enemy.blit()

          def add_enemies(self, enemy):
                    if (self.last_spawn + self.spawn_cooldown < self.game.game_time and
                            len(self.grid.items) < General_Settings["max_enemies"] and not PEACEFUL_MODE):
                              self.last_spawn = self.game.game_time
                              coordinates = random_xy(
                                        pygame.Rect(0, 0, self.game.big_window[0], self.game.big_window[1]),
                                        self.game.window.rect, enemy["res"][0], enemy["res"][1]
                              )
                              if self.enemy_pool:
                                        entity = self.enemy_pool.pop()
                                        self.reset_enemy(entity, coordinates, enemy)
                              else:
                                        entity = Enemy(self.game, coordinates, enemy)
                              self.grid.insert(entity)

          def remove_dead_enemies(self):
                    for enemy in self.grid.items.copy():
                              if enemy.health <= 0:
                                        enemy.dead = True
                              if enemy.dead:
                                        self.grid.items.remove(enemy)
                                        self.game.window.add_screen_shake(
                                                  duration=Screen_Shake["bullet_impact_shake_duration"],
                                                  magnitude=Screen_Shake['bullet_impact_shake_magnitude']
                                        )
                                        self.enemy_pool.add(enemy)

          def calculate_separation(self, enemy):
                    steering = v2(0, 0)
                    total = 0
                    nearby_enemies = self.grid.query(
                              enemy.rect.inflate(self.separation_radius * 2, self.separation_radius * 2))

                    for other in nearby_enemies:
                              if other != enemy:
                                        distance = enemy.pos.distance_to(other.pos)
                                        if distance < self.separation_radius:
                                                  diff = (enemy.pos - other.pos).normalize() / distance
                                                  steering += diff
                                                  total += 1

                    if total > 0:
                              steering = (steering / total).normalize() * enemy.vel - enemy.vel_vector
                              if steering.length() > enemy.vel:
                                        steering = steering.normalize() * enemy.vel

                    return steering * self.separation_strength

          @staticmethod
          def reset_enemy(entity, coordinates, enemy):
                    entity.pos = v2(coordinates)
                    entity.rect.center = coordinates
                    entity.vel_vector = v2(0, 0)
                    entity.acceleration = v2(0, 0)
                    entity.health = enemy['health']
                    entity.res = enemy['res']
                    entity.max_vel = enemy['vel']
                    entity.name = enemy['name']
                    entity.damage = enemy['damage']
                    entity.dead = False
                    entity.facing = "right"
                    entity.frame = 0
                    entity.animation_speed = enemy['animation_speed']
                    entity.stopping_distance = enemy['stopping_distance']
                    entity.steering_strength = enemy['steering_strength']
                    entity.friction = enemy['friction']
                    if 'image' in enemy:
                              entity.images = enemy['image']


class BulletManager:
          def __init__(self, game):
                    self.game = game
                    self.grid = SpatialHash(game)
                    self.player_bullets = set()
                    self.enemy_bullets = set()
                    self.bullet_pool = set()

          def update(self):
                    current_time = self.game.game_time
                    for bullet in list(self.grid.items):
                              bullet.update()
                              if current_time - bullet.creation_time > bullet.lifetime:
                                        bullet.dead = True
                    self.check_for_collisions()
                    self.check_dead_bullets()
                    self.grid.rebuild()

          def draw(self):
                    offset_x, offset_y = self.game.window.offset_rect.topleft
                    for bullet in self.grid.window_query():
                              self.game.display_screen.blit(bullet.image,
                                                            (bullet.rect.x - offset_x, bullet.rect.y - offset_y))

          def add_bullet(self, start_x, start_y, angle, name, spread):
                    if self.bullet_pool:
                              bullet = self.bullet_pool.pop()
                              bullet.reset(start_x, start_y, angle, spread)
                    else:
                              bullet = Bullet(self.game, self.game.player.gun, (start_x, start_y), angle, name, spread)
                    self.grid.insert(bullet)
                    bullet_set = self.player_bullets if name == "Player Bullet" else self.enemy_bullets
                    bullet_set.add(bullet)

          def check_dead_bullets(self):
                    for bullet in self.grid.items.copy():
                              if bullet.dead:
                                        self.grid.items.remove(bullet)
                                        bullet_set = self.player_bullets if bullet.name == "Player Bullet" else self.enemy_bullets
                                        bullet_set.remove(bullet)
                                        self.bullet_pool.add(bullet)

          def check_for_collisions(self):
                    for bullet in self.player_bullets:
                              for enemy in self.game.enemy_manager.grid.query(bullet.rect):
                                        if bullet.check_collision(enemy):
                                                  self.create_bullet_sparks(bullet)
                                                  break

          def create_bullet_sparks(self, bullet):
                    spark_angle = math.radians(random.randint(
                              int(270 - bullet.angle) - Sparks_Settings['bullet']['spread'],
                              int(270 - bullet.angle) + Sparks_Settings['bullet']['spread']
                    ))
                    for _ in range(Sparks_Settings['bullet']['amount']):
                              self.game.particle_manager.sparks.add(
                                        Spark(self.game, bullet.pos, spark_angle,
                                              random.randint(3, 6), Sparks_Settings['bullet']['colour'],
                                              Sparks_Settings['bullet']['size'])
                              )


class ParticleManager:
          def __init__(self, game):
                    self.game = game
                    self.sparks = set()

          def update(self):
                    for _, spark in sorted(enumerate(self.sparks), reverse=True):
                              spark.move()
                              if not spark.alive:
                                        self.sparks.remove(spark)

          def draw(self):
                    for _, spark in sorted(enumerate(self.sparks), reverse=True):
                              spark.draw()


class ObjectManager:
          def __init__(self, game):
                    self.current_objects = []
                    self.game = game
                    self.interaction = True
                    self.position = 0

          def update(self):
                    pass

          def draw(self):
                    pass


class SoundManager:
          def __init__(self, game):
                    self.game = game
                    self.sounds = {}


class ButtonManager:
          def __init__(self, game):
                    self.game = game
                    self.buttons = {}
                    self.sliders = {}
                    self._create_buttons()
                    self._create_sliders()

          def _create_buttons(self):
                    button_configs = {
                              'resume': Buttons['resume'],
                              'fullscreen': Buttons['fullscreen'],
                              'quit': Buttons['quit'],
                              'return': Buttons['Return'],
                    }
                    for name, config in button_configs.items():
                              self.buttons[name] = Button(
                                        self.game,
                                        Button_Images["Button1"],
                                        config['pos'],
                                        config['axis'],
                                        config['axisl'],
                                        text_input=config['name']
                              )

          def _create_sliders(self):
                    slider_configs = {
                              'fps': {
                                        **Sliders['fps'],
                                        'max_value': 240,
                                        'min_value': 60,
                                        'initial_value': pygame.display.get_current_refresh_rate()
                              },
                              'brightness': {
                                        **Sliders['brightness'],
                                        'max_value': 100,
                                        'min_value': 0,
                                        'initial_value': Window_Attributes['brightness'],
                              }
                    }
                    for name, config in slider_configs.items():
                              self.sliders[name] = Slider(
                                        self.game,
                                        Button_Images["Button2"],
                                        config['pos'],
                                        config['axis'],
                                        config['axisl'],
                                        text_input=config['text'],
                                        text_pos=config['text_pos'],
                                        max_value=config['max_value'],
                                        min_value=config['min_value'],
                                        initial_value=config['initial_value']
                              )

          def update_buttons(self):
                    all_elements = list(self.buttons.values()) + list(self.sliders.values())
                    for element in all_elements:
                              element.active = self.game.changing_settings
                              element.update()
                              element.changeColor()

                    if self.game.mouse_state[0]:
                              if self.buttons['resume'].check_for_input():
                                        self.game.changing_settings = False
                              elif self.sliders['fps'].update_value:
                                        self.game.fps = self.sliders['fps'].value
                              elif self.sliders['brightness'].update_value:
                                        self.game.UI_Settings.brightness = self.sliders['brightness'].value
                              elif self.buttons['fullscreen'].check_for_input():
                                        self.game.event_manager.update_size(True)
                              elif self.buttons['quit'].check_for_input():
                                        self.game.immidiate_quit = True
                              elif self.buttons['return'].check_for_input():
                                        self.game.return_to_menu = True

          def draw_buttons(self):
                    for element in list(self.buttons.values()) + list(self.sliders.values()):
                              element.draw()
