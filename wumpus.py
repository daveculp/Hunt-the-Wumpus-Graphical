import pygame
import random
import time
import sys

#================================================================================
#                       Gloabls and Constants area                              =
#================================================================================

#Our screen width and height
SCREEN_WIDTH = SCREEN_HEIGHT = 800

#Number of rooms
GRID_WIDTH = 10
GRID_HEIGHT = 10

#key to what is in each room
EMPTY = 0
WUMPUS = 1
BATS = 2
PIT = 3

#number of bats and pits in the cave
NUM_BATS = 4
NUM_PITS = 5

#constants for directions
LEFT = 0
RIGHT = 1
UP = 3
DOWN = 4

#color defintions
BROWN = 193,154,107
BLACK = 0,0,0
RED = 255,0,0

MAX_ARROWS = 1
#two dimensional list that holds the cave
cave = [[EMPTY for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

player_pos = [0,0] #tracks where we are in the cave
wumpus_pos = [0,0] #tracks where the Wumpus is
num_arrows = MAX_ARROWS # total number of arrows player can have

#================================================================================
#                       Functions Area                                          =
#================================================================================
def check_neighbor_rooms(pos, item):
    """ Checks each orthagonal cell next to pos for the requested item
    returns True as soon as the item is found.
    """
    
    x=0 # the 0th index is the x coordinate
    y=1 # the 1st index is the y coordinate

    #If the cell is on  the inside of the grid 
    if (pos[x] > 0 and pos[x]< GRID_WIDTH-1) and ( pos[y]>0 and pos[y]<GRID_HEIGHT-1 ):
        if cave [pos[x]] [pos[y]-1] == item:
            return True
        elif cave [pos[x]] [pos[y]+1] == item:
            return True
        elif cave [pos[x]-1] [pos[y]] == item:
            return True
        elif cave [pos[x]+1] [pos[y]] == item:
             return True
    # The cell is on the left side of grid:
    elif pos[x] == 0 and (pos[y]>0 and pos[y]<GRID_HEIGHT-1):
        if cave[ pos[x]][pos[y]-1] == item:
            return True
        elif cave[ pos[x]][pos[y]+1] == item:
            return True
        elif cave [ pos[x]+1][pos[y]] == item:
            return True

    # The cell is on the right side:
    elif pos[x] == GRID_WIDTH-1 and (pos[y]>0 and pos[y]<GRID_HEIGHT-1):
        if cave[ pos[x]][pos[y]-1] == item:
            return True
        elif cave[ pos[x]][pos[y]+1] == item:
            return True
        elif cave [ pos[x]-1][pos[y]] == item:
            return True

    # The cell is on the top row:
    elif pos[y] == 0 and (pos[x]>0 and pos[x]<GRID_WIDTH-1):
        if cave[ pos[x]+1][pos[y]] == item:
            return True
        elif cave[ pos[x]-1][pos[y]] == item:
            return True
        elif cave [ pos[x]][pos[y]+1] == item:
            return True
            
    # The cell is on the bottom row:
    elif pos[y] == GRID_HEIGHT-1 and (pos[x]>0 and pos[x]<GRID_WIDTH-1):
        if cave[ pos[x]+1][pos[y]] == item:
            return True
        elif cave[ pos[x]-1][pos[y]] == item:
            return True
        elif cave [ pos[x]][pos[y]-1] == item:
            return True

    #The cell is inn the upper left corner
    elif pos[x] == 0 and pos[y] == 0:
        if cave[0][1] == WUMPUS or cave[1][0] == item:
            return True

    #The cell is in the upper right corner
    elif pos[x] == GRID_WIDTH-1 and pos[y] == 0:
        if cave[GRID_WIDTH-1][1] == WUMPUS or cave[GRID_WIDTH-2][0] == item:
            return True

    #The cell is in the lower left corner
    elif pos[x] == 0 and pos[y] == GRID_HEIGHT -1:
        if cave[0][GRID_HEIGHT-2] == WUMPUS or cave[1][GRID_HEIGHT-1] == item:
            return True

    #The cell is in the lower right corner
    elif pos[x] == GRID_WIDTH-1 and pos[y] == GRID_HEIGHT-1:
        if cave[GRID_WIDTH-1][GRID_HEIGHT-2] == item or cave[GRID_WIDTH-2][GRID_HEIGHT-1] == item:
            return True
        
def draw_room( pos, screen):
    """ Draws the room in the back buffer
    """
    x=0
    y=1
    
    wumpus = False  #assume no wumpus present
    screen.fill( (0,0,0) ) #paint the background in red

    #draw the room circle in brown
    circle_radius = int ((SCREEN_WIDTH//2)*.75)
    pygame.draw.circle(screen, BROWN, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), circle_radius, 0)

    #next draw all exits from the room
    if pos[x] > 0:
        #draw left exit
        left = 0
        top = SCREEN_HEIGHT//2-40
        pygame.draw.rect(screen, BROWN, ((left,top), (SCREEN_WIDTH*.25,80)), 0)
    if pos[x]<GRID_WIDTH-1:
        #draw right exit
        left = SCREEN_WIDTH-110
        top = SCREEN_HEIGHT//2-40
        pygame.draw.rect(screen, BROWN, ((left,top), (SCREEN_WIDTH*.25,80)), 0)
    if pos[y] >0:
        #draw top exit
        left = SCREEN_WIDTH//2-40
        top = 0
        pygame.draw.rect(screen, BROWN, ((left,top), (80,SCREEN_HEIGHT*.25)), 0)
    if pos[y] <GRID_HEIGHT -1:
        #draw bottom exit
        left = SCREEN_WIDTH//2-40
        top = SCREEN_HEIGHT-110
        pygame.draw.rect(screen, BROWN, ((left,top), (80,SCREEN_HEIGHT*.25)), 0)
        
    #draw a blood circle if the Wumpus is nearby
    if check_neighbor_rooms(pos, WUMPUS) == True:
        circle_radius = int ((SCREEN_WIDTH//2)*.5)
        pygame.draw.circle(screen, RED, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), circle_radius, 0)

    #draw the pit in black if it is present
    if cave[pos[x]][pos[y]] == PIT:
        circle_radius = int ((SCREEN_WIDTH//2)*.5)
        pygame.draw.circle(screen, BLACK, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), circle_radius, 0)


    bats_near = check_neighbor_rooms(pos, BATS)
    pit_near = check_neighbor_rooms(pos, PIT)
     
    #draw the player
    screen.blit(player_img,(SCREEN_WIDTH//2-player_img.get_width()//2,SCREEN_HEIGHT//2-player_img.get_height()//2))

    #draw the bat imag
    if cave[pos[x]][pos[y]] == BATS:
        screen.blit(bat_img,(SCREEN_WIDTH//2-bat_img.get_width()//2,SCREEN_HEIGHT//2-bat_img.get_height()//2))

    #draw the bat wumpus
    if cave[pos[x]][pos[y]] == WUMPUS:
        screen.blit(wumpus_img,(SCREEN_WIDTH//2-wumpus_img.get_width()//2,SCREEN_HEIGHT//2-wumpus_img.get_height()//2))
        
    #draw text
    y_text_pos = 0 #keeps track of the next y positiojn on screen to draw text
    pos_text = font.render("POS:"+str(pos[x])+","+str(pos[y]), 1, (0, 255, 64))
    screen.blit(pos_text,(0, 0))
    arrow_text = font.render("Arrows: "+str(num_arrows), 1, (0, 255, 64))
    y_text_pos = y_text_pos+pos_text.get_height()+10
    screen.blit(arrow_text,(0, y_text_pos))
    if bats_near == True:
        bat_text = font.render("You hear the squeaking of bats nearby", 1, (0, 255, 64))
        y_text_pos = y_text_pos+bat_text.get_height()+10
        screen.blit(bat_text,(0, y_text_pos))
    if pit_near == True:
        pit_text = font.render("You feel a draft nearby", 1, (0, 255, 64))
        y_text_pos = y_text_pos+pit_text.get_height()+10
        screen.blit(pit_text,(0, y_text_pos))

    if cave[pos[x]][pos[y]] == BATS: #if bats are near, go ahead and flip the display and wait a bit
        pygame.display.flip()
        time.sleep(2.0)
        
              
def populate_cave():
    global player_pos, wumpus_pos, cave

    #reset all cells in the cave to empty
    for row in range(GRID_HEIGHT-1):
        for col in range(GRID_WIDTH-1):
            cave[row][col] = EMPTY

    #place the player
    player_pos = [random.randint(0,GRID_WIDTH-1), random.randint(0, GRID_HEIGHT -1)]

    # place the wumpus
    wumpus_pos = player_pos
    while (wumpus_pos == player_pos):
        wumpus_pos = [random.randint(0,GRID_WIDTH-1), random.randint(0, GRID_HEIGHT -1)]
    cave [wumpus_pos[0]] [wumpus_pos[1]] = WUMPUS
    
    #place the bats
    for bat in range(0,NUM_BATS):
        bat_pos = player_pos
        while bat_pos == player_pos or cave [bat_pos[0]][bat_pos[1]] == BATS or cave [bat_pos[0]][bat_pos[1]] == WUMPUS:
            bat_pos = [random.randint(0,GRID_WIDTH-1), random.randint(0, GRID_HEIGHT -1)]
        cave [bat_pos[0]][bat_pos[1]] = BATS
        print ("Bats at: "+str(bat_pos))

    #place the pits
    for pit in range (0,NUM_PITS):
        pit_pos = player_pos
        while (pit_pos == player_pos) or (cave [pit_pos[0]][pit_pos[1]] == BATS) or (pit_pos == wumpus_pos):
            pit_pos = [random.randint(0,GRID_WIDTH-1), random.randint(0, GRID_HEIGHT -1)]
        cave [pit_pos[0]][pit_pos[1]] = PIT
        print ("Pit at: "+str(pit_pos))

    print ("Player at: "+str(player_pos))
    print ("Wumpus at: "+str(wumpus_pos))

def place_wumpus():
    global player_pos, cave, wumpus_pos
    
    cave [wumpus_pos[0]][wumpus_pos[1]] = EMPTY
    print ("Deleting Wumpus at: "+str(wumpus_pos))
    
    wumpus_pos = player_pos
    while (wumpus_pos == player_pos) or (cave [wumpus_pos[0]][wumpus_pos[1]] == BATS) or (cave [wumpus_pos[0]][wumpus_pos[1]] == PIT):
        wumpus_pos = [random.randint(0,GRID_WIDTH-1), random.randint(0, GRID_HEIGHT -1)]
    cave [wumpus_pos[0]][wumpus_pos[1]] = WUMPUS
    print ("Wumpus at: "+str(wumpus_pos))
    
def check_room(pos):
    global player_pos, cave, screen
    
    #is there a Wumpus in the room?
    if player_pos == wumpus_pos:
        game_over("You were eaten by a WUMPUS!!!")

    #is there a pit?
    if cave [pos[0]][pos[1]] == PIT:
        game_over("You fell into a bottomless pit!!")

    #is there bats in the room?  If so move the player and the bats
    if cave [pos[0]][pos[1]] == BATS:
        print("Bats pick you up and place you elsewhere in the cave!")
        screen.fill(BLACK)
        bat_text = font.render("Bats pick you up and place you elsewhere in the cave!", 1, (0, 255, 64))
        textrect = bat_text.get_rect()
        textrect.centerx = screen.get_rect().centerx
        textrect.centery = screen.get_rect().centery
        screen.blit(bat_text,textrect)
        pygame.display.flip()
        time.sleep(2.5)
        new_pos = pos # set new_pos equal to the old os so the first test fails
        # Now place the player in a random location
        while cave [new_pos[0]][new_pos[1]] == PIT or cave [new_pos[0]][new_pos[1]] == WUMPUS or cave [new_pos[0]][new_pos[1]] == BATS:
            new_pos = [random.randint(0,GRID_WIDTH-1), random.randint(0, GRID_HEIGHT -1)]
            
        player_pos = new_pos
        print ("player at:"+str(player_pos))
        
        new_pos = pos
        while cave [new_pos[0]][new_pos[1]] == PIT or cave [new_pos[0]][new_pos[1]] == WUMPUS or cave [new_pos[0]][new_pos[1]] == BATS:
            new_pos = [random.randint(0,GRID_WIDTH-1), random.randint(0, GRID_HEIGHT -1)]
            
        cave[pos[0]] [pos[1]] = EMPTY    
        cave [new_pos[0]][new_pos[1]] = BATS
        print ("bat at: "+str(new_pos))

def reset_game():
    global num_arrows
    populate_cave()
    num_arrows = MAX_ARROWS

def game_over(message):
    global screen
    time.sleep(2.0)
    screen.fill(RED)
    text=font.render(message, 1, (0, 255, 64))
    textrect = text.get_rect()
    textrect.centerx = screen.get_rect().centerx
    textrect.centery = screen.get_rect().centery
    screen.blit(text,textrect)
    pygame.display.flip()
    time.sleep(2.5)
    print (message)
    pygame.quit()
    sys.exit()

def shoot_arrow(pos, direction):
    global num_arrows, player_pos, cave

    hit = False
    
    if num_arrows == 0:
        return False
    num_arrows -= 1
    
    if direction == LEFT:
        if pos[0] > 0:
            if cave [pos[0]-1][pos[1]] == WUMPUS:
                hit = True
    elif direction == RIGHT:
        if pos[0] < GRID_WIDTH-1:
            if cave [pos[0]+1][pos[1]] == WUMPUS:
                hit = True
    elif direction == DOWN:
        if pos[1] < GRID_HEIGHT-1:
            if cave [pos[0]][pos[1]+1] == WUMPUS:
                hit = True
    elif direction == UP:
        if pos[1] > 0:
            if cave [pos[0]][pos[1]-1] == WUMPUS:
                hit = True

    if hit == True:
        game_over("Your aim was true and you have killed the Wumpus!")
        pygame.quit()
        sys.exit()
    else:    
        print ("Your arrow sails into the darkness, never to be seen again....")
        place_wumpus()
    if num_arrows == 0:
        game_over("You are out of arrows.  You have died!")

def check_pygame_events():
    global player_pos
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_LEFT:
             if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                shoot_arrow(player_pos,LEFT)
             elif player_pos[0]>0: 
                player_pos[0]-=1
        elif event.key == pygame.K_RIGHT:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                shoot_arrow(player_pos, RIGHT)
            elif player_pos[0]<GRID_WIDTH-1:
                player_pos[0]+=1
        elif event.key == pygame.K_UP:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                shoot_arrow(player_pos, UP)
            elif player_pos[1]>0:
                player_pos[1]-=1
        elif event.key ==pygame.K_DOWN:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                shoot_arrow(player_pos, DOWN)
            elif player_pos[1]<GRID_HEIGHT-1:
                player_pos[1]+=1 
#======================================================================
#                       Initiilizations area                          =
#======================================================================

pygame.init()
screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE )
pygame.display.set_caption("Hunt the Wumpus")

#load our three images
bat_img = pygame.image.load('images/bat.png')
player_img = pygame.image.load('images/player.png')
wumpus_img = pygame.image.load('images/wumpus.png')

#setup our font
font = pygame.font.Font(None, 36)

#Get iniital game settings
reset_game()


#main game loop
while True:
    check_pygame_events()     
    draw_room(player_pos, screen)
    pygame.display.flip()
    #time.sleep(.5)
    check_room(player_pos)
    
    
    
