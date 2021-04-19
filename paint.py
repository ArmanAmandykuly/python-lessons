import pygame
from threading import Thread
from pygame.locals import * 
pygame.init()
ww,hh = 500,500
canvas = pygame.display.set_mode((ww+100,hh))
insurf = pygame.Surface((ww,hh))
insurf.fill((255,255,255))
pygame.display.set_caption("paint")
pygame.display.set_icon(pygame.image.load("paint.png"))
class Button:
    def __init__(self,x,y,img):
        self.img = pygame.image.load(img+".png")
        self.r = self.img.get_rect(topleft = (x,y))
    def draw(self):
        canvas.blit(self.img,self.r)
    def get_pressed(self):
        return pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0] in range(self.r.x,self.r.x+self.r.w) and pygame.mouse.get_pos()[1] in range(self.r.y,self.r.y+self.r.h)
class Color:
    def __init__(self,x,y,c,h = 50,w = 50):
        self.c = c
        self.r = pygame.Rect(x,y,h,w)
    def draw(self):
        pygame.draw.rect(canvas,self.c,self.r)
    def get_pressed(self):
        return pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0] in range(self.r.x,self.r.x+self.r.w) and pygame.mouse.get_pos()[1] in range(self.r.y,self.r.y+self.r.h)
class Pen:
    def __init__(self,r = 10,c = (0,0,0)):
        self.r = r
        self.c = c
    def draw(self):
        x,y = pygame.mouse.get_pos()
        if x in range(0,ww) and y in range(0,hh):
            pygame.draw.circle(canvas,self.c,(x,y),self.r)
            if pygame.mouse.get_pressed()[0]:
               pygame.draw.circle(insurf,self.c,(x,y),self.r)
class Eraser(Pen):
    def __init__(self,r = 10):
        super().__init__(r,(255,255,255))
    def draw(self):
        x,y = pygame.mouse.get_pos()
        if x in range(0,ww) and y in range(0,hh):
            pygame.draw.rect(canvas,(255,255,255),pygame.Rect(x-self.r,y-self.r,self.r*2,self.r*2))
            if pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(insurf,(255,255,255),pygame.Rect(x-self.r,y-self.r,self.r*2,self.r*2))
class Rect:
    def __init__(self,r = 10,c = (0,0,0)):
        self.r = r
        self.c = c
        self.i = 0
    def draw(self):
        if self.i:
            x,y = pygame.mouse.get_pos()
            if(pygame.mouse.get_pressed()[0]): 
                pygame.draw.rect(insurf,self.c,pygame.Rect(self.x,self.y,x-self.x,y-self.y))
                self.i = 0
                pygame.time.Clock().tick(10)
                return 1
            else:
                x,y = pygame.mouse.get_pos() 
                pygame.draw.rect(canvas,self.c,pygame.Rect(self.x,self.y,x-self.x,y-self.y))
                return 0
        else:
            self.x,self.y = pygame.mouse.get_pos()
            self.i  = pygame.mouse.get_pressed()[0] and self.x in range(0,ww) and self.y in range(0,hh)
            if self.i:
                pygame.time.Clock().tick(10)
class Oval:
    def __init__(self,r = 10,c = (0,0,0)):
        self.r = r
        self.c = c
        self.i = 0
    def draw(self):
        if self.i:
            x,y = pygame.mouse.get_pos()
            if(pygame.mouse.get_pressed()[0]):
                if(self.x<x and self.y<y):
                    pygame.draw.ellipse(insurf,self.c,pygame.Rect(self.x,self.y,x-self.x,y-self.y))
                if(self.x<x and self.y>=y):
                    pygame.draw.ellipse(insurf,self.c,pygame.Rect(self.x,y,x-self.x,self.y-y))
                if(self.x>=x and self.y<y):
                    pygame.draw.ellipse(insurf,self.c,pygame.Rect(x,self.y,-x+self.x,y-self.y))
                if(self.x>=x and self.y>=y):
                    pygame.draw.ellipse(insurf,canvas,self.c,pygame.Rect(x,y,-x+self.x,-y+self.y))
                self.i = 0
                pygame.time.Clock().tick(10)
                return 1
            else:
                if(self.x<x and self.y<y):
                    pygame.draw.ellipse(canvas,self.c,pygame.Rect(self.x,self.y,x-self.x,y-self.y))
                if(self.x<x and self.y>=y):
                    pygame.draw.ellipse(canvas,self.c,pygame.Rect(self.x,y,x-self.x,self.y-y))
                if(self.x>=x and self.y<y):
                    pygame.draw.ellipse(canvas,self.c,pygame.Rect(x,self.y,-x+self.x,y-self.y))
                if(self.x>=x and self.y>=y):
                    pygame.draw.ellipse(canvas,self.c,pygame.Rect(x,y,-x+self.x,-y+self.y))
                return 0
        else:
            self.x,self.y = pygame.mouse.get_pos()
            self.i  = pygame.mouse.get_pressed()[0] and self.x in range(0,ww) and self.y in range(0,hh)
            if self.i:
                pygame.time.Clock().tick(10)
