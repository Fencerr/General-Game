import pygame, Population
from gameobjects import *


pygame.display.init()
pygame.font.init()

arial = pygame.font.SysFont("arial",50)

displayInfo = pygame.display.Info()
setWindowDim((displayInfo.current_w,displayInfo.current_h))

window = pygame.display.set_mode(getWindowDim(),pygame.FULLSCREEN)

running = True
kills = 0
def increaseCount():
    global kills
    kills += 1
    Population.CurrentPopulation -= 1

mainClickButton = Button(projection((0.1,0.1)),projection((0.1,0.1)),
                                     Color((255,255,255)),
                                     Color((128,128,128)),
                                     Color((64,64,64)),increaseCount)

while running:
    allEvents = pygame.event.get()
    mainClickButton.update(allEvents)
    mainClickButton.render(window)
    #Population.update()
    window.blit(arial.render("Kills: "+str(kills),True,(255,255,255)),projection((0.5,0.5)))
    window.blit(arial.render("Population: " + str(Population.getCurrentPopulation()), True, (255, 255, 255)), projection((0.5, 0.4)))
    pygame.display.update()
    window.fill((0,0,0))
    for event in allEvents:
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                running = False