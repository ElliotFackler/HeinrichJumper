import pygame
from sys import exit
from random import randint, choice




# Skapad av Elliot Fackler
# Heinrich är en riddare vem kommer från Tyskland.
# Han går till Jerusalem för Popen.
# Fiender: Fiende, Fiende Soldater, och Cannon Balls

# King of his kingdom: "Heinrich, I have been called on by the Pope to join the 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
        self.player_crouch = pygame.image.load("graphics/player/player_crouch.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
        if keys[pygame.K_DOWN]:
            self.jump_sound.play()
            self.gravity = 10

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    def animation_state(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.image = self.player_crouch
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'cannonball':
            cannonball_1 = pygame.image.load('graphics/cannonball/cannonball1.png').convert_alpha()
            cannonball_2 = pygame.image.load('graphics/cannonball/cannonball2.png').convert_alpha()
            self.frames = [cannonball_1, cannonball_2]
            y_pos = 210
        elif type == 'fiendesoldat':
            fiendesoldat_1 =  pygame.image.load('graphics/fiendesoldat/fiendesoldat1.png').convert_alpha()
            fiendesoldat_2 = pygame.image.load('graphics/fiendesoldat/fiendesoldat2.png').convert_alpha()
            self.frames = [fiendesoldat_1, fiendesoldat_2]
            y_pos = 300
        else:
            fiende_1 = pygame.image.load('graphics/Snail/snail1.png').convert_alpha()
            fiende_2 = pygame.image.load('graphics/Snail/snail2.png').convert_alpha()
            self.frames = [fiende_1, fiende_2]
            y_pos = 300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    time_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    time_rect = time_surf.get_rect(center=(300, 50))
    screen.blit(time_surf, time_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if(obstacle_rect.bottom == 300):
                screen.blit(fiende_surf, obstacle_rect)
            else:
                screen.blit(cannonball_surf, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x >-100]
        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True


def player_animation():
    global player_surf, player_index
    if(player_rect.bottom < 300):
        player_surf = player_jump
    else:
        player_index += 0.1
        if(player_index >= len(player_walk)): player_index = 0
        player_surf = player_walk[int(player_index)]


# Set variables.
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Adventures of Heinrich')
pygame_icon = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
pygame.display.set_icon(pygame_icon)
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_Music = pygame.mixer.Sound('audio/music.wav')
bg_Music.play()
bg_Music.set_volume(0.5)
bg_Music.play(loops = -1)

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()



# SPELARE SURFACES
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
player_crouch = pygame.image.load('graphics/player/player_crouch.png').convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 300))

# FIENDE SURFACES
fiende_surface1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
fiende_surface2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
cannonball_surf1 = pygame.image.load('graphics/cannonball/cannonball1.png').convert_alpha()
cannonball_surf2 = pygame.image.load('graphics/cannonball/cannonball2.png').convert_alpha()
fiendesoldat_surf1 = pygame.image.load('graphics/fiendesoldat/fiendesoldat1.png').convert_alpha()
fiendesoldat_surf2 = pygame.image.load('graphics/fiendesoldat/fiendesoldat2.png').convert_alpha()

fiende_frame_index = 0
cannonball_frame_index = 0
fiendesoldat_frame_index = 0

fiende_frames = [fiende_surface2, fiende_surface1]
cannonball_frames = [cannonball_surf2, cannonball_surf1]
fiendesoldat_frames = [fiendesoldat_surf2, fiendesoldat_surf1]

cannonball_surf = cannonball_frames[cannonball_frame_index]
fiende_surf = fiende_frames[fiende_frame_index]
fiendesoldat_surf = fiendesoldat_frames[fiendesoldat_frame_index]

obstacle_rect_list = []


# DISPLAY SURFACES
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

player_gravity = 0
game_name = test_font.render('Adventures of Heinrich', False, (64, 64, 64))
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = test_font.render('Press Space To Run', False, (64, 64, 64))
game_message_rect = game_message.get_rect(center=(400, 340))

player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

fiende_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fiende_animation_timer, 500)

cannonball_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(cannonball_animation_timer, 500)

fiendesoldat_animation_timer = pygame.USEREVENT + 4
pygame.time.set_timer(fiendesoldat_animation_timer, 500)

# WHILE LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.bottom == 300:
                    if player_rect.collidepoint(event.pos):
                        player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if player_rect.bottom == 300:
                    if event.key == pygame.K_SPACE:
                        player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                #snail_rect.left = 800
                start_time = int(pygame.time.get_ticks()/1000)

        if event.type == obstacle_timer and game_active and score < 20:
            obstacle_group.add(Obstacle(choice(['cannonball', 'snail', 'snail', 'snail'])))
        elif event.type == obstacle_timer and game_active and  score >= 20:
            obstacle_group.add(Obstacle(choice(['cannonball', 'snail', 'snail', 'snail', 'fiendesoldat'])))

        if event.type == fiende_animation_timer:
            if fiende_frame_index == 0: fiende_frame_index = 1
            else: fiende_frame_index = 0
            fiende_surf = fiende_frames[fiende_frame_index]
        if event.type == cannonball_animation_timer:
            if cannonball_frame_index == 0: cannonball_frame_index = 1
            else: cannonball_frame_index = 0
        if event.type == fiendesoldat_animation_timer:
            if fiendesoldat_frame_index == 0: fiendesoldat_frame_index = 1
            else: fiendesoldat_frame_index = 0


    if game_active:
        # BAKGRUND
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()







        # SPELARE UPDATE
        player.draw(screen)
        player.update()
        # FIENDE UPDATE
        obstacle_group.draw(screen)
        obstacle_group.update()
        # COLLISIONS
        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_gravity = 0
        player_rect.midbottom = (80, 300)
        score_message = test_font.render(f'Your score: {score}',False,(64,64,64))
        score_message_rect = score_message.get_rect(center = (400, 330))
        screen.blit(game_name, game_name_rect)
        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)

    # UPDATE
    pygame.display.update()
    clock.tick(60)
