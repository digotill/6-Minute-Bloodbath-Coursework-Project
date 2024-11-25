import pygame, math, random, perlin_noise
from Code.Variables.Variables import *
from Code.Variables.Initialize import *
from Code.Utilities.Utils import *
from pygame.math import Vector2 as v2
from Code.Utilities.Particles import Spark

class RectEntity:
          def __init__(self, game, coordinates, res, vel, name, angle=None):
                    self.game = game
                    self.pos = v2(coordinates)
                    self.name = name
                    self.res = res
                    self.rect = pygame.Rect(self.pos.x, self.pos.y, res[0], res[1])
                    self.vel = vel
                    if angle is not None:
                              self.vel_vector = v2(self.vel * math.sin(math.radians(angle)),
                                                   self.vel * math.cos(math.radians(angle)))
                              self.angle = angle
                    if name == "Player":
                              self.stamina = PLAYER_STAMINA

          def calc_angle(self):
                    return v2(self.game.player.pos.x + 0.5 * self.game.player.res[0] - self.pos.x - 0.5 * self.res[0],
                              self.game.player.pos.y + 0.5 * self.game.player.res[1] - self.pos.y - 0.5 * self.res[
                                        1]).angle_to((0, 1))


class AnimatedEntity:
          def __init__(self, game, images, animation=ANIMATION_SPEED):
                    self.game = game
                    self.images = images
                    self.animation = animation
                    self.frame = 0
                    self.facing = "right"

          def update_frame(self):
                    self.frame += self.animation * self.game.dt


class AnimalEntity:
          def __init__(self, game, health, damage):
                    self.game = game
                    self.health = health
                    self.damage = damage
                    self.dead = False


class Player(RectEntity, AnimatedEntity, AnimalEntity):
          def __init__(self, game, health, res, vel, damage, coordinates, name, images, angle=None,
                       animation=ANIMATION_SPEED, acceleration=PLAYER_ACCELERATION):
                    RectEntity.__init__(self, game, coordinates, res, vel, name, angle)
                    AnimalEntity.__init__(self, game, health, damage)
                    self.acceleration = acceleration
                    self.current_vel = 0
                    self.gun = Gun(game, Rifle, PLAYER_GUN_RES, Rifle_bullet, PLAYER_GUN_DISTANCE, PLAYER_BULLET_SPEED,
                                   PLAYER_BULLET_LIFETIME, PLAYER_BULLET_RATE, PLAYER_BULLET_FRICTION)
                    AnimatedEntity.__init__(self, game, images, animation)
                    self.pos.x -= self.res[0] / 2
                    self.pos.y -= self.res[1] / 2

          def update(self):
                    dx, dy = 0, 0
                    if self.game.keys[pygame.K_a]: dx -= 1
                    if self.game.keys[pygame.K_d]: dx += 1
                    if self.game.keys[pygame.K_s]: dy += 1
                    if self.game.keys[pygame.K_w]: dy -= 1

                    magnitude = math.sqrt(dx ** 2 + dy ** 2)
                    if magnitude != 0:
                              dx /= magnitude
                              dy /= magnitude

                    if (dy != 0 or dx != 0) and not self.game.changing_settings: self.update_frame()
                    self.update_velocity(dy, dx)
                    self.update_facing()

                    new_x = self.pos.x + dx * self.current_vel * self.game.dt
                    new_y = self.pos.y + dy * self.current_vel * self.game.dt

                    move_hor, move_vert = False, False
                    if not self.game.changing_settings:
                              if PLAYER_OFFSET_X1 < new_x < self.game.big_window[0] - self.res[0] + PLAYER_OFFSET_X2:
                                        self.pos.x = new_x
                                        self.rect.x = self.pos.x
                                        move_hor = True
                              if PLAYER_OFFSET_Y1 < new_y < self.game.big_window[1] - self.res[1] + PLAYER_OFFSET_Y2 + 23:
                                        self.pos.y = new_y
                                        self.rect.y = self.pos.y
                                        move_vert = True

                    self.game.window.move(dx, dy, move_hor, move_vert)

          def draw(self):
                    if self.facing == "left":
                              image = pygame.transform.flip(self.images[int(self.frame) % len(self.images) - 1], True,
                                                            False)
                    else:
                              image = self.images[int(self.frame) % len(self.images) - 1]
                    image = pygame.transform.scale(image, PLAYER_RES)
                    self.game.display_screen.blit(image, (self.rect.x - self.game.window.offset_rect.x,
                                                          self.rect.y - self.game.window.offset_rect.y))

          def update_facing(self):
                    if self.game.correct_mouse_pos[0] < self.game.player.rect.centerx - self.game.window.offset_rect.x:
                              self.facing = "left"
                    else:
                              self.facing = "right"

          def update_velocity(self, dy, dx):
                    if dy != 0 or dx != 0:
                              if self.current_vel + self.acceleration * self.game.dt < PLAYER_VEL:
                                        self.current_vel += self.acceleration * self.game.dt
                              else:
                                        self.current_vel = PLAYER_VEL
                    else:
                              if self.current_vel - self.acceleration * self.game.dt > 0:
                                        self.current_vel -= self.acceleration * self.game.dt
                              else:
                                        self.current_vel = 0

          def update_frame(self):
                    self.frame += self.animation * self.game.dt


