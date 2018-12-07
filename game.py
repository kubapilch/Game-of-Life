import pygame
from time import sleep
from square import square, superior
import copy
import atexit

pygame.init()

class Game():

    #Colors
    backgroundColor = (0, 0, 0)
    deadCellColor = (195, 200, 181)
    aliveCellColor = (0, 27, 9)

    #FPS control variables
    FPS = 30
    clock = pygame.time.Clock()

    def __init__(self, amount=20, size=20):
        #Some math to calculate size of the screen based on size and amount of cells + space between them
        self.display_size = ((amount*size) + amount - 1, (amount*size) + amount - 1) 
        self.display = pygame.display.set_mode(self.display_size)

        self.size = size
        self.amount = amount

        atexit.register(self.cleanup)


    def create_array(self):
        grid = list()
        
        size = self.size
        amount = self.amount

        for row in range(0, amount):
            placeholder = []
            for column in range(0, amount):
                cell = square(row=row, column=column, x=column*size + column, y=row*size + row, number_of_columns=amount, size=size)
                placeholder.append(cell)
            grid.append(placeholder)
        return grid

    def create_grid(self, grid):
        self.display.fill(self.backgroundColor)
        #Render grid
        for row in grid:
            for cell in row:
                if cell.alive:
                    pygame.draw.rect(self.display, self.aliveCellColor, [cell.x, cell.y, cell.size, cell.size])
                else:
                    pygame.draw.rect(self.display, self.deadCellColor, [cell.x, cell.y, cell.size, cell.size])
        pygame.display.update()

    def check(self, grid):

        #Create old gird tamplate
        old_grid = copy.deepcopy(grid)

        for row in grid:
            for cell in row:
                alive = 0

                # Check for alive neighbors
                # Upper cell
                if not cell.is_in_first_row:
                    if old_grid[cell.row - 1][cell.column].alive:
                        alive += 1
                # Left cell
                if not cell.is_in_first_column:
                    if old_grid[cell.row][cell.column - 1].alive:
                        alive += 1
                # Right cell
                if not cell.is_in_last_column:
                    if old_grid[cell.row][cell.column + 1].alive:
                        alive += 1
                # Down cell
                if not cell.is_in_last_row:
                    if old_grid[cell.row + 1][cell.column].alive:
                        alive += 1
                # Left top cell
                if not cell.is_in_first_column and not cell.is_in_first_row:
                    if old_grid[cell.row - 1][cell.column - 1].alive:
                        alive += 1
                # Right top cell
                if not cell.is_in_first_row and not cell.is_in_last_column:
                    if old_grid[cell.row - 1][cell.column + 1].alive:
                        alive += 1
                # Left down cell
                if not cell.is_in_last_row and not cell.is_in_first_column:
                    if old_grid[cell.row + 1][cell.column - 1].alive:
                        alive += 1
                # Right down cell
                if not cell.is_in_last_column and not cell.is_in_last_row:
                    if old_grid[cell.row + 1][cell.column + 1].alive:
                        alive += 1

                #Decide if cell is alive or dead
                if alive < 2 or alive > 3:
                    cell.alive = False
                elif alive == 3:
                    cell.alive = True
        
        return grid

    def start_game(self):
        mousePressed = False
        highlitedCells = []

        exitGame = False
        gameStarted = False
        
        grid = self.create_array()
        self.create_grid(grid)
        
        while not exitGame:
            
            for event in pygame.event.get():
                #Check if user wants to quit
                if event.type == pygame.QUIT:
                    exitGame = True

                #Placing cells
                if mousePressed:
                    for row in grid:
                        for cell in row:
                            click = pygame.mouse.get_pos()
                            if cell.is_in_range(click[0], click[1]) and cell not in highlitedCells:
                                cell.alive = (not cell.alive)
                                self.create_grid(grid)
                                highlitedCells.append(cell)
                
                #Start drawing
                if event.type == pygame.MOUSEBUTTONDOWN and not gameStarted:
                    mousePressed = True
                
                #Stop drawing
                if event.type == pygame.MOUSEBUTTONUP and not gameStarted:
                    mousePressed = False
                    highlitedCells = []

                #Start the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not gameStarted:
                        gameStarted = True
                        self.FPS = 2
                    elif event.key == pygame.K_SPACE and gameStarted:
                        gameStarted = False
                        self.FPS = 30

            if gameStarted: 
                grid = self.check(grid)
                
                #Render grid
                self.create_grid(grid)  
                
                #Check if all cells are dead
                if superior().number_alive == 0:
                    exitGame = True

            self.clock.tick(self.FPS)
    
    def cleanup(self):
        pygame.quit()
        quit()

if __name__ == "__main__":
    game = Game()
    game.start_game()