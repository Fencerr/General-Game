import pygame, Population, gameobjects

pygame.display.init()
pygame.font.init()

arial = pygame.font.SysFont("arial",50)

displayInfo = pygame.display.Info()
dimensions = (displayInfo.current_w,displayInfo.current_h)

window = pygame.display.set_mode(dimensions,pygame.FULLSCREEN)


running = True
kills = 0
def increaseCount():
    global kills
    kills += 1
mainClickButton = gameobjects.Button((100,100),(100,100),
                                     gameobjects.Color((255,255,255)),
                                     gameobjects.Color((128,128,128)),
                                     gameobjects.Color((64,64,64)),increaseCount)

while running:
    allEvents = pygame.event.get()
    mainClickButton.update(allEvents)
    mainClickButton.render(window)
    window.blit(arial.render(str(kills),True,(255,255,255)),(500,300))
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