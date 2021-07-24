import pygame
from numpy import clip
# These are the import statements, both pygame and numpy are used.

WINDOW_DIMENSIONS = None
# Window size for the game.

class Texture():
    def __init__(self,image):
        if type(image)==str:
            self.image = pygame.image.load("Sprites/"+image)
        elif type(image)==pygame.Surface:
            self.image = image
    def setImage(self,image):
        self.image = pygame.image.load("Sprites/" + image)
    def render(self,surface,pos,size, rotation = 0,alpha=255):
        rotationSurf = pygame.transform.rotate(pygame.transform.scale(self.image,size),rotation)
        rotationSurf.set_alpha(alpha)
        surface.blit(rotationSurf,pos)
    def get_size(self):
        return self.image.get_size()
    
# The color class below is for 
class Color(Texture):
    def __init__(self,rgb):
        surf = pygame.Surface(projection((1,1)))
        surf.fill(rgb)
        super().__init__(surf)

# The class below is the blueprint for all the buttons used, as seen in the UI of the game, for things such as the "Gun Improvements" and the "More Poachers" button. 
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
        self.clickAnimation = False
        self.dead = []
        self.internalClock = pygame.time.Clock()
        self.currentTime = 0
        self.lastClickTime = 0
    def update(self,events):
        self.currentTime += self.internalClock.tick()
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
                    self.dead.append(self.currentTime)
        if self.currentTexture == 2:
            self.currentTexture = 1
    def render(self,window):
        for dead in self.dead:
            offset = 1-((1-(clip(self.currentTime - dead,0,500)/500))**2)
            self.textures[2].render(window,[self.pos[i]+offset*projection((0.1,0.1))[0] for i in range(2)],self.size,rotation = offset*-45,alpha=255-offset*255)
        self.dead = [dead for dead in self.dead if self.currentTime - dead<500]
        self.textures[self.currentTexture].render(window,self.pos,self.size)

# The class below is the blueprint for the menu of the game, basically structuring the interface for the elephant image, etc. etc. 
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
        for index,rect in enumerate(self.rects):
            if pygame.mouse.get_pressed()[0] and rect.collidepoint(*pygame.mouse.get_pos()):
                self.actions[index](*self.args[index])
    def setOptions(self,newOptions):
        self.options = newOptions
    def draw(self,font: pygame.font.Font,surface: pygame.Surface):
        self.texture.render(surface,projection(self.pos),projection(self.size))
        for i in range(len(self.options)):
            if len(self.images)>=i+1:
                self.images[i].render(surface,(self.rects[i].x+projection((0.1,0))[0]-projection((0.06,0.1))[0],self.rects[i].y),projection((0.05,0.05*WINDOW_DIMENSIONS[0]/WINDOW_DIMENSIONS[1])))
            for ind,line in enumerate(self.options[i].split("\n")):
                surface.blit(font.render(line,True,(255,255,255)),(self.rects[i].x+projection((0.1,0))[0],self.rects[i].y+projection((0.02*ind,0))[0]))


# The method below sets the dimensions for the game window to the inputted parameter newVal. 
def setWindowDim(newVal):
    global WINDOW_DIMENSIONS
    WINDOW_DIMENSIONS = newVal

# The method below returns the dimensions of the game window. 
def getWindowDim():
    return WINDOW_DIMENSIONS


def projection(pos,dimensions=WINDOW_DIMENSIONS):
    global WINDOW_DIMENSIONS
    if dimensions is None:
        dimensions = WINDOW_DIMENSIONS
    return [int(dimensions[i]*pos[i]) for i in range(2)]
