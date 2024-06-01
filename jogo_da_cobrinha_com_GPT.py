import pygame
import random
import urllib.request
import io

# Inicialização do Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Jogo da Cobrinha - Arbok')

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Configurações da cobrinha
snake_size = 20
snake_speed = 15

# URL da imagem da Arbok
AROK_IMAGE_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/24.png"

# Função para carregar a imagem da Arbok
def load_image():
    with urllib.request.urlopen(AROK_IMAGE_URL) as url:
        image_file = io.BytesIO(url.read())
        image = pygame.image.load(image_file)
        return pygame.transform.scale(image, (snake_size, snake_size))

# Função para desenhar a cobrinha
def draw_snake(snake_list):
    for x, y in snake_list:
        screen.blit(load_image(), (x, y))

# Função para mostrar o texto na tela
def show_text(msg, color, x, y):
    font = pygame.font.SysFont(None, 35)
    text = font.render(msg, True, color)
    screen.blit(text, [x, y])

# Função principal do jogo
def game_loop():
    game_over = False
    game_close = False

    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, SCREEN_WIDTH - snake_size) / snake_size) * snake_size
    foody = round(random.randrange(0, SCREEN_HEIGHT - snake_size) / snake_size) * snake_size

    clock = pygame.time.Clock()
    lives = 3

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            show_text("Game Over! Pressione C para jogar novamente ou Q para sair", RED, 50, SCREEN_HEIGHT / 2)
            show_text(f'Vidas restantes: {lives}', RED, 50, SCREEN_HEIGHT / 2 + 50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_size
                    x1_change = 0

        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            lives -= 1
            if lives == 0:
                game_close = True
            else:
                x1 = SCREEN_WIDTH / 2
                y1 = SCREEN_HEIGHT / 2
                x1_change = 0
                y1_change = 0
                snake_list = []
                length_of_snake = 1

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)
        pygame.draw.rect(screen, GREEN, [foodx, foody, snake_size, snake_size])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                lives -= 1
                if lives == 0:
                    game_close = True
                else:
                    x1 = SCREEN_WIDTH / 2
                    y1 = SCREEN_HEIGHT / 2
                    x1_change = 0
                    y1_change = 0
                    snake_list = []
                    length_of_snake = 1

        draw_snake(snake_list)
        show_text(f'Vidas: {lives}', WHITE, 0, 0)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, SCREEN_WIDTH - snake_size) / snake_size) * snake_size
            foody = round(random.randrange(0, SCREEN_HEIGHT - snake_size) / snake_size) * snake_size
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Iniciar o jogo
game_loop()
