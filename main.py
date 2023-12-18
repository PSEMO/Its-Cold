import pygame
import random
import math
import numpy as np
from sys import exit

width = 1080
height = 520

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("It's Cold!")

clock = pygame.time.Clock()

framerate = 150

GameState = 0 #*************************************************CHANGE ON BUILD

StoryStopwatch = 0
StoryTimer = 5 #*************************************************CHANGE ON BUILD
CurrentStoryState = 0
StoryGoingDark = False

MouseClicked = False
LavashSelected = False
PlateSelected = False
Food1Selected = False
Food3Selected = False
SwordSelected = False


CLavash = (False, 0, 0)
CPlate = (False, 0, 0)
CFood1 = (False, 0, 0)
CFood2 = (False, 0, 0)
CFood3 = (False, 0, 0)
CSword = (750, 380)
CCut = (False, 985, 140)

dönerCounter = 0

LastMouseX = 0

MaxDay = 3
MaxMoney = 150
Day = 1
Money = 0
Time = 8

alphaForState3 = 255

Lost1 = False
Continue1 = False

CCutRight = True

#------------
#region read images
def GiveFile(input):
    return input

icon = pygame.image.load(GiveFile('icon.png'))
pygame.display.set_icon(icon)

image1 = pygame.image.load(GiveFile('image1.png'))
image_rect = image1.get_rect()
image_rect.center = (width / 2, height / 2) # center the image on the screen

image2 = pygame.image.load(GiveFile("image2.png"))
image_rect2 = image2.get_rect()
image_rect2.center = (width / 2, height / 2) # center the image on the screen

image3 = pygame.image.load(GiveFile("image3.png"))
image_rect3 = image3.get_rect()
image_rect3.center = (width / 2, height / 2) # center the image on the screen

image4 = pygame.image.load(GiveFile("image4.png"))

image5 = pygame.image.load(GiveFile("image5.png"))

image6 = pygame.image.load(GiveFile("image6.png"))

image7 = pygame.image.load(GiveFile("image7.png"))

store = pygame.image.load(GiveFile("Store.png"))
store_rect = store.get_rect()
store_rect.center = (width / 2, height / 2) # center the image on the screen

plate = pygame.image.load(GiveFile("Plate.png"))
plate_rect = plate.get_rect()

lavash = pygame.image.load(GiveFile("Lavash.png"))
lavash_rect = lavash.get_rect()

food1 = pygame.image.load(GiveFile("FoodLv1.png"))
food1_rect = food1.get_rect()

food2 = pygame.image.load(GiveFile("FoodLv2.png"))
food2_rect = food2.get_rect()

food3 = pygame.image.load(GiveFile("FoodLv3.png"))
food3_rect = food3.get_rect()

Sword = pygame.image.load(GiveFile("Sword.png"))
Sword_rect = Sword.get_rect()

Cut = pygame.image.load(GiveFile("cut.png"))
Cut_rect = Cut.get_rect()
#endregion
#---------------------------------
#region Snowflake class
slowestSnowflake = 50
SnowFlakeVertical = 250
class Snowflake:

    def __init__(self):
        # Initialize the attributes of the snowflake
        self.x = 0 # The x coordinate
        self.y = 0 # The y coordinate
        self.speedY = 0 # The falling speed
        self.radius = 0 # The radius of the circle
        Snowflake.randomizeSnowflake(self)

    def update(self, dt):
        # Update the position of the snowflake
        self.y += self.speedY * dt # Move down by the speed
        self.x += SnowFlakeVertical * dt # Move down by the speed
        # If the snowflake reaches the bottom of the screen, reset its position
        if self.y > height or self.x > width:
            Snowflake.randomizeSnowflake(self)
        # Draw self
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)
        
    def randomizeSnowflake(obj):
        obj.x = random.randint(int(-(slowestSnowflake / height) * SnowFlakeVertical)
                               - width, width) # Random x coordinate
        obj.y = random.randint(-height, 0) # Random y coordinate
        obj.speedY = random.randint(slowestSnowflake, 250) # Random speed
        obj.radius = random.randint(1, 2) # Random radius
#endregion
#---------------------------------
def degree_to_position(degree):
    # Convert degree to radian
    radian = degree * math.pi / 180
    # Calculate x and y coordinates
    x = math.cos (radian)
    y = math.sin (radian)
    # Return coordinates as a tuple
    return (x, y)
#---------------------------------
def Similarity(n1, n2):
    """ calculates a similarity score between 2 numbers """
    if n1 + n2 == 0:
        return 1
    else:
        return 1 - abs(n1 - n2) / (n1 + n2)
