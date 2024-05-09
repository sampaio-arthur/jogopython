import pygame
import sys
import math

# Inicialização do Pygame
pygame.init()

# Definição das cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Definição das configurações da tela
WIDTH = 800
HEIGHT = 600
FPS = 60

# Definição das configurações do papel e da lata de lixo
PAPER_RADIUS = 20
TRASHCAN_WIDTH = 300
TRASHCAN_HEIGHT = 150
TRASHCAN_TOP_HEIGHT = 50  # Altura da tampa da lata de lixo

# Definição das configurações iniciais
score = 0

# Configuração da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trashcan Game")
clock = pygame.time.Clock()

# Carregar e redimensionar as imagens
background_image = pygame.image.load('G:/Meu Drive/estudos pc drive/ufsc/inf na educ/jogo/escola.jpg').convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

trashcan_image = pygame.image.load('G:/Meu Drive/estudos pc drive/ufsc/inf na educ/jogo/lixo3.png').convert_alpha()
trashcan_image = pygame.transform.scale(trashcan_image, (TRASHCAN_WIDTH, TRASHCAN_HEIGHT))
trashcan_rect = trashcan_image.get_rect(center=(WIDTH/2, HEIGHT - TRASHCAN_HEIGHT/2 - 50))
trashcan_top_rect = pygame.Rect(trashcan_rect.left, trashcan_rect.top, trashcan_rect.width, TRASHCAN_TOP_HEIGHT)

paper_image = pygame.image.load('G:/Meu Drive/estudos pc drive/ufsc/inf na educ/jogo/papel3.png').convert_alpha()
paper_image = pygame.transform.scale(paper_image, (PAPER_RADIUS*2.5, PAPER_RADIUS*2.5))

# Função para desenhar a lata de lixo
def draw_trashcan():
    screen.blit(trashcan_image, trashcan_rect)

# Função para desenhar o papel
def draw_paper(paper_pos):
    screen.blit(paper_image, (int(paper_pos[0] - PAPER_RADIUS), int(paper_pos[1] - PAPER_RADIUS)))

# Função para desenhar a pontuação
def draw_score():
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), 1, BLACK)
    screen.blit(text, (WIDTH - 120, 10))

# Função para desenhar o botão iniciar
def draw_start_button():
    font = pygame.font.Font(None, 50)
    text = font.render("Iniciar", 1, WHITE)
    pygame.draw.rect(screen, BLACK, (WIDTH/2 - 100, HEIGHT/2 - 50, 200, 100))
    screen.blit(text, (WIDTH/2 - 50, HEIGHT/2 - 25))

# Função para desenhar a linha de mira
def draw_aim_line(start_pos, end_pos):
    dx = start_pos[0] - end_pos[0]
    dy = start_pos[1] - end_pos[1]
    distance = math.sqrt(dx**2 + dy**2)
    if distance > 0:
        for i in range(0, int(distance), 10):
            x = start_pos[0] - dx * i / distance
            y = start_pos[1] - dy * i / distance
            pygame.draw.circle(screen, BLACK, (int(x), int(y)), 2)

# Função para desenhar a mensagem de parabéns
def draw_congratulations():
    font = pygame.font.Font(None, 50)
    text = font.render("Parabéns, você fez o seu papel de cidadão!", 1, BLACK)
    pygame.draw.rect(screen, WHITE, (WIDTH/2 - text.get_width() // 2 - 10, HEIGHT/2 - text.get_height() // 2 - 10, text.get_width() + 20, text.get_height() + 20))
    screen.blit(text, (WIDTH/2 - text.get_width() // 2, HEIGHT/2 - text.get_height() // 2))

# Função principal do jogo
def game():
    global score
    
    paper_pos = [50, 50]
    paper_vel = [0, 0]
    mouse_pos = paper_pos.copy()

    running = True
    game_started = False
    mouse_down = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not game_started and WIDTH/2 - 100 < mouse_pos[0] < WIDTH/2 + 100 and HEIGHT/2 - 50 < mouse_pos[1] < HEIGHT/2 + 50:
                    game_started = True
                elif game_started:
                    mouse_down = True

            if event.type == pygame.MOUSEBUTTONUP:
                if game_started and mouse_down:
                    # Calcula a velocidade do papel em direção ao cursor
                    dx = mouse_pos[0] - paper_pos[0]
                    dy = mouse_pos[1] - paper_pos[1]
                    vel = math.sqrt(dx**2 + dy**2)
                    paper_vel = [dx/vel, dy/vel]
                    mouse_down = False

        if mouse_down:
            mouse_pos = pygame.mouse.get_pos()

        paper_pos[0] += paper_vel[0] * 5
        paper_pos[1] += paper_vel[1] * 5

        if game_started and paper_pos[0] > trashcan_top_rect.left - PAPER_RADIUS and paper_pos[0] < trashcan_top_rect.right + PAPER_RADIUS and paper_pos[1] > HEIGHT - trashcan_top_rect.height - PAPER_RADIUS - 50:
            score += 1
            paper_pos = [50, 50]
            paper_vel = [0, 0]
            if score == 5:
                draw_congratulations()
                pygame.display.flip()
                pygame.time.wait(2000)
                score = 0

        screen.blit(background_image, (0, 0))
        if game_started:
            draw_trashcan()
            draw_paper(paper_pos)
            draw_score()
            if mouse_down:
                draw_aim_line(paper_pos, mouse_pos)
        else:
            draw_start_button()
        pygame.display.flip()
        clock.tick(FPS)

# Inicia o jogo
game()
