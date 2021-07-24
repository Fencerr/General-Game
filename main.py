import Population, cv2
from gameobjects import *
from math import *
from numpy import clip


pygame.display.init()
pygame.font.init()
pygame.mixer.init()

vid = cv2.VideoCapture("FINALelpahnt poacher.mp4")
finalMusic = pygame.mixer.Sound("elpahnt poacher.mp3")
mechanicalSounds = pygame.mixer.Sound("2021-07-24 17-03-43.mp3")

gameFont = pygame.font.Font("Fonts/CUTE_ANIMAL.ttf",40)
menuFont = pygame.font.Font("Fonts/CUTE_ANIMAL.ttf",20)

displayInfo = pygame.display.Info()
setWindowDim((int(displayInfo.current_w / 1), int(displayInfo.current_h / 1)))
window = pygame.display.set_mode(getWindowDim(), pygame.FULLSCREEN|pygame.RESIZABLE|pygame.DOUBLEBUF|pygame.HWACCEL)
pygame.display.set_caption("Poached")

poacherPrice = 100
radarPrice = 50
upgradePrice = 10

menuOptions = ["More Poachers\n"+str(poacherPrice)+" Ivory", "Elephant Radar\n"+str(radarPrice)+" Ivory", "Gun Improvements\n"+str(upgradePrice)+" Ivory"][::-1]
menuImgs = [Texture("morehunters.png"),Texture("radar_elephant.png"),Texture("moreguns.png")][::-1]
running = True
ivory = 0
timeFrame = 1/365*10
pollutants = []
ivoryPerSec = 0
ivoryMul = 1
timer = pygame.time.Clock()
tick = 0
gunUpgrade = 1
tusks = [Texture("Tusk 1.png"),Texture("Tust2.png")]

def nthroot(n,root):
    return n**(1/root)

def addPoachers():
    global timeFrame, ivoryPerSec,ivory, poacherPrice,pollutants
    print("add poachers")
    ivory-=poacherPrice
    if ivory>=0:
        Population.addCO2Emitter(0.0000001 * timeFrame)
        pollutants.append(1)
        ivoryPerSec += 10
    else:
        ivory+=poacherPrice
def elephantRadar():
    global timeFrame, ivoryMul, ivory, radarPrice,pollutants
    print("radar")
    ivory-=radarPrice
    if ivory>=0:
        Population.addCO2Emitter(0.000001 * timeFrame)
        pollutants.append(1)
        ivoryMul += 5
    else:
        ivory+=radarPrice
def increaseCount():
    global ivory, gunUpgrade
    ivory += 1 * gunUpgrade
    Population.kill(gunUpgrade)
def upgradeGun():
    print("upgrade")
    global gunUpgrade, ivory, upgradePrice
    ivory-=upgradePrice
    if ivory>=0:
        gunUpgrade+=3
    else:
        ivory+=upgradePrice

mainClickButton = Button((0.1, 0.5 - 0.15), (0.3, 0.3),
                         Texture("ALIVE_elephant.png"),
                         Texture("ALIVE_elephant.png"),
                         Texture("DEAD_elephant GOOD VERSION.png"), increaseCount)
background = Texture("forest_1.png")
automationSelection = Texture("wooden board.png")
menu = Menu((0.75,0),(0.25,1),automationSelection,images = menuImgs,options = menuOptions,
            actions = [addPoachers,elephantRadar,upgradeGun][::-1],
            args = [[],[],[]])
