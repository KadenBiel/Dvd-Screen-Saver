import pygame as p, random as r, time as t, sys, tkinter as tk, os

def rp(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

os.environ['SDL_VIDEO_CENTERED'] = '1'
width, height = 640, 480 #Initial screen width & height
x, y, vel = 0, 0, [1, 1] #Makes coordinates and velocity
showInfo = False #sets bool to show display info
fullscr = False #sets bool to toggle full screen
iter = False #sets iteration bool for fullscreen toggles
catch = False #sets catch bool for fullscreen toggles
showHelp = False #sets the bool to bring up the help menu
showMenuHelp = True #sets the bool to toggle the --Press H for help--
c = 0 #sets counter for corner hits
h = 0 #sets counter for total hits
corners = [(width-29, height-19), (29, 19), (width-29, 19), (29, height-19)] #defiones list of all corner coordinates
helpmsg = ["----Help----", "F3: Show live in-game information", "F11: Fullscreen toggle", "r: set the logo to the center of the screen", "h: Toggle this menu"] #defines list of lines in the help message
DVD = p.image.load(rp('./sprites/w.png')) #Loads a sprite
DVDRECT = DVD.get_rect() #Makes object for the sprites to be loaded onto
p.display.set_caption('DVD')#Sets executable capton
screen = p.display.set_mode((width, height), p.RESIZABLE) #Sets screen to resizable mode
fps = 90 #sets FPS
clock = p.time.Clock() #sets FPS clock
p.init() #Initialize Pygame
Font = p.font.Font(rp('dvdFont.ttf'), 18) #initializes font
more = Font.render("--Press H for help--", True, (255, 255, 255)) #makes default on boot helper
morerect = more.get_rect() #makes surface for default on boot helper
run = True

x, y = r.choice([570, 571, 572]), r.choice([420, 421, 422]) #sets the start location

#Loads in sprites
wht = p.image.load(rp('./sprites/w.png'))
blu = p.image.load(rp('./sprites/b.png'))
pnk = p.image.load(rp('./sprites/p2.png'))
pur = p.image.load(rp('./sprites/p.png'))
grn = p.image.load(rp('./sprites/g.png'))
org = p.image.load(rp('./sprites/o.png'))
ylw = p.image.load(rp('./sprites/y.png'))
p.display.set_icon(wht)

def new_color():
    """
    Function for getting random colors
    """
    return r.choice([wht, blu, pnk, pur, grn, org, ylw])

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

while run:
    for event in p.event.get():
        #Exits if user closes window
        if event.type == p.QUIT:
            print("exiting")
            run = False

        if event.type == p.KEYUP:
            #toggles info menu
            if event.key == p.K_F3:
                showInfo = not showInfo

            #toggles fullscreen
            if event.key == p.K_F11:
                if not fullscr:
                    fullscr = True
                    iter = False
                    root = tk.Tk()
                    scrw = root.winfo_screenwidth()
                    scrh = root.winfo_screenheight()
                    screen = p.display.set_mode((scrw, scrh), p.RESIZABLE)
                    screen = p.display.set_mode((0, 0), p.FULLSCREEN)
                else:
                    fullscr = False
                    screen = p.display.set_mode((640, 480), p.RESIZABLE)

            #resets the logo to the center of the window
            if event.key == p.K_r:
                info = p.display.Info()
                x, y = round(info.current_w/2), round(info.current_h/2)

            #toggles help menu
            if event.key == p.K_h:
                showHelp = not showHelp
                showMenuHelp = False

            #toggles default on boot helper
            if event.key == p.K_s:
                showMenuHelp = not showMenuHelp

        #checks if the user changed window dimensions and adjust the game surface accordingly
        if event.type == p.VIDEORESIZE:
            scrsize = event.size
            screen = p.display.set_mode(scrsize, p.RESIZABLE)
            width, height = scrsize[0], scrsize[1]
            if DVDRECT.center[0] >= width-29:
                y = DVDRECT.center[1]
                x = width-30
                DVDRECT.center = (x, y)
            if DVDRECT.center[1] >= height-19:
                y = height-20
                DVDRECT.center = (x, y)
            corners = [(width-29, height-19), (29, 19), (width-29, 19), (29, height-19)]

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
    if x >= width-29:
        print("right")
        vel[0] = -vel[0] #Makes logo 'bounce' off wall
        DVD = new_color() #Sets a new color to the logo
        p.display.set_icon(DVD) #Sets icon to same color as logo
        h += 1 #Adds one total hit counter
        
    if x <= 29:
        print("left")
        vel[0] = -vel[0]
        DVD = new_color()
        p.display.set_icon(DVD)
        h += 1
        
    if y >= height-19:
        print("bottom")
        vel[1] = -vel[1]
        DVD = new_color()
        p.display.set_icon(DVD)
        h += 1

    if y <= 19:
        print("top")
        vel[1] = -vel[1]
        DVD = new_color()
        p.display.set_icon(DVD)
        h += 1

    DVDRECT.center = (x, y) #moves the logo
    screen.fill((0, 0, 0)) #sets background to black
    screen.blit(DVD, DVDRECT) #Updates logo
    Iy = 6 #sets text starting Y coordinate

    #shows live info menu
    if showInfo:
        info = get_info()
        for i in info:
            curIn = Font.render(i, True, (255,255,255))
            curInRect = curIn.get_rect()
            curInRect.center = (round(curInRect.w/2), Iy)
            screen.blit(curIn, curInRect)
            Iy += 12

    #shows help menu
    if showHelp:
        for i in helpmsg:
            help = Font.render(i, True, (255, 255, 255))
            helprect = help.get_rect()
            helprect.center = (round(helprect.w/2), Iy)
            screen.blit(help, helprect)
            Iy += 12
    else:
        #shows default on boot helper
        if showMenuHelp:
            morerect.center = (round(morerect.w/2), Iy)
            screen.blit(more, morerect)

    #sets to fullscreen 1 frame after surface is resized to the display resolution
    if fullscr and iter and catch:
        screen = p.display.set_mode((0, 0), p.FULLSCREEN)
        catch = False

    #sets bools to make the previous IF statment run in the next frame
    if fullscr and iter != True:
        iter = True
        catch = True

    p.display.update() #updates screen
    clock.tick(fps) #updates fps clock

p.quit()
