import pygame, random
from perlin_noise import PerlinNoise
pygame.init()

START_FULLSCREEN = False
MONITER_RES = pygame.display.Info().current_w, pygame.display.Info().current_h
MIN_WIN_RES = 1280, 720
MAX_WIN_RES = 2560, 1440
if START_FULLSCREEN: WIN_RES = MONITER_RES
else: WIN_RES = MIN_WIN_RES
PLAYABLE_AREA_SIZE = 3840, 2160
REN_RES = 480, 270

PLAYER_RES = 32, 32
PLAYER_VEL = 200
PLAYER_DAMAGE = 30
PLAYER_HEALTH = 100
PLAYER_STAMINA = 100
PLAYER_ACCELERATION = 600

PLAYER_OFFSET_X1, PLAYER_OFFSET_X2 = 50, - 50
PLAYER_OFFSET_Y1, PLAYER_OFFSET_Y2 = 50, - 50

AK47_RES = 32, 32
AK47_VEL = 700
AK47_SPREAD = 3
AK47_RELOAD_TIME = 2
AK47_FIRE_RATE = 0.1
AK47_CLIP_SIZE = 30
AK47_LIFETIME = 3
AK47_LIFETIME_RANDOMNESS = 0.2
AK47_DAMAGE_DROP_OFF = 2
AK47_DAMAGE = 30
AK47_DISTANCE = - 2

SHOTGUN_RES = 32, 32
SHOTGUN_VEL = 700
SHOTGUN_SPREAD = 15
SHOTGUN_RELOAD_TIME = 1.5
SHOTGUN_FIRE_RATE = 0.8
SHOTGUN_CLIP_SIZE = 8
SHOTGUN_LIFETIME = 0.5
SHOTGUN_LIFETIME_RANDOMNESS = 0.2
SHOTGUN_DAMAGE_DROP_OFF = 5
SHOTGUN_DAMAGE = 50
SHOTGUN_DISTANCE = -2

MINIGUN_RES = 32, 32
MINIGUN_VEL = 800
MINIGUN_SPREAD = 5
MINIGUN_RELOAD_TIME = 4
MINIGUN_FIRE_RATE = 0.05
MINIGUN_CLIP_SIZE = 100
MINIGUN_LIFETIME = 2
MINIGUN_LIFETIME_RANDOMNESS = 0.2
MINIGUN_DAMAGE_DROP_OFF = 1
MINIGUN_DAMAGE = 15
MINIGUN_DISTANCE = -2

PLAYER_GUN_DISTANCE = -2
PLAYER_GUN_RES = 20, 20
PLAYER_GUN_SPREAD = 5
PLAYER_BULLET_RES = 24, 24
PLAYER_BULLET_FRICTION = 2
PLAYER_BULLET_DAMAGE = 20
PLAYER_BULLET_LIFETIME = 0.8
BULLET_LIFETIME_RANDOMNESS = 0.2
PLAYER_BULLET_SPEED = 700
PLAYER_BULLET_RATE = 0.1
PLAYER_BULLET_ANIMATION = 15
PLAYER_NAME = "Player"

ENEMY_RES = 32, 36
ENEMY_VEL = 250
ENEMY_DAMAGE = 20
ENEMY_HEALTH = 100
ENEMY_SPAWN_RATE = 5
ENEMY_BULLET_RES = 10, 10
ENEMY_BULLET_DAMAGE = 10
ENEMY_BULLET_LIFETIME = 1000
ENEMY_BULLET_SPEED = 700
ENEMY_STOPPING_DISTANCE = 25
ENEMY_NAME = "Enemy"
ENEMY_SCREEN_SHAKE_DURATION = 0.5
ENEMY_SCREEN_SHAKE_MAGNITUDE = 10
MAX_ENEMIES = 50

BG_ENTITIES_DENSITY = 90
BG_ENTITIES_RES = 24, 19

ANIMATION_SPEED = 5
SPATIAL_GRID_SIZE = 100
BG_COLOUR = (22, 22, 24)
BUTTONS_SIZE = 1.1
FONT = "Assets\\Font\\font2.ttf"
MOUSE_RES = 13, 13
BORDER_ANIMATION_SPEED = 10

WINDOW_MAX_OFFSET = 0.3
WINDOW_LERP_SPEED = 0.05
WINDOW_DEADZONE = 3
WINDOW_SHAKE_SPEED = 200
WINDOW_MOUSE_SMOOTHING = 10, 10
WINDOW_SHAKE_DIRECTIONS = 1, 1

PLAY_BUTTON_NAME = "Play"
PLAY_BUTTON_POS = 240, 80
PLAY_BUTTON_BASE_COLOUR = "black"
PLAY_BUTTON_HOVERING_COLOUR = "blue"
PLAY_BUTTON_RES = 46, 15

OPTIONS_BUTTON_NAME = "Options"
OPTIONS_BUTTON_POS = 240, 160
OPTIONS_BUTTON_BASE_COLOUR = "black"
OPTIONS_BUTTON_HOVERING_COLOUR = "blue"

QUIT_BUTTON_NAME = "Quit"
QUIT_BUTTON_POS = 240, 240
QUIT_BUTTON_BASE_COLOUR = "black"
QUIT_BUTTON_HOVERING_COLOUR = "blue"
QUIT_BUTTON_RES = 46, 15

SETTINGS_BUTTON_SPEED = 900
SETTINGS_BUTTON_FRICTION = 300

HEALTH_BAR_POS = 135, 95
STAMINA_BAR_POS = 170, 95

FPS_POS = 150, 74
TIME_POS = 150, 74
FPS_AND_TIME_SIZE = 15

FULLSCREEN_KEY = pygame.K_F11
TOGGLE_FPS_KEY = pygame.K_F12
ESCAPE_KEY = pygame.K_F10
UNGRAB_KEY = pygame.K_ESCAPE

START_WITH_FPS_AND_TIME = False
FPS_AND_TIME_COOLDOWN = 0.5
FULLSCREEN_COOLDOWN = 0.5
CHANGING_SETTINGS_COOLDOWN = 0.5

PERLIN_OCTAVES = 3
PERLIN_SEED = random.randint(0, 100000)
perlin = PerlinNoise(octaves=PERLIN_OCTAVES, seed=PERLIN_SEED)
