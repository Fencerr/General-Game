import pygame

pygame.display.init()
displayInfo = pygame.display.Info()

dimensions = (displayInfo.current_w,displayInfo.current_h)
window = pygame.display.set_mode(dimensions,pygame.FULLSCREEN)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                running = False