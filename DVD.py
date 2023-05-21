import pygame as p, pygame_widgets as pw, random as r, time as t, sys, tkinter as tk, os
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button

def rp(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def checkIn(txt, min, max):
    try:
        txt = float(txt)
        if txt > max or txt < min:
            raise Exception("input out of bounds")
    except Exception as e:
        print(e)
        return False
    return True

def submit(id, min, max):
    if id == 's':
        if checkIn(speedL.getText(), min, max):
            speed.setValue(float(speedL.getText()))
        else:
            if str(speedL.getText()).lower() == 'fast':
                speed.max = 120
                speed.setValue(120)
            elif str(speedL.getText()).lower() == 'slow':
                speed.min = .01
                speed.setValue(.01)
            else:
                speedL.setText(speed.getValue())
    elif id == 'f':
        if checkIn(fpsL.getText(), min, max):
            fpsS.setValue(float(fpsL.getText()))
        else:
            fpsL.setText(fpsS.getValue())

def save():
    saveF = open(rp('./save.dvd'), 'w')
    for i in [speed.getValue(), '\n', fpsS.getValue()]:
        saveF.write(str(i))
    saveF.close()
    print('saved')

def openSave():
    print('opening...')
    saveF = open(rp('./save.dvd'), 'r')

    saveLines = []

    for line in saveF:
        saveLines.append(line)
    
    speed.setValue(float(saveLines[0]))
    speedL.setText(speed.getValue())
    fpsS.setValue(float(saveLines[1]))
    fpsL.setText(fpsS.getValue())
    altSpeed = 'n'

    if not checkIn(float(saveLines[0]), .5, 30):
        if float(saveLines[0]) > 30:
            altSpeed = 'f'
            speed.max = 120
            speedL.setText('fast')
        else:
            altSpeed = 's'
            speed.min = .01
            speedL.setText('slow')
    return altSpeed

def reset():
    speed.setValue(1.0)
    fpsS.setValue(60)

p.init() #Initialize Pygame
Font = p.font.Font(rp('dvdFont.ttf'), 25) #initializes font
bigFont = p.font.Font(rp('dvdFont.ttf'), 35)
width, height = 640, 480 #Initial screen width & height
screen = p.display.set_mode((width, height), p.RESIZABLE) #Sets screen to resizable mode
speed = Slider(screen, 100, 50, 800, 20, min=.5, max=30, step=.25, initial=1, colour=(174, 235, 230))
speed.hide()
speedL = TextBox(screen, 100, 80, 50, 30, fontSize=20, radius=10, onSubmit=submit, onSubmitParams=('s', .5, 30), borderThickness=1, colour=(174, 235, 230))
speedL.setText('1.0')
speedL.hide()
fpsS = Slider(screen, 100, 200, 800, 20, min=5, max=180, step=1, initial=60, colour=(174, 235, 230))
fpsS.hide()
fpsL = TextBox(screen, 100, 230, 40, 30, fontSize=20, radius=10, onSubmit=submit, onSubmitParams=('f', 5, 180), borderThickness=1, colour=(174, 235, 230))
fpsL.setText('60')
fpsL.hide()
resetB = Button(screen, 100, 300, 50, 30, text='Reset', onClick=reset)
resetB.hide()
altSpeed = openSave()
os.environ['SDL_VIDEO_CENTERED'] = '1'
x, y, vel = 0, 0, [speed.getValue(), speed.getValue()] #Makes coordinates and velocity
showInfo = False #sets bool to show display info
fullscr = False #sets bool to toggle full screen
iter = False #sets iteration bool for fullscreen toggles
catch = False #sets catch bool for fullscreen toggles
showHelp = False #sets the bool to bring up the help menu
settings = False #sets bool to toggle the settings menu
showMenuHelp = True #sets the bool to toggle the --Press H for help--
c = 0 #sets counter for corner hits
h = 0 #sets counter for total hits
corners = [(width-29, height-19), (29, 19), (width-29, 19), (29, height-19)] #defiones list of all corner coordinates
helpmsg = ["----Help----", "F3: Show live in-game information", "F11: Fullscreen toggle", "R: set the logo to the center of the screen", "H: Toggle this menu", "S: Open settings"] #defines list of lines in the help message
DVD = p.image.load(rp('./sprites/w.png')) #Loads a sprite
DVDRECT = DVD.get_rect() #Makes object for the sprites to be loaded onto
p.display.set_caption('DVD')#Sets executable capton
fps = fpsS.getValue() #sets FPS
clock = p.time.Clock() #sets FPS clock
more = Font.render("--Press H for help--", True, (255, 255, 255)) #makes default on boot helper
morerect = more.get_rect() #makes surface for default on boot helper
run = True
x, y = r.choice([570, 571, 572]), r.choice([420, 421, 422]) #sets the start location
counter = 0

#Loads in sprites
wht = p.image.load(rp('./sprites/w.png'))
blu = p.image.load(rp('./sprites/b.png'))
pnk = p.image.load(rp('./sprites/p2.png'))
pur = p.image.load(rp('./sprites/p.png'))
grn = p.image.load(rp('./sprites/g.png'))
org = p.image.load(rp('./sprites/o.png'))
ylw = p.image.load(rp('./sprites/y.png'))
p.display.set_icon(wht)

def get_info():
    """
    Function for getting in game live information
    """
    info = p.display.Info() #creates object to get information


    curPosX, curPosY = DVDRECT.center[0], DVDRECT.center[1] #gets current position of logo
    curW, curH = info.current_w, info.current_h #gets current width and height of window
    fps = round(clock.get_fps())#gets current fps (in interger)

    #gets current color of the DVD logo
    if DVD == wht:
        color = "Color: White"
    if DVD == blu:
        color = "Color: Blue"
    if DVD == pnk:
        color = "Color: Pink"
    if DVD == pur:
        color = "Color: Purple"
    if DVD == grn:
        color = "Color: Green"
    if DVD == org:
        color = "Color: Orange"
    if DVD == ylw:
        color = "Color: Yellow"

    hits = "Total hits: "+str(h) #gets total hits
    corner = "Corner hits: "+str(c) #gets corner hits

    return ["DVD X: "+str(curPosX)+" Y: "+str(curPosY), "Screen Width: "+str(curW)+" Height: "+str(curH), "FPS: "+str(fps), hits, corner, color]

def hit_edge(xy):
    """
    Function for when logo hits the edge
        xy: int, expects 1 if horizontal edge is hit and 0 if vertical edge is hit.
    """
    vel[xy] = -vel[xy] #"Bounces" logo of the edge
    DVD = r.choice([wht, blu, pnk, pur, grn, org, ylw]) #sets logo to new random color
    p.display.set_icon(DVD) #sets window icon to cureent logo color
    return DVD

def textHollow(font, message, fontcolor):
    notcolor = [c^0xFF for c in fontcolor]
    base = font.render(message, 0, fontcolor, notcolor)
    size = base.get_width() + 2, base.get_height() + 2
    img = p.Surface(size, 16)
    img.fill(notcolor)
    base.set_colorkey(0)
    img.blit(base, (0, 0))
    img.blit(base, (2, 0))
    img.blit(base, (0, 2))
    img.blit(base, (2, 2))
    base.set_colorkey(0)
    base.set_palette_at(1, notcolor)
    img.blit(base, (1, 1))
    img.set_colorkey(notcolor)
    return img

def textOutline(font, message, fontcolor, outlinecolor):
    base = font.render(message, 0, fontcolor)
    outline = textHollow(font, message, outlinecolor)
    img = p.Surface(outline.get_size(), 16)
    img.blit(base, (1, 1))
    img.blit(outline, (0, 0))
    img.set_colorkey(0)
    return img

while run:
    events = p.event.get()
    for event in events:
        #Exits if user closes window
        if event.type == p.QUIT:
            print("exiting")
            run = False

        if event.type == p.KEYUP:
            #toggles info menu

            if event.key == p.K_ESCAPE:
                if showMenuHelp:
                    showMenuHelp = False
                elif showHelp:
                    showHelp = False
                else:
                    print("exiting")
                    run = False

            if event.key == p.K_F3:
                showInfo = not showInfo

            #toggles fullscreen
            if event.key == p.K_F11:
                if not fullscr:
                    fullscr = True
                    screen = p.display.set_mode((0, 0), p.FULLSCREEN)
                else:
                    fullscr = False
                    screen = p.display.set_mode((width-20, height-80), p.RESIZABLE)

            #resets the logo to the center of the window
            if event.key == p.K_r:
                info = p.display.Info()
                x, y = round(info.current_w/2), round(info.current_h/2)

            #toggles help menu
            if event.key == p.K_h:
                showHelp = not showHelp
                showMenuHelp = False

            #toggles settings
            if event.key == p.K_s:
                if not speedL.selected and not fpsL.selected:
                    settings = not settings

                if settings:
                    speed.show()
                    speedL.show()
                    fpsS.show()
                    fpsL.show()
                    resetB.show()
                else:
                    speed.hide()
                    speedL.hide()
                    fpsS.hide()
                    fpsL.hide()
                    resetB.hide()

    src = p.display.Info()
    width, height = src.current_w, src.current_h
            
    #Makes new coordinates:
    x += vel[0]
    y += vel[1]

    #checks if logo hits a corner
    if (x, y) in corners:
        print("corner")
        c += 1

    #Checks if logo hits a wall
    if x > width-30:
        print("right")
        DVD = hit_edge(0)
        h += 1 #increases hit counter
        x = width-30
        
    if x < 30:
        print("left")
        DVD = hit_edge(0)
        h += 1 #increases hit counter
        x = 30
        
    if y > height-20:
        print("bottom")
        DVD = hit_edge(1)
        h += 1 #increases hit counter
        y = height-20

    if y < 20:
        print("top")
        DVD = hit_edge(1)
        h += 1 #increases hit counter
        y = 20

    screen.fill((0, 0, 0)) #redraws black background
    DVDRECT.center = (x, y) #moves the logo
    screen.blit(DVD, DVDRECT) #Updates logo
    Iy = 9 #sets text starting Y coordinate

    #shows live info menu
    if showInfo:
        info = get_info()
        for i in info:
            curIn = Font.render(i, True, (255,255,255))
            curInRect = curIn.get_rect()
            curInRect.center = (round(curInRect.w/2), Iy)
            screen.blit(curIn, curInRect)
            Iy += 18

    #shows help menu
    if showHelp:
        for i in helpmsg:
            help = Font.render(i, True, (255, 255, 255))
            helprect = help.get_rect()
            helprect.center = (round(helprect.w/2), Iy)
            screen.blit(help, helprect)
            Iy += 18
    else:
        #shows default on boot helper
        if showMenuHelp:
            morerect.center = (round(morerect.w/2), Iy)
            screen.blit(more, morerect)
            counter += 1

    #displays settings menu
    if settings:
        bkg = p.Surface((width, height)) #creates and draws transparent background for menu
        bkg.set_alpha(50)
        bkg.fill((200, 222, 221))
        screen.blit(bkg, (0,0))

        spTxt = bigFont.render('Speed', True, (255,255,255))
        spRect = spTxt.get_rect()
        spRect.center = (round(width/2), 25)
        screen.blit(spTxt, spRect)

        fpTxt = bigFont.render('FPS', True, (255,255,255))
        fpRect = fpTxt.get_rect()
        fpRect.center = (round(width/2), 175)
        screen.blit(fpTxt, fpRect)

        speed.setWidth(width-200)
        speedL.setX(int(round(width/2))-int(round(speedL.getWidth()/2)))
        fpsS.setWidth(width-200)
        fpsL.setX(int(round(width/2))-int(round(fpsL.getWidth()/2)))
        resetB.setX(int(round(width/2))-int(round(resetB.getWidth()/2)))

        if abs(vel[0]) != speed.getValue():
            if speed.getValue() > 30 and altSpeed != 'f':
                altSpeed = 'f'
                speedL.setText('fast')
            elif speed.getValue() > 30 and altSpeed == 'f':
                speed.setValue(30)
                speed.max = 30
                altSpeed = 'n'
            elif speed.getValue() < .5 and altSpeed != 's':
                altSpeed = 's'
                speedL.setText('slow')
            elif speed.getValue() < .5 and altSpeed == 's':
                speed.setValue(.5)
                speed.min = .5
                altSpeed = 'n'
            else:
                altSpeed = 'n'
                speed.min = .5
                speed.max = 30
                speedL.setText(speed.getValue())
        
        if fps != fpsS.getValue():
            fpsL.setText(fpsS.getValue())
            fps = fpsS.getValue()

        if vel[0] < 0:
            vel[0] = -(speed.getValue())
        else:
            vel[0] = speed.getValue()

        if vel[1] < 0:
            vel[1] = -(speed.getValue())
        else:
            vel[1] = speed.getValue()

    if counter >= fps*5:
        showMenuHelp = False
        counter = 0
        
    pw.update(events)
    p.display.update() #updates screen
    clock.tick(fps) #updates fps clock

save()
p.quit()