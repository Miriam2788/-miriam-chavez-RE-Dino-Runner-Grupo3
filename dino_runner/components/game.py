import pygame
from dino_runner.components import text_utils
from dino_runner.components.dinosour import Dinosour
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, RUNNING, Sounds
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.player_hearts.player_heart_manager import PlayerHeartManager

pygame.mixer.init()
class Game:
    def __init__(self) :
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosour()
        self.player_heart_manager = PlayerHeartManager()

        self.obstacle_manager = ObstacleManager()
        self.points = 0
        self.running = True
        self.death_count = 0
        self.power_up_manager = PowerUpManager()

    def run(self):
        self.create_components()
        self.obstacle_manager.reset_obstacles(self)
        self.player_heart_manager.reduce_heart()
        self.playing = True
        while self.playing == True:
            self.events()
            self.update()
            self.draw()
    def create_components(self):
        self.points = 0
        self.game_speed = 20
        self.player_heart_manager.heart_count = 4
    
    def execute(self):
        while self.running:
            if not self.playing:
                self.show_menu()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
        self.screen.fill((0,0,0))

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.points, self.game_speed, self.player)
        


    def draw(self):
        self.score()##mostrar El Score en la pantalla
        self.clock.tick(FPS)
        self.power_up_manager.draw(self.screen)
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.player_heart_manager.draw(self.screen)

        pygame.display.update()
        pygame.display.flip()


    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg ))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg ))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
    
    def score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed += 1
        text, text_rect = text_utils.get_score_element(self.points)
        self.screen.blit(text, text_rect)
        self.player.check_invicibility(self.screen)



    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                self.run()


    def print_menu_elements(self):
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            text,text_rect = text_utils.get_centred_message("press any key to start")
            self.screen.blit(text, text_rect)
        elif self.death_count > 0 :
            text,text_rect = text_utils.get_centred_message("press any key to Restart")
            ##aqui ocupo hacer esto
            score, score_rect = text_utils.get_centred_message("Your score:" +str(self.points), height=half_screen_height + 50)
            death, death_rect = text_utils.get_centred_message("Death count:" +str(self.death_count), height=half_screen_height + 80)

            self.screen.blit (score, score_rect)
            self.screen.blit ( text, text_rect)
            self.screen.blit (death, death_rect)
            Sounds[2].play()
        self.screen.blit(RUNNING[0],(half_screen_width-20, half_screen_height-140))
        

    def show_menu(self):
        self.running = True

        white_color = (18, 116, 165 )
        self.screen.fill(white_color)
        self.print_menu_elements()
        pygame.display.update()
        self.handle_key_events_on_menu()