#---------------------------------
def draw_text(surface, text, size, color, x, y, relative):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surf = font.render(str(text), True, color)
    text_rect = text_surf.get_rect()

    if(relative == 'center'):
        text_rect.center = (x, y)
    
    surface.blit(text_surf, text_rect)
#---------------------------------
def disBetweenPoints(P1, P2):
    dis = (P1[1] - P2[1])**2 + (P1[0] - P2[0])**2
    return dis
#---------------------------------

#Create an empty list to store the snowflakes
snowflakes = []
#Fill snowflakes
def CreateSnow():
    for i in range(1000):
        temp = Snowflake()
        snowflakes.append(temp)
#------------
        
CreateSnow()

#Update()
while 1:

    #count the time frame took and assign it to ms
    ms = clock.tick(framerate)
    deltaTime = ms / 1000
    #------------

    #resets screen
    screen.fill((0, 0, 0))
    #------------

    #detect events including inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    #------------

    #get the user input
    keys = pygame.key.get_pressed()
    #------------

    if GameState == 0:
        draw_text(screen, "Press enter key to start",
                  40, (255, 255, 255), width / 2, height / 2, "center")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                GameState = 1
    elif GameState == 1:
        if not StoryGoingDark:
            StoryStopwatch += deltaTime
            if StoryStopwatch > StoryTimer:
                StoryStopwatch = StoryTimer
                StoryGoingDark = True
        else:
            StoryStopwatch -= deltaTime
            if StoryStopwatch < 0:
                StoryStopwatch = 0
                CurrentStoryState += 1
                StoryGoingDark = False
            
        alpha = (StoryStopwatch / StoryTimer) * 255

        if CurrentStoryState == 0:
            CurrentImg = image1
        elif CurrentStoryState == 1:
            if Lost1:
                break
            CurrentImg = image2
        elif CurrentStoryState == 2:
            CurrentImg = image3
        elif CurrentStoryState == 3:
            GameState = 2
            StoryStopwatch = 0
            CurrentStoryState = 0
            StoryGoingDark = False
            if Continue1:
                GameState = 6

        CurrentImg.set_alpha(alpha)
        screen.blit(CurrentImg, image_rect)
        if CurrentStoryState != 3:
            for snowflake in snowflakes:
                snowflake.update(deltaTime)

    elif GameState == 2:

        Time += deltaTime / 4

        if Time > 24:
            GameState = 3
            if Day == 3:
                GameState = 4

        if Money >= MaxMoney:
            GameState = 5

        for snowflake in snowflakes:
            snowflake.update(deltaTime)
        screen.blit(store, store_rect)

        MousePos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            MouseClicked = True
            if (MousePos[0] > 490 and MousePos[0] < 590 and not CFood1[0] and not CFood2[0]and
                MousePos[1] > 160 and MousePos[1] < 255 and not CLavash[0] and not CFood3[0]
                ):
                LavashSelected = True
            elif (MousePos[0] > 650 and MousePos[0] < 745 and not CFood1[0] and not CFood2[0]and
                  MousePos[1] > 160 and MousePos[1] < 255 and not CPlate[0] and not CFood3[0]
                  ):
                PlateSelected = True
            elif (CLavash[0] and disBetweenPoints([MousePos[0], MousePos[1]], [CLavash[1], CLavash[2]]) < 625
                  ):
                LavashSelected = True
            elif (CPlate[0] and disBetweenPoints([MousePos[0], MousePos[1]], [CPlate[1], CPlate[2]]) < 625
                  ):
                PlateSelected = True
            elif (CFood1[0] and disBetweenPoints([MousePos[0], MousePos[1]], [CFood1[1], CFood1[2]]) < 625
                  ):
                dönerCounter = 0
                Food1Selected = True
            elif (CFood3[0] and disBetweenPoints([MousePos[0], MousePos[1]], [CFood3[1], CFood3[2]]) < 625
                  ):
                dönerCounter = 0
                Food3Selected = True
            elif (CFood2[0] and disBetweenPoints([MousePos[0], MousePos[1]], [CFood2[1], CFood2[2]]) < 625
                  ):
                CFood3 = (True, CFood2[1], CFood2[2])
                CFood2 = (False, 0, 0)
                Food3Selected = True
            elif (disBetweenPoints([MousePos[0], MousePos[1]], [CSword[0], CSword[1] + 75]) < 625
                  ):
                SwordSelected = True
        elif event.type == pygame.MOUSEBUTTONUP:
            MouseClicked = False
            LavashSelected = False
            PlateSelected = False
            Food1Selected = False
            Food3Selected = False
            SwordSelected = False
            if CPlate[0] and CLavash[0]:
                if disBetweenPoints([CPlate[1], CPlate[2]], [CLavash[1], CLavash[2]]) < 900:
                    CFood1 = (True, CPlate[1], CPlate[2])
                    CLavash = (False, 0, 0)
                    CPlate = (False, 0, 0)
            if CFood3[0]:
                if MousePos[0] > 200 and MousePos[1] > 330 and MousePos[0] < 360 and MousePos[1] < 495:
                    CFood3 = (False, 0, 0)
                    Money += 15

        if MouseClicked == True:
            MousePos = pygame.mouse.get_pos()
            if LavashSelected:
                CLavash = (True, MousePos[0], MousePos[1])
            elif PlateSelected:
                CPlate = (True, MousePos[0], MousePos[1])
            elif Food1Selected:
                CFood1 = (True, MousePos[0], MousePos[1])
            elif Food3Selected:
                CFood3 = (True, MousePos[0], MousePos[1])
            elif SwordSelected:
                CSword = (MousePos[0], MousePos[1] - 75)
                if CFood1[0]:
                    if MousePos[0] > 950 and MousePos[1] < 350:
                        dönerCounter += abs(MousePos[0] - LastMouseX)
                        print(dönerCounter)
                    if dönerCounter > 1000:
                        CFood2 = (True, CFood1[1], CFood1[2])
                        CFood1 = (False, 0, 0)
                        CCut = (False, 985, 140)
                        dönerCounter = 0
                    else:
                        if CCutRight:
                            CCut = (True, CCut[1] + deltaTime * 20, CCut[2])
                            if (CCut[1] > 1000):
                                CCut = (True, 1000, CCut[2])
                                CCutRight = False
                        else:
                            CCut = (True, CCut[1] - deltaTime * 20, CCut[2])
                            if (CCut[1] < 970):
                                CCut = (True, 970, CCut[2])
                                CCutRight = True
            
        if CPlate[0]:
            plate_rect.center = (CPlate[1], CPlate[2])
            screen.blit(plate, plate_rect)

        if CLavash[0]:
            lavash_rect.center = (CLavash[1], CLavash[2])
            screen.blit(lavash, lavash_rect)

        if CFood1[0]:
            food1_rect.center = (CFood1[1], CFood1[2])
            screen.blit(food1, food1_rect)

        if CFood2[0]:
            food2_rect.center = (CFood2[1], CFood2[2])
            screen.blit(food2, food2_rect)

        if CFood3[0]:
            food3_rect.center = (CFood3[1], CFood3[2])
            screen.blit(food3, food3_rect)

        if CCut[0] and SwordSelected:
            Cut_rect.center = (CCut[1], CCut[2])
            screen.blit(Cut, Cut_rect)

        if True:
            Sword_rect.center = (CSword[0], CSword[1])
            screen.blit(Sword, Sword_rect)
        
        draw_text(screen, "Day: " + str(Day) + "/" + str(MaxDay) + " - " +
                  "Clock: " + str(int(Time)), 32, (255, 255, 255), width / 2, 20, "center")
        draw_text(screen, "Earning: " + str(int(Money)) + "/" + str(MaxMoney), 32,
                  (255, 255, 255), width / 2, 52, "center")

    elif GameState == 3:
        alphaForState3 -= deltaTime * 100
        draw_text(screen, "Day: " + str(Day) + "/" + str(MaxDay),
                  32, (255, 255, 255, alphaForState3), width / 2, int(height / 2 - 32), "center")
        draw_text(screen, "Earning: " + str(int(Money)) + "/" + str(MaxMoney), 32,
                  (255, 255, 255, alphaForState3), int(width / 2), int(height / 2 + 32), "center")
        if alphaForState3 < 1:
            alphaForState3 = 255
            Day += 1
            Time = 8
            GameState = 2
            Food1Selected = False
            Food3Selected = False
            PlateSelected = False
            SwordSelected = False
            LavashSelected = False
            CFood1 = (False, 0, 0)
            CFood2 = (False, 0, 0)
            CFood3 = (False, 0, 0)
            CLavash = (False, 0, 0)
            CPlate = (False, 0, 0)
            CCut = (False, 985, 140)
            CSword = (750, 380)

    elif GameState == 4:
        Lost1 = True
        image1 = image7
        GameState = 1
        #breaks the loop

    elif GameState == 5:
        Continue1 = True
        image1 = image4
        image2 = image5
        image3 = image6
        GameState = 1
        #jumps to 6

    elif GameState == 6:
        break

    LastMouseX = pygame.mouse.get_pos()[0]
    pygame.display.flip()