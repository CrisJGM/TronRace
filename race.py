import pygame
import sys
import random

# Inicializar pygame
pygame.init()

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TRON_RED = (255, 50, 50)
TRON_BLUE = (50, 150, 255)
TRON_GLOW = (0, 255, 255)

# Pantalla
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("""                       draw_ascii_title()                           """)

# Fuentes
font = pygame.font.SysFont("Arial", 24)
font_large = pygame.font.SysFont("Arial", 36)

# Comentarios
commentary = [
    "¡Comienza la carrera!",
    "Esto se empieza a encender...",
    "Hemos cruzado el centro del camino.",
    "Cada vez queda menos...",
]

# Estados de teclas
moving_player1 = False
moving_player2 = False

# ASCII Art
ASCII_TITLE = """
                                                                                    _____             _         _____                      
                                                                                    / ____|           (_)       |  __ \                     
                                                                                    | (___   ___   __ _ _ _ __   | |__) |_ _ _ __ ___  _ __  
                                                                                    \___ \ / _ \ / _` | | '_ \  |  ___/ _` | '_ ` _ \| '_ \ 
                                                                                    ____) | (_) | (_| | | | | | | |  | (_| | | | | | | |_) |
                                                                                    |_____/ \___/ \__, |_|_| |_| |_|   \__,_|_| |_| |_| .__/ 
                                                                                                    __/ |                               | |    
                                                                                                |___/                                |_|    
"""

# Dibujar texto
def draw_text(text, font, color, surface, x, y):
    label = font.render(text, True, color)
    surface.blit(label, (x, y))

def draw_ascii_title():
    screen.fill(BLACK)
    y_offset = 20
    for line in ASCII_TITLE.splitlines():
        draw_text(line, font, TRON_GLOW, screen, 50, y_offset)
        y_offset += 24
    pygame.display.flip()
    pygame.time.delay(1500)

# Menú
def menu():
    draw_ascii_title()
    print()
    draw_text("Introduce el nombre de Jugador 1", font, WHITE, screen, 200, 250)
    pygame.display.flip()

    player1_name = ""
    player2_name = ""
    input_box_y = 300

    def input_name(label):
        name = ""
        entering = True
        while entering:
            screen.fill(BLACK)
            draw_text(label, font, WHITE, screen, 200, 250)
            draw_text(name, font, WHITE, screen, 200, input_box_y)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name:
                        entering = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
        return name

    player1_name = input_name("Introduce el nombre de Jugador 1")
    player2_name = input_name("Introduce el nombre de Jugador 2")
    select_track(player1_name, player2_name)

# Selección de pista
def select_track(player1_name, player2_name):
    screen.fill(BLACK)
    draw_ascii_title()
    draw_text("Elige tu pista (1-5):", font_large, WHITE, screen, 250, 300)
    pygame.display.flip()

    selected_track = None
    while selected_track is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_5:
                    selected_track = event.key - pygame.K_1
    start_race(player1_name, player2_name, selected_track)

# Comentarios
def show_commentary(comment_index):
    screen.fill(BLACK)
    draw_text(commentary[comment_index], font, WHITE, screen, 200, 50)
    pygame.display.flip()
    pygame.time.delay(1000)

# Estilo Tron para jugador
def draw_tron_icon(x, y, color):
    pygame.draw.circle(screen, color, (x, y), 12)
    pygame.draw.circle(screen, TRON_GLOW, (x, y), 16, 2)

# Carrera
def start_race(player1_name, player2_name, track):
    global moving_player1, moving_player2
    player1_x = 50
    player2_x = 50
    y1, y2 = 250, 350
    track_length = random.randint(400, 700)
    score1 = score2 = 0

    show_commentary(0)
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    moving_player1 = True
                if event.key == pygame.K_k:
                    moving_player2 = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_f:
                    moving_player1 = True
                if event.key == pygame.K_k:
                    moving_player2 = True

        if moving_player1:
            player1_x += 2
        if moving_player2:
            player2_x += 2

        # Meta
        pygame.draw.line(screen, WHITE, (track_length, 0), (track_length, SCREEN_HEIGHT), 5)

        # Jugadores
        draw_tron_icon(player1_x, y1, TRON_RED)
        draw_tron_icon(player2_x, y2, TRON_BLUE)

        # Comentarios progresivos
        for pos, score, idx in [(player1_x, score1, 0), (player2_x, score2, 0)]:
            if pos >= track_length * 0.25 and score == 0:
                show_commentary(1)
                if pos == player1_x:
                    score1 = 1
                else:
                    score2 = 1
            elif pos >= track_length * 0.5 and score == 1:
                show_commentary(2)
                if pos == player1_x:
                    score1 = 2
                else:
                    score2 = 2
            elif pos >= track_length * 0.75 and score == 2:
                show_commentary(3)
                if pos == player1_x:
                    score1 = 3
                else:
                    score2 = 3

        # Fin de la carrera
        if player1_x >= track_length:
            winner = player1_name
            running = False
        elif player2_x >= track_length:
            winner = player2_name
            running = False

        pygame.display.flip()
        clock.tick(60)

    # Resultado final
    screen.fill(BLACK)
    draw_text(f"¡Tenemos un ganador! Enhorabuena {winner}", font_large, WHITE, screen, 150, 250)
    pygame.display.flip()
    pygame.time.delay(4000)

# Main
def main():
    menu()

if __name__ == "__main__":
    main()

