import pygame
import random
import time
import sys

#===============================================================================
#                       Gloabls and Constants area                             =
#===============================================================================

#Our screen width and height
SCREEN_WIDTH = SCREEN_HEIGHT= 800

#Number of rooms
GRID_WIDTH = 10
GRID_HEIGHT = 10

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
RED = 138,7,7

NUM_ARROWS = 2

player_pos = [0,0] #tracks where we are in the cave
wumpus_pos = [0,0] #tracks where the Wumpus is
bats_list = []
pits_list = []
arrows_list = []
num_arrows = 1 # Starting arrows
mobile_wumpus = False

#===============================================================================
#                       Functions Area                                         =
#===============================================================================
def check_neighbor_rooms(pos, item_list):
    """ Checks each orthagonal cell next to pos for the requested item
    returns True as soon as the item is found.
    """
    x=0
    y=1
    
    left_cell = [pos[x]-1,pos[y]]
    right_cell = [pos[x]+1,pos[y]]
    top_cell = [pos[x],pos[y]-1]
    bottom_cell = [pos[x],pos[y]+1]
    
    if (left_cell in item_list) or (right_cell in item_list) or (top_cell in item_list) or (bottom_cell in item_list):
        return True
        
def draw_room( pos, screen):
    """ Draws the room in the back buffer
    """
    x=0
    y=1
    
    screen.fill( (0,0,0) ) #paint the background in black

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
        left = SCREEN_WIDTH-(SCREEN_WIDTH*.25)
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
        top = SCREEN_HEIGHT-(SCREEN_WIDTH*.25)
        pygame.draw.rect(screen, BROWN, ((left,top), (80,SCREEN_HEIGHT*.25)), 0)
        
    #find out if bats, pits or a wumpus is near
    bats_near = check_neighbor_rooms(pos, bats_list)
    pit_near = check_neighbor_rooms(pos, pits_list)
    wumpus_near = check_neighbor_rooms(pos, [wumpus_pos, [-1,-1]])
    
    #draw a blood circle if the Wumpus is nearby
    if wumpus_near == True:
        circle_radius = int ((SCREEN_WIDTH//2)*.5)
        pygame.draw.circle(screen, RED, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), circle_radius, 0)

    #draw the pit in black if it is present
    if player_pos in pits_list:
        circle_radius = int ((SCREEN_WIDTH//2)*.5)
        pygame.draw.circle(screen, BLACK, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), circle_radius, 0)
     
    #draw the player
    screen.blit(player_img,(SCREEN_WIDTH//2-player_img.get_width()//2,SCREEN_HEIGHT//2-player_img.get_height()//2))

    #draw the bat imag
    if player_pos in bats_list:
        screen.blit(bat_img,(SCREEN_WIDTH//2-bat_img.get_width()//2,SCREEN_HEIGHT//2-bat_img.get_height()//2))

    #draw the wumpus
    if player_pos == wumpus_pos:
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

    if player_pos in bats_list: #if bats are here, go ahead and flip the display and wait a bit
        pygame.display.flip()
        time.sleep(2.0)
        
def populate_cave():
    global player_pos, wumpus_pos

    #place the player
    player_pos = [random.randint(0,GRID_WIDTH-1), random.randint(0, GRID_HEIGHT -1)]

    # place the wumpus
    place_wumpus()
    
    #place the bats
    for bat in range(0,NUM_BATS):
        place_bat()

    #place the pits
    for pit in range (0,NUM_PITS):
        place_pit()

    #place the arrows
    for arrow in range (0,NUM_ARROWS):
        place_arrow()

    print ("Player at: "+str(player_pos))
    print ("Wumpus at: "+str(wumpus_pos))

def place_wumpus():
    global player_pos, wumpus_pos
    
    wumpus_pos = player_pos
    while (wumpus_pos == player_pos):
        wumpus_pos = [random.randint(0,GRID_WIDTH-1), random.randint(0, GRID_HEIGHT -1)]
    print ("Wumpus at: "+str(wumpus_pos))

def place_bat():
   #place the bats
    bat_pos = player_pos
    while bat_pos == player_pos or (bat_pos in bats_list) or (bat_pos == wumpus_pos) or (bat_pos in pits_list):
        bat_pos = [random.randint(0,GRID_WIDTH-1), random.randint(0, GRID_HEIGHT -1)]
    bats_list.append(bat_pos)
    print ("Bats at: "+str(bat_pos))

def place_pit():
    pit_pos = player_pos
    while (pit_pos == player_pos) or (pit_pos in bats_list) or (pit_pos == wumpus_pos) or (pit_pos in pits_list):
        pit_pos = [random.randint(0,GRID_WIDTH-1), random.randint(0, GRID_HEIGHT -1)]
    pits_list.append(pit_pos)
    print ("Pit at: "+str(pit_pos))

def place_arrow():
    arrow_pos = player_pos
    while (arrow_pos == player_pos) or (arrow_pos in bats_list) or (arrow_pos == wumpus_pos) or (arrow_pos in pits_list):
        arrow_pos = [random.randint(0,GRID_WIDTH-1), random.randint(0, GRID_HEIGHT -1)]
    arrows_list.append(arrow_pos)
    print ("Arrow at: "+str(arrow_pos))
    
def check_room(pos):
    global player_pos, screen, num_arrows
    
    #is there a Wumpus in the room?
    if player_pos == wumpus_pos:
        game_over("You were eaten by a WUMPUS!!!")

    #is there a pit?
    if player_pos in pits_list:
        game_over("You fell into a bottomless pit!!")

    #is there bats in the room?  If so move the player and the bats
    if player_pos in bats_list:
        print("Bats pick you up and place you elsewhere in the cave!")
        screen.fill(BLACK)
        bat_text = font.render("Bats pick you up and place you elsewhere in the cave!", 1, (0, 255, 64))
        textrect = bat_text.get_rect()
        textrect.centerx = screen.get_rect().centerx
        textrect.centery = screen.get_rect().centery
        screen.blit(bat_text,textrect)
        pygame.display.flip()
        time.sleep(2.5)
        
        #move the bats
        new_pos = player_pos
        
        while (new_pos == player_pos) or (new_pos in bats_list) or (new_pos == wumpus_pos) or (new_pos in pits_list):
            new_pos = [random.randint(0,GRID_WIDTH-1), random.randint(0, GRID_HEIGHT -1)]
        bats_list.remove(player_pos)   
        bats_list.append(new_pos)
        print ("bat at: "+str(new_pos))
                
        #now move the player
        new_pos = player_pos # set new_pos equal to the old os so the first test fails
        # Now place the player in a random location
        while (new_pos == player_pos) or (new_pos in bats_list) or (new_pos == wumpus_pos) or (new_pos in pits_list):
            new_pos = [random.randint(0,GRID_WIDTH-1), random.randint(0, GRID_HEIGHT -1)]
        player_pos = new_pos
        print ("player at:"+str(player_pos))

    #is there an arrow in the room?
    if player_pos in arrows_list:
        screen.fill(BLACK)
        text = font.render("You have found an arrow!", 1, (0, 255, 64))
        textrect = text.get_rect()
        textrect.centerx = screen.get_rect().centerx
        textrect.centery = screen.get_rect().centery
        screen.blit(text,textrect)
        pygame.display.flip()
        time.sleep(2.5)
        num_arrows +=1
        arrows_list.remove(player_pos)
            
def reset_game():
    global num_arrows
    populate_cave()
    num_arrows = 1

def game_over(message):
    global screen
    time.sleep(1.0)
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

def move_wumpus():
    global wumpus_pos

    if mobile_wumpus == False:
        return
    
    #move in the x direction
    if player_pos[0] < wumpus_pos[0]:
            wumpus_pos[0] = wumpus_pos[0]-1
    elif player_pos[0] > wumpus_pos[0]:
            wumpus_pos[0] = wumpus_pos[0]+1
    #move in the Y direction
    if player_pos[1] < wumpus_pos[1]:
            wumpus_pos[1] = wumpus_pos[1]-1
    elif player_pos[1] > wumpus_pos[1]:
            wumpus_pos[1] = wumpus_pos[1]+1
    #check x bounds
    if wumpus_pos[0]< 0:
            wumpus_pos[0] = 0
    elif wumpus_pos[0] > GRID_WIDTH -1:
            wumpus_pos[0] = GRID_WIDTH -1
    #check y bounds
    if wumpus_pos[1]< 0:
            wumpus_pos[1] = 0
    elif wumpus_pos[1] > GRID_HEIGHT -1:
            wumpus_pos[1] = GRID_HEIGHT -1
            
    print ("Wumpus moved to:"+str(wumpus_pos))
                   
def shoot_arrow(direction):
    global num_arrows, player_pos

    x=0
    y=1
    hit = False
    
    if num_arrows == 0:
        return False
    num_arrows -= 1
    
    if direction == LEFT:
        arrow_pos = [ player_pos[x]-1, player_pos[y]]
        if arrow_pos == wumpus_pos:
            hit = True
    elif direction == RIGHT:
        arrow_pos = [ player_pos[x]+1, player_pos[y]]
        if arrow_pos == wumpus_pos:
            hit = True
    elif direction == DOWN:
        arrow_pos = [ player_pos[x], player_pos[y]+1]
        if arrow_pos == wumpus_pos:
            hit = True
    elif direction == UP:
        arrow_pos = [ player_pos[x], player_pos[y]-1]
        if arrow_pos == wumpus_pos:
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
        elif event.key ==pygame.K_LEFT:
             if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                shoot_arrow(LEFT)
             elif player_pos[0]>0: 
                player_pos[0]-=1
                move_wumpus()
        elif event.key == pygame.K_RIGHT:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                shoot_arrow(RIGHT)
            elif player_pos[0]<GRID_WIDTH-1:
                player_pos[0]+=1
                move_wumpus()
        elif event.key == pygame.K_UP:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                shoot_arrow(UP)
            elif player_pos[1]>0:
                player_pos[1]-=1
                move_wumpus()
        elif event.key ==pygame.K_DOWN:
            if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                shoot_arrow(DOWN)
            elif player_pos[1]<GRID_HEIGHT-1:
                player_pos[1]+=1
                move_wumpus()

def print_instructoions():
    print(
    '''
                             Hunt The Wumpus!
This is the game of "Hunt the Wumpus".  You have been cast into a
dark 10X10 room cave with a fearsome Wumpus.  The only way out is
to kill the Wumpus.  To that end you have a bow with one arrow.
You might find more arrows from unlucky past Wumpus victims in the
cave.  There are other dangers in the cave, specifcally bats and
bottomless pits.

    * If you run out of arrows you die.
    * If you end up in the same room with the Wumpus you die.
    * If you fall into a bottomless pit you die.
    * If you end up in a room with bats they will pick you up
      and deposit you in a random location.

If you are near the Wumpus you will see the bloodstains on the walls.
If you are near bats you will hear them and if you are near a bottomless
pit you will feel the air flowing down it.

Use the arrow keys to move.  Press the <SHIFT> key and an arrow key to
fire your arrow.
    '''
    )
#===============================================================================
#                       Initiilizations area                                   =
#===============================================================================

print_instructoions()
input("Press <ENTER> to begin.")
pygame.init()
screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE )
pygame.display.set_caption("Hunt the Wumpus")

#load our three images
bat_img = pygame.image.load('images/bat.png')
player_img = pygame.image.load('images/player.png')
wumpus_img = pygame.image.load('images/wumpus.png')
arrow_img = pygame.image.load('images/arrow.png')

#setup our font
font = pygame.font.Font(None, 36)

#Get iniital game settings
reset_game()

#===============================================================================
#                       Main Game Loop                                         =
#===============================================================================
while True:
    check_pygame_events()     
    draw_room(player_pos, screen)
    pygame.display.flip()   
    check_room(player_pos)
    

    
    
    
