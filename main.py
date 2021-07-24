import pygame, Population
from gameobjects import *
from math import *
from numpy import clip


pygame.display.init()
pygame.font.init()

arial = pygame.font.SysFont("arial",50)

displayInfo = pygame.display.Info()
setWindowDim((int(displayInfo.current_w/2),int(displayInfo.current_h/2)))

window = pygame.display.set_mode(getWindowDim(),pygame.RESIZABLE)

running = True
kills = 0
pollutants = [0.0000001/365*10 for i in range(1000)]
[Population.addCO2Emitter(i) for i in pollutants]
def increaseCount():
    global kills
    kills += 1
    Population.kill(1000/365*10)

mainClickButton = Button((0.1,0.5-0.15),(0.3,0.3),
                                     Texture("ALIVE_elephant.png"),
                                     Texture("ALIVE_elephant.png"),
                                     Texture("DEAD_elephant GOOD VERSION.png"),increaseCount)
background = Texture("forest_1.png")
automationSelection = Texture("wooden board.png")
while running:
    allEvents = pygame.event.get()
    mainClickButton.update(allEvents)
    mainClickButton.render(window)
    Population.kill(1000 / 365 * 10)
    window.blit(arial.render("Ivory: "+str(kills),True,(255,255,255)),projection((0.5,0.5)))
    window.blit(arial.render("Population: " + str(Population.update()), True, (255, 255, 255)), projection((0.5, 0.4)))
    automationSelection.render(window,projection((0.75,0)),projection((0.25,1.0)))
    pygame.display.update()
    window = pygame.display.set_mode(getWindowDim(), pygame.RESIZABLE)
    background.setImage("forest_"+str(clip(int(floor(len(pollutants)/10)+1),1,7))+".png")
    background.render(window,projection((0,0)),projection((1,1)))
    for event in allEvents:
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                running = False
        elif event.type == pygame.VIDEORESIZE:
            setWindowDim((event.w, event.h))