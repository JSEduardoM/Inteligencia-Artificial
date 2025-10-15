import pygame
import random

def simulacion_fluido():
    ANCHO, ALTO = 800, 600
    CELL = 40
    COLS, ROWS = ANCHO // CELL, ALTO // CELL

    AZUL = (0, 150, 255)
    AZUL_OSCURO = (0, 100, 200)
    PLOMO = (80, 80, 80)
    FONDO = (20, 20, 20)

    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Simulación de Fluidos Lenta")

    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    # Obstáculos
    for c in range(2, COLS, 5):
        for r in range(ROWS//3, ROWS//2):
            grid[r][c] = 2
    for c in range(1, COLS, 6):
        for r in range(ROWS//2, 2*ROWS//3):
            grid[r][c] = 2

    def dibujar():
        ventana.fill(FONDO)
        for i in range(ROWS):
            for j in range(COLS):
                if grid[i][j] == 1:
                    color = AZUL if random.random() < 0.5 else AZUL_OSCURO
                    pygame.draw.rect(ventana, color, (j*CELL, i*CELL, CELL, CELL))
                elif grid[i][j] == 2:
                    pygame.draw.rect(ventana, PLOMO, (j*CELL, i*CELL, CELL, CELL))
        pygame.display.flip()

    def paso():
        nonlocal grid
        new_grid = [fila[:] for fila in grid]

        # Iterar de abajo hacia arriba para empujar el agua
        for i in range(ROWS-2, -1, -1):
            for j in range(COLS):
                if grid[i][j] == 1:
                    # Intentar mover hacia abajo
                    if grid[i+1][j] == 0:
                        new_grid[i][j], new_grid[i+1][j] = 0, 1
                    else:
                        # Intentar expandirse lateralmente
                        dirs = []
                        if j > 0 and grid[i+1][j-1] == 0:
                            dirs.append(-1)
                        if j < COLS-1 and grid[i+1][j+1] == 0:
                            dirs.append(1)
                        if dirs:
                            d = random.choice(dirs)
                            new_grid[i][j], new_grid[i+1][j+d] = 0, 1
        grid = new_grid

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(4)  # FPS más bajo = más lento

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                cx, cy = x // CELL, y // CELL
                if 0 <= cx < COLS and 0 <= cy < ROWS:
                    if event.button == 1:
                        grid[cy][cx] = 1
                    elif event.button == 3:
                        grid[cy][cx] = 0 if grid[cy][cx] == 2 else 2

        # Generar menos partículas por frame para un flujo lento
        if random.random() < 0.3:
            grid[0][random.randint(0, COLS-1)] = 1

        paso()
        dibujar()

    pygame.quit()
