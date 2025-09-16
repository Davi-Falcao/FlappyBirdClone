import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 640))
    screen.blit(floor_surface, (floor_x_pos + 400, 640))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (600, random_pipe_pos -50))
    top_pipe = pipe_surface.get_rect(midbottom = (600, random_pipe_pos -400))
    
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    
    return visible_pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 720:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False, True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    global can_score
    resultado = True
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            resultado = False

    if bird_rect.top <= -150 or bird_rect.bottom >= 720:
        can_score = True
        resultado = False

    return resultado

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement *3,1)
    
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    #Atualiza animacao do passaro
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    
    return new_bird, new_bird_rect

def score_display(game_state):
    #Atualiza tela durante o jogo
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (83,53,69))
        score_rect = score_surface.get_rect(center = (250, 100))
        screen.blit(score_surface, score_rect)

        score_surface_black = game_font.render(str(int(score)), True, (250,250,250))
        score_rect_black = score_surface_black.get_rect(center=(245, 95))
        screen.blit(score_surface_black, score_rect_black)

    #Atualiza tela quando morre
    if game_state == 'game_over':

        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(250, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(250, 250))
        screen.blit(high_score_surface, high_score_rect)

        Davi_surface = game_font.render(f'by Davi', True, (83,53,69))
        Davi_rect = Davi_surface.get_rect(center=(415, 535))
        screen.blit(Davi_surface, Davi_rect)

        Davi_surface_black= game_font.render(f'by Davi', True, (250,250,250))
        Davi_rect_black = Davi_surface_black.get_rect(center=(422, 532))
        screen.blit(Davi_surface_black, Davi_rect_black)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

#Atualiza a pontuacao a cada cano passado
def pipe_score_check():
    global score,can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True

#Definindo tamanho da tela
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 720

pygame.init()
pygame.display.set_caption("Flappy Bird")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
game_font = pygame.font.Font('Data/04B_19.TTF', 40)

#Variaveis do jogo
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

#Adicionando imagens ao jogo

bg_surface = pygame.image.load('Data/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))

floor_surface = pygame.image.load('Data/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

#Variaveis do passaro
bird_downflap = pygame.transform.scale2x(pygame.image.load('Data/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('Data/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('Data/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 360))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

#Variaveis do cano
pipe_surface = pygame.image.load('Data/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

#Imagens Game Over
game_over_surface = pygame.image.load('Data/message.png').convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center = (250, 360))

#Sons do jogo
flap_sound = pygame.mixer.Sound('Data/sfx_wing.wav')
death_sound = pygame.mixer.Sound('Data/sfx_die.wav')
score_sound = pygame.mixer.Sound('Data/sfx_point.wav')
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        #Fecha o jogo
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #Atualiza o movimento do passaro com o espaco 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                bird_movement = 0
                bird_movement -= 10
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,360)
                bird_movement = 0
                score = 0
        
        #Cria canos
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        #Passaro batendo as asas
        if event.type == BIRDFLAP:
            if bird_index < 2:
                 bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()
    
    screen.blit(bg_surface,(0,0))

    if game_active:
        #Movimento do passaro
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        #Cano
        pipe_list = move_pipes(pipe_list)
        draw_pipe(pipe_list)

        #Score
        pipe_score_check()
        score_display('main_game')

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    #Chao
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -400:
        floor_x_pos = 0


    pygame.display.update()
    clock.tick(120)
