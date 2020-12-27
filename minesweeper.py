import pygame, random, time, math

def inGrid(x, y, Mx, My):
    return x >= 0 and x < Mx and y >= 0 and y < My

def placeBomb(grid, Mx, My, noGo):
    placed = False
    while not placed:
        x = random.randrange(Mx)
        y = random.randrange(My)
        if not grid[x][y].bomb and not [x,y] in noGo:
            placed = True
            grid[x][y].bomb = True
    for x_pos in range(x - 1, x + 2):
        for y_pos in range(y - 1, y + 2):
            if inGrid(x_pos, y_pos, Mx, My):
                grid[x_pos][y_pos].neighbours += 1

def remove(grid, x, y, Mx, My):
    grid[x][y].bomb = False
    for x_pos in range(x - 1, x + 2):
        for y_pos in range(y - 1, y + 2):
            if inGrid(x_pos, y_pos, Mx, My):
                grid[x_pos][y_pos].neighbours -= 1
        
        

class Cell:
    def __init__(self, x, y):
        self.bomb = False
        self.state = "covered"
        self.neighbours = 0
        self.x = x
        self.y = y
        self.size = 16
        self.bomb_state = "revealed"
        self.misflag = False

    def draw(self, window, images):
        rect = (self.x*self.size,self.y*self.size + 26)
        if self.state == "open":
            if self.bomb:
                if self.bomb_state == "revealed":
                    window.blit(images.bombrevealed,rect)
                elif self.bomb_state == "boom":
                    window.blit(images.bombdeath,rect)
            else:
                if self.misflag:
                    window.blit(images.bombmisflagged,rect)
                else:
                    window.blit(images.numbers[self.neighbours],rect)
        elif self.state == "covered":
            window.blit(images.blank,rect)
        elif self.state == "flagged":
            window.blit(images.bombflagged,(rect[0],rect[1]+1))
        elif self.state == "question":
            window.blit(images.bombquestion,rect)

class Images:
    def __init__(self):
        self.numbers = []
        for i in range(9):
            self.numbers.append(pygame.image.load("open"+str(i)+".gif"))
        self.blank = pygame.image.load("blank.gif")
        self.bombdeath = pygame.image.load("bombdeath.gif")
        self.bombflagged = pygame.image.load("bombflagged.gif")
        self.bombmisflagged = pygame.image.load("bombmisflagged.gif")
        self.bombquestion = pygame.image.load("bombquestion.gif")
        self.bombrevealed = pygame.image.load("bombrevealed.gif")
        self.time = []
        for i in range(10):
            self.time.append(pygame.image.load("time"+str(i)+".gif"))
        self.time_neg = pygame.image.load("time-.gif")
        self.smile = pygame.image.load("facesmile.gif")
        self.ooh = pygame.image.load("faceooh.gif")
        self.dead = pygame.image.load("facedead.gif")
        self.win = pygame.image.load("facewin.gif")

def draw_num(window, images, number, x):
    rect = ((x+26,3),(x+13,3),(x,3))
    if number >= 0:
        n = "00"+str(number)
        for i in range(3,0,-1):
            window.blit(images.time[int(n[-i])], rect[i-1])
    else:
        n = "0"+str(-number)
        window.blit(images.time_neg, rect[2])
        for i in range(2,0,-1):
            window.blit(images.time[int(n[-i])], rect[i-1])
        
        

def showAll(grid,Mx,My):
    for x in range(Mx):
        for y in range(My):
            if grid[x][y].bomb:
                if grid[x][y].state == "covered" or grid[x][y].state == "question":
                    grid[x][y].state = "open"
            else:
                if grid[x][y].state == "flagged":
                    grid[x][y].state = "open"
                    grid[x][y].misflag = True

def expose(grid,Mx,My):
    done = False
    while not done:
        a = False
        for x in range(Mx):
            for y in range(My):
                if grid[x][y].state == "open" and grid[x][y].neighbours == 0:
                    for X in range(x-1,x+2):
                        for Y in range(y-1,y+2):
                            if inGrid(X,Y,Mx,My):
                                if not grid[X][Y].bomb:
                                    if grid[X][Y].state == "covered" or grid[X][Y].state == "question":
                                        grid[X][Y].state = "open"
                                        a = True
        if not a:
            done = True

