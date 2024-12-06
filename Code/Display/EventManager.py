import time
from Code.Variables.Variables import *


class EventManager:
          def __init__(self, game):
                    self.game = game
                    self.Last_Fullscreen = 0
                    self.Last_FPS_Toggle = 0
                    self.Last_Changing_settings = 0
                    self.Fullscreen_Toggled = START_FULLSCREEN
                    self.Fullscreen_Cooldown = cooldowns['fullscreen']
                    self.FPS_Cooldown = cooldowns['fps']
                    self.Changing_settings_Cooldown = cooldowns['settings']

          def update_window_events(self):
                    for event in pygame.event.get():
                              if event.type == pygame.QUIT or self.game.keys[keys['escape']]: self.game.running = False

          def update_size(self, always_toggle=False):
                    if self.game.keys[keys[
                              'fullscreen']] and self.Last_Fullscreen + self.Fullscreen_Cooldown < pygame.time.get_ticks() / 1000 or always_toggle:
                              self.Fullscreen_Toggled = not self.Fullscreen_Toggled
                              if self.Fullscreen_Toggled:
                                        pygame.display.set_window_position((0, 0))
                                        self.game.display = pygame.display.set_mode(MAX_WIN_RES,
                                                                                    pygame.NOFRAME | pygame.DOUBLEBUF)
                              else:
                                        pygame.display.set_window_position((MONITER_RES[0] / 2 - MIN_WIN_RES[0] / 2,
                                                                            MONITER_RES[1] / 2 - MIN_WIN_RES[1] / 2))
                                        self.game.display = pygame.display.set_mode(MIN_WIN_RES,
                                                                                    pygame.RESIZABLE | pygame.DOUBLEBUF)
                              self.Last_Fullscreen = pygame.time.get_ticks() / 1000

          def update_fps_toggle(self):
                    if self.game.keys[keys[
                              'fps']] and self.Last_FPS_Toggle + self.FPS_Cooldown < pygame.time.get_ticks() / 1000:
                              self.game.ui.fps_enabled = not self.game.ui.fps_enabled
                              self.Last_FPS_Toggle = pygame.time.get_ticks() / 1000

          def update_grab(self):
                    if self.game.mouse_state[0] and not self.game.changing_settings:
                              pygame.event.set_grab(True)
                    elif self.game.keys[keys['ungrab']]:
                              pygame.event.set_grab(False)

          def update_changing_settings(self):
                    if self.game.keys[keys[
                              'ungrab']] and self.Last_Changing_settings + self.Changing_settings_Cooldown < pygame.time.get_ticks() / 1000 and not self.game.mainmenu.in_menu:
                              self.game.changing_settings = not self.game.changing_settings
                              self.Last_Changing_settings = pygame.time.get_ticks() / 1000