class BG_entities(RectEntity):
          def __init__(self, game, coordinates, res, vel=None, name=None):
                    RectEntity.__init__(self, game, coordinates, res, vel, name)
                    self.image = BG_entities_gif[random.randint(0, len(BG_entities_gif) - 1)]
                    self.rect = pygame.Rect(self.pos.x, self.pos.y, self.image.width, self.image.height)
                    self.name = name

          def blit(self):
                    self.game.display_screen.blit(self.image, (self.pos.x - self.game.window.offset_rect.x,
                                                               self.pos.y - self.game.window.offset_rect.y))


class Enemy(RectEntity, AnimatedEntity, AnimalEntity):
          def __init__(self, game, coordinates, res, vel, name, health, damage, images, angle=None,
                       animation=ANIMATION_SPEED):
                    RectEntity.__init__(self, game, coordinates, res, vel, name, angle)
                    AnimatedEntity.__init__(self, game, images, animation)
                    AnimalEntity.__init__(self, game, health, damage)
                    self.facing = "right"

          def should_move(self):
                    distance = self.distance_to_player()
                    return distance > ENEMY_STOPPING_DISTANCE

          def distance_to_player(self):
                    player_center = self.game.player.pos + v2(self.game.player.res) * 0.5
                    enemy_center = self.pos + v2(self.res) * 0.5
                    return (player_center - enemy_center).length()

          def move(self):
                    new_angle = self.calc_angle()
                    self.rotate_velocity(new_angle)
                    self.update_position()

          def rotate_velocity(self, new_angle):
                    rotate = self.angle - new_angle
                    self.vel_vector.rotate_ip(rotate)
                    self.angle = new_angle

          def update_position(self):
                    self.pos += self.vel_vector * self.game.dt
                    self.rect.topleft = self.pos

          def update_facing(self):
                    self.facing = "right" if self.game.player.pos.x > self.pos.x else "left"

          def blit(self):
                    sprite = self.get_current_sprite()
                    draw_pos = self.pos - (self.game.window.offset_rect.x, self.game.window.offset_rect.y)
                    self.game.display_screen.blit(pygame.transform.scale(sprite, ENEMY_RES), draw_pos)

          def get_current_sprite(self):
                    sprite = self.images[int(self.frame) % len(self.images)]
                    if self.facing == "left":
                              return pygame.transform.flip(sprite, True, False)
                    return sprite


