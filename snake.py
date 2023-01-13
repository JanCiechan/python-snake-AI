import pygame
import numpy as np
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import time
import random
import math

# Set up the drawing window
# Define constants for the screen width and height
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
pygame.init()
# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        #super(Player, self).__init__()
        self.distance_from_food=500
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.direction=2#0-up 1-down 2-left 3-right
        self.next_x=-1;
        self.reward=0
        self.next_y=0;
        self.eaten=False;
        self.move_delay=0.1;
        self.prev_time=time.time();
        self.game_over=False;
        self.food_coord=[random.randint(0,int(SCREEN_HEIGHT/10)),random.randint(0,int(SCREEN_WIDTH/10))]
        self.score=0
   
        #self.map=np.zeros((int(SCREEN_HEIGHT/10),int(SCREEN_WIDTH/10)))
        #self.map[int(SCREEN_HEIGHT/10/2)][int(SCREEN_WIDTH/10/2)]=1
        self.segments=[[int(SCREEN_HEIGHT/10/2),int(SCREEN_WIDTH/10/2)],[int(SCREEN_HEIGHT/10/2)+1,int(SCREEN_WIDTH/10/2)]]
    def update(self, pressed_key):
            if pressed_key == pygame.K_UP and self.direction!=1:
                self.direction=0
                self.next_x=-1;
                self.next_y=0;
                self.reward=1;
            elif pressed_key == pygame.K_UP and self.direction==1:
                self.game_over=True;
                self.reward=-10
                return
            if pressed_key == pygame.K_DOWN and self.direction!=0:
                self.direction=1
                self.next_x=1;
                self.next_y=0;
                self.reward=1
            elif pressed_key == pygame.K_DOWN and self.direction==0:
                self.game_over=True;
                self.reward=-10
                return
            if pressed_key == pygame.K_LEFT and self.direction!=3:
                self.direction=2
                self.next_x=0;
                self.next_y=-1;
                self.reward=1
            elif pressed_key == pygame.K_LEFT and self.direction==3:
                self.game_over=True;
                self.reward=-10
                return
            if pressed_key == pygame.K_RIGHT and self.direction!=2:
                self.direction=3
                self.next_x=0;
                self.next_y=1;
                self.reward=1
            elif pressed_key == pygame.K_RIGHT and self.direction==2:
                self.game_over=True;
                self.reward=-10
                return
            
            self.move();
            
    def move(self):
        #if(time.time()-self.prev_time>self.move_delay):
            self.reward=0
            next_move=[self.segments[0][0]+self.next_x,self.segments[0][1]+self.next_y]
            #if(next_move[0]*10>SCREEN_HEIGHT or next_move[1]*10>SCREEN_WIDTH or next_move[0]<0 or next_move[1]<0 or next_move in self.segments):
             #   self.game_over=True;
            self.segments.insert(0,next_move)
            if(next_move==self.food_coord):
                self.eaten=True
                self.spawn_food()
                self.score+=1
                self.reward=10
             
                
            if(not self.eaten):
                self.segments.pop()
            self.eaten=False
            self.prev_time=time.time()
            new_distance_from_food=math.sqrt(pow(self.food_coord[0]-next_move[0],2) + pow(self.food_coord[1]-next_move[1],2))
            
            if(new_distance_from_food<self.distance_from_food):
               self.reward=2
              
        
           
            self.distance_from_food=new_distance_from_food
            if next_move in self.segments[1:] or self.out_of_bounds(next_move):
            
                self.game_over=True
                self.reward=-10
            
            #self.score+=1
            
    def spawn_food(self):
        while(self.food_coord in self.segments):
            self.food_coord=[random.randint(2,int(SCREEN_HEIGHT/10)-2),random.randint(2,int(SCREEN_WIDTH/10)-2)]
    def check_collisions(self):
        head=self.segments[0]
        #0-up 1-down 2-left 3-right
       
        points=[[head[0]-1,head[1]],[head[0]+1,head[1]],[head[0],head[1]-1],[head[0],head[1]+1]]
        
        result=[]
        for i in points:
            if i in self.segments or self.out_of_bounds(i):
            
                result.append(True)
            else:
                result.append(False)
       
        return result;
    def out_of_bounds(self,point):
       
        if point[0]<0 or point[0]>(SCREEN_HEIGHT/10):
            return True
        if point[1]<0 or point[1]>(SCREEN_WIDTH/10):
            return True  
        return False
    def food_position(self):
        #0-up 1-down 2-left 3-right
        return [self.food_coord[0] < self.segments[0][0],  #food up
        self.food_coord[0] > self.segments[0][0],  # food down
        self.food_coord[1] < self.segments[0][1],  # food left
        self.food_coord[1] > self.segments[0][1]]  # food right
    def distance_collision(self):
        head=self.segments[0]
        points=[[head[0]-1,head[1]],[head[0]+1,head[1]],[head[0],head[1]-1],[head[0],head[1]+1]]
        result=[0,0,0,0]
        for i in range(len(points)):
            going=True
            while going:
                
                if points[i] not in self.segments and not self.out_of_bounds(points[i]):
                
                    result[i]+=1
                    if(i==0):
                        points[i][0]-=1
                    if(i==1):
                        points[i][0]+=1      
                    if(i==2):
                        points[i][1]-=1
                    if(i==3):
                        points[i][1]+=1

                else:
                    going=False
        result2=[x==max(result) for x in result]
        return result2;

        pass
class python_game():
    def __init__(self):
        
        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Instantiate player. Right now, this is just a rectangle.
        self.player = Player()

        # Variable to keep the main loop running
        self.running = True
        self.clock=pygame.time.Clock()
        # Main loop
    def run(self,direction):
    
            direction=[K_UP,
            K_DOWN,
            K_LEFT,
            K_RIGHT][direction.index(1)]
    
            self.player.update(direction)
            # for loop through the event queue
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == KEYDOWN:
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == K_ESCAPE:
                        running = False
                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == QUIT:
                    running = False
            #pressed_keys = pygame.key.get_pressed()
            
            
            # Fill the screen with black
            self.screen.fill((0, 0, 0))
        #   for i in range(len(player.map[0])):
        #        for j in range(len(player.map)):
        #           if(player.map[j][i]==1):
        #                screen.blit(player.surf,pygame.Rect(i*10,j*10,10,10))
            for i in self.player.segments:
                self.screen.blit(self.player.surf,pygame.Rect(i[1]*10,i[0]*10,10,10))
            pygame.draw.circle(self.screen, (0, 0, 255), (self.player.food_coord[1]*10+5, self.player.food_coord[0]*10+5), 5)
            

            # Update the display
            pygame.display.flip()
            if(self.player.game_over):
                self.running=False;
            # Get the set of keys pressed and check for user input
            return self.player.reward, self.player.game_over, self.player.score
