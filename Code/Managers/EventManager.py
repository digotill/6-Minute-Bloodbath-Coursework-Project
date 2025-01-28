from Code.Variables.SettingsVariables import *


class EventManager:
          def __init__(self, game):
                    self.game = game

                    current_time = self.game.ticks

                    self.fullscreen_timer = Timer(GENERAL['cooldowns'][0], current_time)  # Timer for fullscreen toggle
                    self.fps_timer = Timer(GENERAL['cooldowns'][0], current_time)  # Timer for FPS display toggle
                    self.settings_timer = Timer(GENERAL['cooldowns'][0], current_time)  # Timer for settings menu toggle

          def handle_quitting(self):
                    for event in pygame.event.get():
                              if event.type == pygame.QUIT or self.game.keys[KEYS['escape']]:  # Check for quit events
                                        self.game.running = False

          def toggle_fullscreen(self):
                    current_time = self.game.ticks
                    if self.game.keys[KEYS['fullscreen']] and self.fullscreen_timer.check(current_time):  # Toggle fullscreen
                              pygame.display.toggle_fullscreen()
                              self.fullscreen_timer.reactivate(current_time)

          def toggle_grab(self):
                    if self.game.mouse_state[0] and not self.game.changing_settings and not self.game.in_menu:  # Grab mouse
                              pygame.event.set_grab(True)
                    elif self.game.keys[KEYS['ungrab']] or self.game.in_menu:  # Release mouse grab
                              pygame.event.set_grab(False)
                    if self.game.died:  # Release mouse if player died
                              pygame.event.set_grab(False)

          def toggle_fps(self):
                    current_time = self.game.ticks
                    if self.game.keys[KEYS['fps']] and self.fps_timer.check(current_time) and not self.game.in_menu:  # Toggle FPS display
                              self.game.ui_manager.fps_enabled = not self.game.ui_manager.fps_enabled
                              self.fps_timer.reactivate(current_time)

          def toggle_settings(self):
                    current_time = self.game.ticks
                    if self.game.keys[KEYS['ungrab']] and self.settings_timer.check(current_time) and not self.game.in_menu and not self.game.died:  # Toggle settings menu
                              self.game.changing_settings = not self.game.changing_settings
                              self.settings_timer.reactivate(current_time)

          def handle_events(self):
                    self.handle_quitting()  # Check for quit events
                    self.toggle_grab()  # Manage mouse grabbing
                    self.toggle_fullscreen()  # Handle fullscreen toggling
                    self.toggle_settings()  # Manage settings menu access
                    self.toggle_fps()  # Toggle FPS display
