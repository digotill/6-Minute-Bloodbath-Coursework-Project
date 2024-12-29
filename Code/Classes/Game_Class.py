from Code.Classes.Managers import *
from Code.Display.EventManager import *
from Code.Display.Menu import *
from Code.Display.UIManager import *
from Code.Display.Camera import *
from Code.Classes.TileMap import TileMap
from Code.Classes.GrassManager import *
import pygame_shaders
import moderngl



class Game:
          def __init__(self):
                    pygame.init()

                    self.display = Display
                    self.display_screen = pygame.Surface(REN_RES).convert()
                    self.shader = pygame_shaders.Shader(pygame_shaders.DEFAULT_VERTEX_SHADER,
                                                   pygame_shaders.DEFAULT_FRAGMENT_SHADER, self.display_screen)

                    self.ui_surface = pygame.Surface(REN_RES).convert()
                    self.ui_surface.set_colorkey((0, 0, 0))
                    self.clock = pygame.time.Clock()

                    self.running = True
                    self.game_time = 0
                    self.fps = AllButtons["Sliders"]["fps"]["value"]
                    self.changing_settings = False
                    self.immidiate_quit = False
                    self.in_menu = True
                    self.restart = False
                    self.stats = pd.DataFrame(columns=['Coins', 'Score', 'Enemies Killed', 'Difficulty'])
                    self.x_window_ratio = REN_RES[0] / self.display.width
                    self.y_window_ratio = REN_RES[1] / self.display.height

                    self.event_manager = EventManager(self)
                    self.enemy_manager = EnemyManager(self)
                    self.particle_manager = ParticleManager(self)
                    self.object_manager = ObjectManager(self)
                    self.bullet_manager = BulletManager(self)
                    self.button_manager = ButtonManager(self)
                    self.sound_manager = SoundManager(self)
                    self.grass_manager = GrassManager(self)
                    self.rain_manager = RainManager(self)
                    self.ui_manager = UIManager(self)

                    self.tilemap = TileMap(self)
                    self.object_manager.generate_objects()

                    self.update_game_variables()

                    self.mainmenu = MainMenu(self)
                    MainMenu(self).loop()
                    self.camera = Camera(self)


          def refresh(self):
                    pygame.display.flip()
                    self.__init__()
                    self.run_game()

          def update_groups(self):
                    if not self.changing_settings:
                              self.enemy_manager.update()
                              self.particle_manager.update()
                              self.bullet_manager.update()
                              self.rain_manager.update()
                    self.player.update()
                    self.player.gun.update()
                    self.button_manager.update()

          def draw_groups(self):
                    self.tilemap.draw()

                    self.grass_manager.draw()
                    self.object_manager.draw()
                    self.player.draw()
                    self.enemy_manager.draw()

                    self.bullet_manager.draw()
                    self.particle_manager.draw()
                    self.rain_manager.draw()

                    self.ui_manager.darken_screen()
                    self.ui_manager.draw_bars()
                    self.ui_manager.draw_fps()
                    self.ui_manager.draw_time()

                    self.button_manager.draw()

          def update_display(self):
                              self.ui_manager.display_mouse()
                              self.display_screen.blit(self.ui_surface, (0, 0))
                              self.ui_surface.fill((0, 0, 0, 0))
                              self.ui_manager.draw_brightness()
                              self.shader.render_direct(pygame.Rect(0, 0, self.display.get_width(),
                                                                    self.display.get_height()))
                              pygame.display.flip()

          def manage_events(self):
                    self.event_manager.handle_quitting()
                    self.event_manager.update_grab()
                    self.event_manager.fullscreen_toggle()
                    if not self.in_menu:
                              self.event_manager.update_changing_settings()
                              self.event_manager.update_fps_toggle()

          def update_game_variables(self):
                    self.keys = pygame.key.get_pressed()
                    self.mouse_pos = pygame.mouse.get_pos()
                    self.correct_mouse_pos = (int(self.mouse_pos[0] * self.x_window_ratio),
                                              int(self.mouse_pos[1] * self.y_window_ratio))
                    self.mouse_state = pygame.mouse.get_pressed()
                    if self.clock.get_fps() != 0: self.dt = 1 / self.clock.get_fps()
                    else: self.dt = 0
                    if not self.changing_settings:
                              self.game_time += self.dt

          def run_game(self):
                    while self.running:
                              self.clock.tick_busy_loop(self.fps)
                              self.update_game_variables()
                              self.manage_events()
                              self.update_groups()
                              self.draw_groups()
                              self.update_display()
                              if self.restart: self.refresh()
                              elif self.immidiate_quit: return None
