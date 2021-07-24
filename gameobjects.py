import pygame

WINDOW_DIMENSIONS = None

class Texture():
    def __init__(self,image):
        if type(image)==str:
            self.image = pygame.image.load("Sprites/"+image)
        elif type(image)==pygame.Surface:
            self.image = image
    def setImage(self,image):
        self.image = pygame.image.load("Sprites/" + image)
    def render(self,surface,pos,size):
        surface.blit(pygame.transform.scale(self.image,size),pos)

class Color(Texture):
    def __init__(self,rgb):
        surf = pygame.Surface(projection((1,1)))
        surf.fill(rgb)
        super().__init__(surf)

class Button():
    def __init__(self,pos,size,texture,hoverTexture,clickTexture,action,*args):
        self.textures = [texture,hoverTexture,clickTexture]
        self.action = action
        self.actionArgs = args
        self.currentTexture = 0
        self.projPos = pos
        self.projSize = size
        self.pos = projection(self.projPos)
        self.size = projection(self.projSize)
    def update(self,events):
        self.pos = projection(self.projPos)
        self.size = projection(self.projSize)
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

class Menu():
    def __init__(self,pos,size,texture,options=[]):
        self.pos = pos
        self.size = size
        self.texture = texture
        self.options = options
    #def update(self):

def setWindowDim(newVal):
    global WINDOW_DIMENSIONS
    WINDOW_DIMENSIONS = newVal

def getWindowDim():
    return WINDOW_DIMENSIONS

def projection(pos,dimensions=WINDOW_DIMENSIONS):
    global WINDOW_DIMENSIONS
    if dimensions is None:
        dimensions = WINDOW_DIMENSIONS
    return [int(dimensions[i]*pos[i]) for i in range(2)]