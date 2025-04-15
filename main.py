import pygame
import sys
import random
import os
import math

print("Ruta actual de ejecución:", os.getcwd())

# Inicialización de Pygame
pygame.init()

# ---------------------------
# COLORES DEFINIDOS (RGB)
# ---------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TRON_RED = (255, 50, 50)
TRON_BLUE = (50, 150, 255)
TRON_GLOW = (0, 255, 255)

# ---------------------------
# TAMAÑO DE LA VENTANA
# ---------------------------
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snail Race Tron")

# Use relative paths based on current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
menu_background = pygame.image.load(os.path.join(current_dir, "menu-bg.jpg")).convert_alpha()
player1_sprite = pygame.image.load(os.path.join(current_dir, "player1.png")).convert_alpha()
player2_sprite = pygame.image.load(os.path.join(current_dir, "player2.png")).convert_alpha()
player1_sprite = pygame.transform.scale(player1_sprite, (60, 60))
player2_sprite = pygame.transform.scale(player2_sprite, (60, 60))
background_img = pygame.image.load(os.path.join(current_dir, "tron-bg.jpg")).convert()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
menu_background = pygame.transform.scale(menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))


def load_animation_frames(folder):
    frames = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".png"):
            frame = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
            frame = pygame.transform.scale(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
            frames.append(frame)
    return frames

# Use relative path for animation frames
background_frames = load_animation_frames(os.path.join(current_dir, "tron_frames"))

def play_intro_animation(frames, screen, duration=3000, fps=15):
    clock = pygame.time.Clock()
    frame_index = 0
    elapsed = 0
    start_time = pygame.time.get_ticks()

    while elapsed < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(frames[frame_index], (0, 0))
        pygame.display.flip()

        frame_index = (frame_index + 1) % len(frames)
        clock.tick(fps)

        elapsed = pygame.time.get_ticks() - start_time



# ---------------------------
# FUENTES DE TEXTO
# ---------------------------
font = pygame.font.SysFont("Arial", 24)
font_large = pygame.font.SysFont("Arial", 36)


# ---------------------------
# DIBUJA TEXTO EN PANTALLA
# ---------------------------
def draw_text(text, font, color, surface, x, y):
    label = font.render(text, True, color)
    surface.blit(label, (x, y))

# ---------------------------
# MENÚ DE INICIO
# ---------------------------
def menu():
    play_intro_animation(background_frames, screen)
    player1_name = input_name("Introduce el nombre de Jugador 1 (Tecla F)")
    player2_name = input_name("Introduce el nombre de Jugador 2 (Tecla K)")
    select_track(player1_name, player2_name)

# ---------------------------
# FUNCIÓN PARA INGRESAR NOMBRES
# ---------------------------
def input_name(label):
    name = ""
    input_box_y = 300
    entering = True

    while entering:
        screen.blit(menu_background, (0, 0))
        draw_text(label, font, WHITE, screen, 200, 250)
        draw_text(name, font, WHITE, screen, 200, input_box_y)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    entering = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
    return name

# ---------------------------
# SELECCIÓN DE PISTA (1-5)
# ---------------------------
def select_track(player1_name, player2_name):
    screen.blit(menu_background, (0, 0))
    draw_text("Elige tu pista (1-5):", font_large, WHITE, screen, 250, 300)
    pygame.display.flip()

    selected_track = None
    while selected_track is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_5:
                    selected_track = event.key - pygame.K_1
    start_race(player1_name, player2_name, selected_track)

# ---------------------------
# ÍCONO DE JUGADOR (ESTILO TRON)
# ---------------------------
def draw_tron_icon(x, y, color):
    pygame.draw.circle(screen, color, (x, y), 12)
    pygame.draw.circle(screen, TRON_GLOW, (x, y), 16, 2)

# ---------------------------
# FUNCIÓN PRINCIPAL DE LA CARRERA
# ---------------------------
def start_race(player1_name, player2_name, track):
    # Posiciones iniciales
    player1_pos = 0
    player2_pos = 0
    y1, y2 = 250, 350
    background_x = 0  # Posición inicial del fondo
    scroll_speed = 1  # Velocidad del movimiento

    # Longitud de la pista: de 500 a 800 pasos
    track_length = 500 + track * 75  # pista 0-4 → 500-800

    player1_path = [(100 + player1_pos, y1)]
    player2_path = [(100 + player2_pos, y2)]

    clock = pygame.time.Clock()
    running = True
    start_time = pygame.time.get_ticks()  # Cronómetro empieza cuando inicia la carrera


    while running:
        background_x -= scroll_speed
        if background_x <= -SCREEN_WIDTH:
            background_x = 0

        # Dibujar el fondo dos veces para simular desplazamiento infinito
        screen.blit(background_img, (background_x, 0))
        screen.blit(background_img, (background_x + SCREEN_WIDTH, 0))

        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # En segundos

        # Dibujar el cronómetro en pantalla
        draw_text(f"Tiempo: {elapsed_time:.2f} s", font, WHITE, screen, 10, 10)


        # Dibujar la meta
        finish_x = 100 + track_length
        pygame.draw.line(screen, WHITE, (finish_x, 0), (finish_x, SCREEN_HEIGHT), 5)

        # Dibujar líneas del trail de cada jugador
        if len(player1_path) > 1:
            pygame.draw.lines(screen, TRON_RED, False, player1_path, 4)
        if len(player2_path) > 1:
            pygame.draw.lines(screen, TRON_BLUE, False, player2_path, 4)


        # Dibuja jugadores
        screen.blit(player1_sprite, (100 + player1_pos - 20, y1 - 20))  # centrado
        screen.blit(player2_sprite, (100 + player2_pos - 20, y2 - 20))

        # Eventos de teclado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:  # Jugador 1 avanza con F
                    player1_pos += 4
                    
                elif event.key == pygame.K_k:  # Jugador 2 avanza con K
                    player2_pos += 4

        # Verificar si alguien ganó
        if player1_pos >= track_length:
            show_winner(player1_name)
            running = False
        elif player2_pos >= track_length:

            show_winner(player2_name)
            running = False

        pygame.display.flip()
        clock.tick(60)  # Limita a 60 FPS

# ---------------------------
# MUESTRA EL GANADOR
# ---------------------------
def show_winner(name):
    screen.fill(BLACK)
    draw_text(f"¡Ganador: {name}!", font_large, WHITE, screen, 400, 250)
    pygame.display.flip()
    pygame.time.delay(4000)

# ---------------------------
# PROGRAMA PRINCIPAL
# ---------------------------
def main():
    menu()

if __name__ == "__main__":
    main()