class Gun:
          def __init__(self, game, gunImage, gun_res, bullet_image, distance, velocity, lifetime, fire_rate, friction=0):
                    self.game = game
                    self.res = gun_res
                    self.gunImage = gunImage
                    self.distance = distance
                    self.rect = pygame.Rect(0, 0, self.res[0], self.res[1])
                    self.facing = "right"
                    self.angle = 0
                    self.rotated_image = pygame.transform.rotate(self.gunImage, self.angle + 90)
                    self.bullet_image = bullet_image
                    self.bullet_velocity = velocity
                    self.bullet_lifetime = lifetime
                    self.bullet_friction = friction
                    self.last_shot_time = 0
                    self.fire_rate = fire_rate
                    self.continuous_fire_start = None

          def update(self):
                    self.calc_angle()
                    self.update_shooting()

          def draw(self):
                    if self.game.player.facing == "right":
                              self.rotated_image = pygame.transform.rotate(self.gunImage, self.angle + 90)
                    else:
                              self.rotated_image = pygame.transform.flip(pygame.transform.rotate(self.gunImage, -self.angle + 90), True, False)
                    pos_x = (self.game.player.rect.centerx + math.sin(math.radians(self.angle)) * self.distance -
                             self.game.window.offset_rect.x)
                    pos_y = (self.game.player.rect.centery + math.cos(math.radians(self.angle)) * self.distance -
                             self.game.window.offset_rect.y)
                    self.rect = self.rotated_image.get_rect(center=(pos_x, pos_y))
                    self.game.display_screen.blit(self.rotated_image, self.rect)

          def calc_angle(self):
                    change_in_x = (self.game.player.rect.centerx - self.game.window.offset_rect.x
                                   - self.game.correct_mouse_pos[0])
                    change_in_y = (self.game.player.rect.centery - self.game.window.offset_rect.y
                                   - self.game.correct_mouse_pos[1])
                    angle = self.angle = v2(change_in_x, change_in_y).angle_to((0, 1))
                    if angle <= 0:
                              self.angle = angle + 360
                    else:
                              self.angle = angle

          def update_shooting(self):
                    current_time = self.game.game_time
                    if self.fire_rate + self.last_shot_time < current_time and self.game.mouse_state[
                              0] and not self.game.changing_settings:
                              if self.continuous_fire_start is None:
                                        self.continuous_fire_start = current_time

                              firing_duration = current_time - self.continuous_fire_start
                              max_spread_time = 2.0
                              spread_factor = min(firing_duration / max_spread_time, 1.0)

                              self.last_shot_time = current_time

                              start_x = (self.game.player.rect.centerx + math.sin(math.radians(self.angle)) * int(
                                        self.distance - 18))
                              start_y = (self.game.player.rect.centery + math.cos(math.radians(self.angle)) * int(
                                        self.distance - 18))

                              new_bullet = Bullet(self.game, (start_x, start_y), self.angle, self.bullet_velocity,
                                                  self.bullet_image, self.bullet_lifetime, self.bullet_friction,
                                                  "Player Bullet", PLAYER_BULLET_DAMAGE, spread_factor=spread_factor)

                              for _ in range(GUN_SPARK_AMOUNT):
                                        self.game.particle_manager.sparks.add(Spark(self.game, [start_x, start_y],
                                                  math.radians(random.randint(int(270 - self.angle) - GUN_SPARK_SPREAD,
                                                            int(270 - self.angle) + GUN_SPARK_SPREAD)), random.randint(3, 6),
                                                                      GUN_SPARK_COLOUR, GUN_SPARK_SIZE))

                              self.game.bullet_manager.add_bullet(new_bullet)
                    elif self.fire_rate + self.last_shot_time + 0.5 < current_time:
                              self.continuous_fire_start = None

class Bullet(RectEntity):
          def __init__(self, game, pos, angle, velocity, image, lifetime, friction, name=PLAYER_NAME, damage=10,
                       health=1, spread_factor=0):
                    time = game.game_time
                    noise_value = perlin([time * 0.1, 0])
                    spread_angle = noise_value * PLAYER_GUN_SPREAD * spread_factor

                    final_angle = angle + spread_angle

                    self.image = pygame.transform.rotate(image, final_angle + 90)
                    RectEntity.__init__(self, game, pos, self.image.get_rect().size, velocity, name, final_angle + 180)
                    self.original_image = image
                    self.lifetime = change_random(lifetime, BULLET_LIFETIME_RANDOMNESS)
                    self.dead = False
                    self.creation_time = game.game_time
                    self.friction = friction
                    self.damage = damage
                    self.health = health
                    self.rect.center = self.pos

          def update(self):
                    if self.friction > 0:
                              self.vel_vector *= (1 - self.friction * self.game.dt)

                    self.pos += self.vel_vector * self.game.dt
                    self.rect.center = self.pos

          def check_collision(self, target):
                    if self.rect.colliderect(target.rect):
                              target.health -= self.damage
                              self.health -= 1
                              return True
                    return False