class Line:
    def __init__(self,r = 10,c = (0,0,0)):
        self.r = r
        self.c = c
        self.i = 0
    def draw(self):
        if self.i:
            x,y = pygame.mouse.get_pos()
            if(pygame.mouse.get_pressed()[0]):
                pygame.draw.line(insurf,self.c,(x,y),(self.x,self.y),self.r)
                self.i = 0
                pygame.time.Clock().tick(10)
                return 1
            else:
                pygame.draw.line(canvas,self.c,(x,y),(self.x,self.y),self.r)
                return 0
        else:
            self.x,self.y = pygame.mouse.get_pos()
            self.i  = pygame.mouse.get_pressed()[0] and self.x in range(0,ww) and self.y in range(0,hh)
            if self.i:
                pygame.time.Clock().tick(10)
def main():
    global insurf
    mxy = 0
    r = 5
    pen = Button(ww,0,"pen")
    pen.ins = Pen
    line = Button(ww+50,0,"stick")
    line.ins = Line
    rect = Button(ww,50,"rect")
    rect.ins = Rect
    select = pygame.Rect(-100,-100,50,50)
    selectc = pygame.Rect(-100,-100,50,50)
    eraser = Button(ww+50,50,"eraser")
    eraser.ins = Eraser
    oval = Button(ww+50,100,"oval")
    oval.ins = Oval
    red,blue,green,black,white = Color(ww,200,(255,0,0)),Color(ww+50,200,(0,0,255)),Color(ww,250,(0,255,0)),Color(ww+50,250,(0,0,0)),Color(ww,300,(255,255,255))
    s = pygame.Surface((100,hh))
    s.fill((227,226,217))
    inst = Pen()
    pen.n = "circle"
    eraser.n = "rect"
    while(1):
        if pygame.key.get_pressed()[K_UP]:
            r+=1
        elif pygame.key.get_pressed()[K_DOWN] and r>0:
            r-=1
        xy = pygame.mouse.get_pos()
        canvas.blit(s,(ww,0))
        canvas.blit(insurf,(0,0))
        for i in [pen,line,rect,eraser,oval]:
            i.draw()
            if i.get_pressed():
                select.x,select.y = i.r.x,i.r.y
                inst = i.ins()
        for i in [red,blue,green,white,black]:
            i.draw()
            if i.get_pressed() or (selectc.x == i.r.x and selectc.y == i.r.y):
                inst.c = i.c
                selectc.x,selectc.y = i.r.x,i.r.y
        if pygame.key.get_pressed()[K_UP] and inst.r<20:
            inst.r+=1
            pygame.time.Clock().tick(10)
        if pygame.key.get_pressed()[K_DOWN] and inst.r>0:
            inst.r-=1
            pygame.time.Clock().tick(10)
        inst.draw()
        pygame.draw.line(canvas,(0,0,0),(pygame.mouse.get_pos()[0]-5,pygame.mouse.get_pos()[1]),(pygame.mouse.get_pos()[0]+5,pygame.mouse.get_pos()[1]))
        pygame.draw.line(canvas,(0,0,0),(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]-5),(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]+5))
        pygame.draw.rect(canvas,(0,0,0),select,4)
        pygame.draw.rect(canvas,(0,0,0),selectc,4)
        pygame.display.update()
def check():
    while 1:
        x,y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(insurf,'saved.png')
                pygame.quit()
                exit()
t1 = Thread(target = check,name = "t")
t2 = Thread(target = main,name = "s")
t1.start()
t2.start()
t1.run()
t2.run()