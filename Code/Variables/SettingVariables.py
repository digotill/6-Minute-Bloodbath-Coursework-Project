from Code.Variables.ImportDependencies import *

# Initialize Pygame
pygame.init()

# Set window and rendering resolutions
WINRES = (1280, int(1280 / (pygame.display.Info().current_w / pygame.display.Info().current_h)))
RENRES = 640, int(640 / (pygame.display.Info().current_w / pygame.display.Info().current_h))
GAMESIZE = 1500, 1500

# Set up the display
DISPLAY = pygame.display.set_mode(WINRES, pygame.OPENGL | pygame.DOUBLEBUF)

# Toggle fullscreen twice (to fix a display issue)
pygame.display.toggle_fullscreen()
pygame.display.toggle_fullscreen()

# Get system information
HZ = pygame.display.get_current_refresh_rate()

# Initialize Methods class and rename files
M = Methods()
M.rename_files_recursive(r"C:\Users\digot\PycharmProjects\Survivor-Coursework-Project\Assets")
AM = LoadAssets()

# Set up mouse cursor and window properties
pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
pygame.display.set_icon(AM.assets["cover"])
pygame.display.set_caption("Survivor Game")

# General game settings
GENERAL = {
          'volume': 0.5,
          'enemies': (100, 0.2, True),  # max, spawn rate, spawning on
          'brightness': (1.5, 1.5, 70),  # max, min, paused
          'sparks': (20, 0.3, 3.5, 0.1),  # friction, width, height, min_vel
          'hash_maps': (50, 40, 16, 100, 90, 30, 60, 16),  # Enemies, Bullets, Tilemap, Rain, Objects, Particles, Effects, XP
          'cooldowns': (0.5, 0.1),  # toggle cooldowns, value checker cooldown
          'animation_speeds': (15, 20, 10, 20), }  # main menu. transition, you died

# Difficulty settings
DIFFICULTY = {"easy": (0.9, 0.8, 1), "medium": (1, 1, 1), "hard": (1.1, 5, 1)}  # enemy speed, enemy health, enemy damage

# Experience settings
EXPERIENCE = {"starting_max_xp": 100, "xp_progression_rate": 1.2, "blue": 10, "orange": 50, "green": 200, "purple": 1000, "animation_speed": 10,
              "attributes": {"speed": 200, "attraction_distance": 50, "collection_distance": 10}, "gradual_increase": 150}

# Miscellaneous settings
MISC = {"hit_effect": (20, 200), "enemy_spawns": 100, "transition_time": 1, "enviroment_density": (0.05, 16, 250), "blood_on_player_hit": 20,
        "ui_bars": (80, 30), "bullet_knockback": 1000, "xp_bar": (240, 30), "blood": 0.6, "youdied_duration": 3, "blood_effect_duration": 4}

# Camera settings
CAMERA = {'lerp_speed': 5, 'mouse_smoothing': v2(10, 10), 'window_mouse_smoothing_amount': 5, 'deadzone': 1, 'window_max_offset': 0.3,
          'shake_speed': 200, 'reduced_screen_shake': 1}

# Grass settings
GRASS = {"tile_size": 16, "shade_amount": 100, "stiffness": 300, "max_unique": 5, "vertical_place_range": (0, 1), "wind_effect": (13, 25), "density": 0.4,
         "shadow_radius": 3, "shadow_strength": 60, "shadow_shift": (1, 2),
         "Rot_Function": lambda x_val, y_val, game_time: int(math.sin(game_time * 2 + x_val / 100 + y_val / 100) * 15), "positions": {"forest_grass": [0, 1, 2, 3, 4],
                                                                                                                                      "lush_grass": [5, 6, 7, 8, 9], "spring_grass": [10, 11, 12, 13, 14], "cherryblossom_grass": [15, 16, 17, 18, 19], "wasteland_grass": [20, 21, 22, 23, 24]}}

# Player settings
PLAYER = {'health': 100, "res": (16, 16), 'vel': 90, "sprint_vel": 140, "slowed_vel": 50, 'damage': 30, 'acceleration': 200, "offset": (10, 10, -10, -10),
          'animation_speed': 10, "hit_cooldown": 0.8, 'stamina': 100, "stamina_consumption": 20, "stamina_recharge_rate": 30, "grass_force": 10, "slow_cooldown": 0.1}

# Enemy settings
ENEMIES = {"mantis": {"name": "mantis", "res": (32, 32), "health": 100, "vel": 100, "damage": 15, "attack_range": 50, "stopping_range": 25 ** 2,
                      "steering_strength": 0.4, "friction": 0.2, "animation_speed": 15, "hit_cooldown": 0, "separation_radius": 20, "separation_strength": 0.2,
                      "armour": 1, "attack_cooldown": 0.4, "xp_chances": {"blue": 0.9, "orange": 0.98, "green": 0.99, "purple": 1}, "has_shadow": True},
           "beetle": {"name": "beetle", "res": (32, 32), "health": 200, "vel": 150, "damage": 10, "attack_range": 20, "stopping_range": 25 ** 2,
                      "steering_strength": 0.4, "friction": 0.2, "animation_speed": 15, "hit_cooldown": 0, "separation_radius": 30, "separation_strength": 0.2,
                      "armour": 2, "attack_cooldown": 0.4, "xp_chances": {"blue": 0.9, "orange": 0.95, "green": 0.99, "purple": 1}, "has_shadow": False}
           }

# Effect settings
EFFECTS = {"blood": {"name": "blood", "res": (48, 48), "speed": (800, 30), "direction": 20, "animation_speed": 40, "vanish_time": (1, 1.5), "variety": 10}, }

