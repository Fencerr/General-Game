import pygame

class Texture():
    def __init__(self,image):
        if type(image)==str:
            self.image = pygame.image.load(image)
        elif type(image)==pygame.Surface:
            self.image = image
    def render(self,surface,pos,size):
        surface.blit(pygame.transform.scale(self.image,size),pos)

class Color(Texture):
    def __init__(self,rgb):
        surf = pygame.Surface((100,100))
        surf.fill(rgb)
        super().__init__(surf)

class Button():
    def __init__(self,pos,size,texture,hoverTexture,clickTexture,action,*args):
        self.textures = [texture,hoverTexture,clickTexture]
        self.action = action
        self.actionArgs = args
        self.size = size
        self.currentTexture = 0
        self.pos = pos
    def update(self,events):
        if pygame.Rect(*self.pos,*self.size).collidepoint(*pygame.mouse.get_pos()):
            self.currentTexture = 1
        else:
            self.currentTexture = 0
        if pygame.mouse.get_pressed()[0] and self.currentTexture == 1:
            self.currentTexture = 2
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.currentTexture == 2:
                    self.action(*self.actionArgs)
    def render(self,window):
        self.textures[self.currentTexture].render(window,self.pos,self.size)

def projection(pos,dimensions):
    return [int(dimensions[i]*pos[i] for i in range(2))]