def finished(grid,Mx,My):
    n = True
    for x in range(Mx):
        for y in range(My):
            if not grid[x][y].bomb:
                if grid[x][y].state == "covered" or grid[x][y].state == "question":
                    n = False

    if n:
        for x in range(Mx):
            for y in range(My):
                if grid[x][y].state != "flagged" and grid[x][y].bomb:
                    grid[x][y].state = "flagged"
    
    return n
                    

def main():
    grid_width = 31
    grid_height = 16
    bombs = 99

    #grid_width = 10
    #grid_height = 10
    #bombs = 10
    
    flags = bombs
    width = grid_width * 16
    height = grid_height * 16
    cells = []
    for x in range(grid_width):
        cells.append([])
        for y in range(grid_height):
            cells[-1].append(Cell(x,y))


    pygame.init()
    screen = pygame.display.set_mode((width,height+26))
    pygame.display.set_caption("minesweeper")

    images = Images()

    done = False
    firstClick = True
    timer = False
    total = 0
    dead = False
    rect = (int(width/2)-13,0)
    restart = True
    win = False

    while restart:
        restart = False
        done = False
        win = False
        dead = False
        timer = False
        total = 0
        firstclick = True
        flags = bombs
        cells = []
        for x in range(grid_width):
            cells.append([])
            for y in range(grid_height):
                cells[-1].append(Cell(x,y))
            
        
        while not done:
            events = pygame.event.get()
            x,y = pygame.mouse.get_pos()
            cellX = int(x/16)
            cellY = int((y-26)/16)
            if inGrid(cellX,cellY,grid_width,grid_height) and y > 26 and not win and not dead:
                for event in events:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            if firstclick:
                                firstclick = False
                                if not timer:
                                    start = time.time()
                                timer = True

                                noGo = []
                                for i in range(cellX-1,cellX+2):
                                    for j in range(cellY-1,cellY+2):
                                        noGo.append([i,j])
                                for i in range(bombs):
                                    placeBomb(cells, grid_width, grid_height, noGo)

                            if cells[cellX][cellY].state == "covered":
                                cells[cellX][cellY].state = "open"
                                if cells[cellX][cellY].bomb:
                                    cells[cellX][cellY].bomb_state = "boom"
                                    showAll(cells,grid_width,grid_height)
                                    dead = True
                                elif cells[cellX][cellY].neighbours == 0:
                                    expose(cells,grid_width,grid_height)


                        elif event.button == 3:
                            if cells[cellX][cellY].state == "covered":
                                cells[cellX][cellY].state = "flagged"
                                flags -= 1
                            elif cells[cellX][cellY].state == "flagged":
                                flags += 1
                                cells[cellX][cellY].state = "question"
                            elif cells[cellX][cellY].state == "question":
                                cells[cellX][cellY].state = "covered"
            elif pygame.MOUSEBUTTONUP in [event.type for event in events]:
                if x > rect[0] and x < rect[0] + 26 and y > 0 and y < 26:
                    done = True
                    restart = True

            win = finished(cells,grid_width,grid_height)
            if win or dead:
                timer = False
            
            if timer:
                total = int(time.time() - start)

            if dead:
                face = images.dead
            elif win:
                face = images.win
            elif any(pygame.mouse.get_pressed()):
                face = images.ooh
            else:
                face = images.smile
                
            
            screen.fill((192,192,192))
            screen.blit(face,rect)
            
            for x in range(grid_width):
                for y in range(grid_height):
                    cells[x][y].draw(screen,images)
            draw_num(screen,images,flags,0)
            draw_num(screen,images,total,width-39)
            pygame.display.flip()
            pygame.time.wait(5)

            if pygame.QUIT in [event.type for event in events]:
                done = True
    
if __name__ == "__main__":
    main()
    pygame.quit()