# Screen shake settings
SHAKE = {"ak47": (5, 0.1), "shotgun": (25, 0.1), "minigun": (5, 0.1), "hit": (20, 0.5)}  # magnitude, duration

# Spark effect settings
SPARKS = {"muzzle_flash": {"spread": 20, "scale": 0.8, "colour": (255, 255, 255), "amount": 10, "min_vel": 3, "max_vel": 10}}

# Map generation settings
MAP = {"biomes_map": (0.004, 1), "biomes_density_map": (0.05, 4), "tiles_map": (0.2, 1), "gun_shake_map": (0.1, 2), "camera_shake_map": (0.1, 3)}

# Biome settings
BIOMES = {"wasteland": (0.35, 2, 0.5), "spring": (0.45, 1, 0.5), "forest": (0.55, 1, 0.5), "lush": (0.6, 1, 1),
          "cherryblossom": (1, 1, 0.5), }  # chance of biome spawning, tree density, padding density

# Tile settings
TILES = {"Tile_Ranges": {"water_tile": -0.1, "grass_tile": 1}, "transitions": [["grass_tile", "water_tile"]], "animation_speed": 5, "animated_tiles": [], }

# Rain effect settings
RAIN = {"spawn_rate": 0.1, "amount_spawning": 5, "animation_speed": 30, "angle": 40, "vel": (800, 50), "lifetime": (0.5, 0.8)}

# Weapon settings
WEAPONS = {
          "ak47": {"vel": 750, "spread": 3, "fire_rate": 0.1, "lifetime": 3, "lifetime_randomness": 0.2, "damage": 50, "distance": -2, "friction": 0.1,
                   "spread_time": 2, "pierce": 2, "shots": 1, "name": "ak47"},
          "shotgun": {"vel": 900, "spread": 15, "fire_rate": 0.8, "lifetime": 0.5, "lifetime_randomness": 0.2, "damage": 50, "distance": -2, "friction": 0.1,
                      "spread_time": 2, "pierce": 2, "shots": 10, "name": "shotgun"},
          "minigun": {"vel": 600, "spread": 5, "fire_rate": 0.01, "lifetime": 2, "lifetime_randomness": 0.2, "damage": 5, "distance": -12, "friction": 0.1,
                      "spread_time": 0.2, "pierce": 1, "shots": 1, "name": "minigun"}
}

# Button settings for various game states
BUTTONS = {
          "In_Game_Buttons": {"resume": M.create_button("resume", v2(320, 135), AM.assets["button5"]),
                              "fullscreen": M.create_button("fullscreen", v2(580, 90), AM.assets["button5"], {"axis": "x", "axisl": "max"}),
                              "quit": M.create_button("quit", v2(320, 180), AM.assets["button5"]),
                              "return": M.create_button("return", v2(320, 90), AM.assets["button5"]), },
          "Weapon_Buttons": {"ak47": M.create_button("ak47", v2(600, 240), M.get_image_outline(AM.assets["ak47"]), {"text_pos": "left", "on": True, "active": True, "axisl": "max", "axis": "x"}),
                             "shotgun": M.create_button("shotgun", v2(600, 200), M.get_image_outline(AM.assets["shotgun"]), {"text_pos": "left", "active": True, "axisl": "max", "axis": "x"}),
                             "minigun": M.create_button("minigun", v2(600, 160), M.get_image_outline(AM.assets["minigun"]), {"text_pos": "left", "active": True, "axisl": "max", "axis": "x"}), },
          "Menu_Buttons": {"play": M.create_button("play", v2(280, 180), AM.assets["button5"], {"active": True}),
                           "quit": M.create_button("quit", v2(360, 180), AM.assets["button5"], {"active": True}),
                           "easy": M.create_button("easy", v2(220, 30), AM.assets["button5"], {"active": True, "axisl": "min"}),
                           "medium": M.create_button("medium", v2(320, 30), AM.assets["button5"], {"on": True, "active": True, "axisl": "min"}),
                           "hard": M.create_button("hard", v2(420, 30), AM.assets["button5"], {"active": True, "axisl": "min"})},
          "Sliders": {"brightness": M.create_slider(v2(60, 225), "brightness:  ", 0, 100, 50, AM.assets["button7"], {"axis": "x", "axisl": "min"}),
                      "fps": M.create_slider(v2(60, 180), "max fps:  ", 20, 240, HZ, AM.assets["button7"], {"axis": "x", "axisl": "min"}),
                      "shake": M.create_slider(v2(60, 135), "reduced shake:  ", 0, 100, 100, AM.assets["button7"], {"axis": "x", "axisl": "min"}),
                      "colour": M.create_slider(v2(60, 90), "colour mode:  ", 1, 100, 50, AM.assets["button7"], {"axis": "x", "axisl": "min"}),
                      "volume": M.create_slider(v2(60, 315), "sound volume:  ", 0, 100, 50, AM.assets["button7"], {"axis": "x", "axisl": "min"}),
                      "text_size": M.create_slider(v2(60, 270), "text size:  ", 100, 150, 100, AM.assets["button7"], {"axis": "x", "axisl": "min"})},
          "End_Screen_Buttons": {"restart": M.create_button("restart", v2(240, 270), AM.assets["button8"], {"axis": "y", "axisl": "max", "res": (92, 30)}),
                                 "quit": M.create_button("quit", v2(400, 270), AM.assets["button8"], {"axis": "y", "axisl": "max", "res": (92, 30)})},
          "XP_bar": M.create_button("", v2(320, 30), AM.assets["xp_bar_uncoloured"], {"text_pos": "top", "active": True, "hover_slide": True, "res": AM.assets["xp_bar_uncoloured"].size, "distance_factor": 0.1})
}
