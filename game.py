import pygame
from time import sleep
from square import square, superior
import copy

pygame.init()

background = (0, 0, 0)
deadCell = (195, 200, 181)
aliveCell = (0, 27, 9)

amount = 20
size = 20
display_size = ((amount*size) + amount - 1, (amount*size) + amount - 1)
display = pygame.display.set_mode(display_size)

exitGame = False
gameStarted = False

FPS = 2

grid = list()

clock = pygame.time.Clock()

def create_array():
    global grid
    
    for z in range(0, amount):
        placeholder = []
        for i in range(0, amount):
            cell = square(z, i, i*size + i, z*size + z, amount, size)
            placeholder.append(cell)
        grid.append(placeholder)

def create_grid():
    display.fill(background)
    
    for row in grid:
        for cell in row:
            if cell.alive:
                pygame.draw.rect(display, aliveCell, [cell.x, cell.y, size, size])
            else:
                pygame.draw.rect(display, deadCell, [cell.x, cell.y, size, size])
    pygame.display.update()

def check():
    global grid

    old_grid = copy.deepcopy(grid)
    

    for row in grid:
        for cell in row:
            alive = 0
            
            next_row = cell.row + 1
            previous_row = cell.row - 1
            
            next_column = cell.column + 1
            previous_column = cell.column - 1
            
            if previous_row < 0:
                previous_row = len(row) + 100
            
            if previous_column < 0:
                previous_column = len(row) + 100

            try:
                if old_grid[next_row][cell.column].alive:
                    alive += 1
            except:
                pass
            try:
                if old_grid[previous_row][cell.column].alive:
                    alive += 1
            except:
                pass
            try:
                if old_grid[cell.row][previous_column].alive:
                    alive += 1
            except:
                pass
            try:
                if old_grid[cell.row][next_column].alive:
                    alive += 1
            except:
                pass
            try:
                if old_grid[previous_row][previous_column].alive:
                    alive += 1
            except:
                pass
            try:
                if old_grid[previous_row][next_column].alive:
                    alive += 1
            except:
                pass
            try:
                if old_grid[next_row][previous_column].alive:
                    alive += 1
            except:
                pass
            try:
                if old_grid[next_row][next_column].alive:
                    alive += 1
            except:
                pass
            
            if alive < 2 or alive > 3:
                cell.alive = False
            elif alive == 3:
                cell.alive = True

create_array()
create_grid()

while not exitGame:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitGame = True

        if event.type == pygame.MOUSEBUTTONDOWN and not gameStarted:
            for row in grid:
                for cell in row:
                    click = pygame.mouse.get_pos()
                    if cell.is_in_range(click[0], click[1]):
                        cell.alive = (not cell.alive)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gameStarted = True

    if gameStarted: 
        check()

        if superior().number_alive == 0:
            print(superior().number_alive)
            exitGame = True

    create_grid()   
    clock.tick(FPS)
        

pygame.quit()
quit()