crosshair = Texture("Crosshair.png")
extinct = False
extinctTransition = False
fadeOut = pygame.Surface(getWindowDim())
fadeOut.fill((0,0,0))
transition = 0
mechanicalSounds.play(loops=-1)
lastBackground = clip(int(floor(len(pollutants) / 50) + 1), 1, 7)
while running:
    allEvents = pygame.event.get()
    fadeOut = pygame.Surface(getWindowDim())
    fadeOut.fill((0, 0, 0))
    if extinct == False:
        dimensions = getWindowDim()
        tick=timer.tick()
        if extinctTransition == True:
            transition += tick
        if pygame.mouse.get_pos()[0] < projection((0.75,0))[0]:
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)
        if extinctTransition == False:
            Population.kill(int(((ivoryPerSec*ivoryMul)/1000*tick)))
            ivory += int(((ivoryPerSec*ivoryMul)/1000*tick))
            mainClickButton.update(allEvents)
        else:
            mainClickButton.update([])
            if clip(int((transition/5000)*255),0,255)==255:
                extinct = True
                mechanicalSounds.stop()
                finalMusic.play()
        mainClickButton.render(window)
        window.blit(gameFont.render("Ivory: " + str(round(ivory,2)), True, (255, 255, 255)), projection((0.5, 0.5)))
        newPop = Population.update()
        if newPop == None:
            extinctTransition = True
            newPop = 0
        if extinctTransition == False:
            window.blit(gameFont.render("Population: " + str(int(newPop)), True, (255, 255, 255)),
                        projection((0.2, 1-0.1)))
        else:
            window.blit(gameFont.render("Population: 0", True, (255, 0, 0)),
                        projection((0.2, 1 - 0.1)))
        mainClickButton.render(window)
        window.blit(gameFont.render("Ivory/Sec: " + str(ivoryPerSec*ivoryMul), True, (255, 255, 255)), projection((0.5, 0.6)))
        menu.update(allEvents)
        menu.draw(menuFont,window)
        if pygame.mouse.get_visible()==False:
            crosshair.render(window,[pygame.mouse.get_pos()[i]-projection((0.05,0.05*dimensions[0]/dimensions[1]))[i] for i in range(2)],projection((0.1,0.1*dimensions[0]/dimensions[1])))
        fadeOut.set_alpha(clip(int((transition/5000)*255),0,255))
        window.blit(fadeOut,(0,0))
        pygame.display.update()
        menuOptions = ["More Poachers\n"+str(round(poacherPrice,2))+" Ivory", "Elephant Radar\n"+str(round(radarPrice,2))+" Ivory", "Gun Improvements\n"+str(round(upgradePrice,2))+" Ivory"][::-1]
        """poacherPrice = int(100*nthroot((ivoryPerSec*ivoryMul)/10+1,1.5))
        radarPrice = int(50*nthroot((ivoryPerSec*ivoryMul)/10+1,1.5))
        upgradePrice = int(10*nthroot((ivoryPerSec*ivoryMul)/10+1,1.5))"""
        menu.setOptions(menuOptions)
        window = pygame.display.set_mode(getWindowDim(), pygame.FULLSCREEN|pygame.RESIZABLE|pygame.DOUBLEBUF|pygame.HWACCEL)
        bgImg = clip(int(floor(len(pollutants) / (1200/7)) + 1), 1, 7)
        if bgImg!=lastBackground:
            background.setImage("forest_" + str(bgImg) + ".png")
        background.render(window, projection((0, 0)), projection((1, 1)))
        poacherPrice = 100 * (nthroot(ivoryPerSec*ivoryMul,1.5)+10)/10
        radarPrice = 50 * (nthroot(ivoryPerSec * ivoryMul,1.5) + 10)/10
        upgradePrice = 10 * (nthroot(ivoryPerSec * ivoryMul,1.5) +10)/10
    elif extinct == True:
        ret,frame = vid.read()
        if ret == True:
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            surf = pygame.transform.scale(pygame.transform.flip(pygame.transform.rotate(pygame.surfarray.make_surface(frame),-90),True,False),getWindowDim())
        window.blit(surf,(0,0))
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
        elif event.type == pygame.VIDEORESIZE:
            setWindowDim((event.w, event.h))
    lastBackground = clip(int(floor(len(pollutants) / 50) + 1), 1, 7)