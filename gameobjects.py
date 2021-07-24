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
    def get_size(self):
        return self.image.get_size()

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
    def __init__(self,pos,size,texture,images = [],options=[],actions = [], args = []):
        self.pos = pos
        self.size = size
        self.texture = texture
        self.options = options
        self.images = images
        self.rects = []
        self.actions = actions
        self.args = args
    def update(self,events):
        self.rects = []
        for i in range(len(self.options)):
            self.rects.append(pygame.Rect(*projection((self.pos[0],self.pos[1]+(1/len(self.options))*i+0.2)),*projection((0.25,0.1))))
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for index,rect in enumerate(self.rects):
                        if rect.collidepoint(*pygame.mouse.get_pos()):
                            self.actions[index](*self.args[index])
    def setOptions(self,newOptions):
        self.options = newOptions
    def draw(self,font: pygame.font.Font,surface: pygame.Surface):
        self.texture.render(surface,projection(self.pos),projection(self.size))
        for i in range(len(self.options)):
            if len(self.images)>=i+1:
                self.images[i].render(surface,(self.rects[i].x+projection((0.1,0))[0]-projection((0.06,0.1))[0],self.rects[i].y),projection((0.05,0.05*WINDOW_DIMENSIONS[0]/WINDOW_DIMENSIONS[1])))
                #surface.blit(self.images[i],(self.rects[i].x-projection((0.01,0))[0],self.rects[i].y))
            for ind,line in enumerate(self.options[i].split("\n")):
                surface.blit(font.render(line,True,(255,255,255)),(self.rects[i].x+projection((0.1,0))[0],self.rects[i].y+projection((0.02*ind,0))[0]))



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