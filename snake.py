import pygame,random
from pygame.locals import *
from threading import Thread
import math,json
pygame.init()
ww, hh = 500,500
m = 300
p = 20
fps = 50
gmo = 0
canvas = pygame.display.set_mode((ww+m,hh))
pygame.display.set_caption("Snake")
scores = [0,0]
eaten = [0,0]
file = []
players = []
def dis(x,y,a,b):
    return ((x-a)**2+(y-b)**2)**0.5
def gameover(ll,n = 1):
    s = pygame.Surface((ww,hh),pygame.SRCALPHA,32).convert_alpha()
    cl = pygame.time.Clock()
    for i in range(50):
        s.fill((0,0,0,i))
        canvas.blit(s,(0,0))
        pygame.display.update()
        cl.tick(50)
    font = pygame.font.SysFont("kalam",40)
    s = pygame.Surface((ww+m,hh),pygame.SRCALPHA,32).convert_alpha()
    for i in range(50):
        s.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255),i))
        canvas.blit(s,(0,0))
        pygame.display.update()
        cl.tick(50)
    stp = [max(scores[i]//100,1) for i in range(n)]
    g = [0 for i in range(n)]
    while 1:
        s.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255),50))
        canvas.blit(font.render("GAME OVER",1,(255,255,255)),(ww//2-50,hh//2-20))
        f = pygame.font.SysFont(pygame.font.get_fonts()[0],20)
        canvas.blit(f.render("SCORE {}".format(g[0]),1,(255,255,255)),(ww//2,hh//2+30))
        if(n==2):
            canvas.blit(f.render("SCORE {}".format(g[1]),1,(255,255,255)),(ww//2,hh//2+60))            
        for i in range(len(g)):
            if(scores[i]>g[i]):
                g[i]+=max(1,(scores[i]-g[i])//100)
        canvas.blit(s,(0,0))
        pygame.display.update()
        cl.tick(50)
        button = Button(600,200,"Restart",w=70)
        button.draw(canvas)
        mnu = Button(400,250,"Menu",w = 70)
        mnu.draw(canvas)
        k = pygame.Surface((ww+m,hh),pygame.SRCALPHA).convert_alpha()
        if button.get_pressed():
            for i in range(50):
                s.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255),50))
                k.fill((0,0,0,i))
                #canvas.blit(font.render("GAME OVER",1,(255,255,255)),(ww//2-50,hh//2-20))
                #canvas.blit(f.render("SCORE {}".format(g),1,(255,255,255)),(ww//2,hh//2+30))
                canvas.blit(k,(0,0))
                '''if g<score1:
                    g+=min(stp,score1-g)'''
                cl.tick(50)
                pygame.display.update()
            return main(ll,n)
        if mnu.get_pressed():
            return menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
class Button:
    def __init__(self,x,y,tx,color = (255,0,0),h = 30,w = 50,font = pygame.font.SysFont("kalam",20)):
        self.tx,self.c,self.font = tx,color,font
        self.tc = (255,255,255)
        self.r = pygame.Rect(x,y,w,h)
    def draw(self,canvas):
        pygame.draw.rect(canvas,self.c,self.r)
        canvas.blit(self.font.render(self.tx,1,self.tc),(self.r.x+5,self.r.y))
    def get_pressed(self):
        return pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0] in range(self.r.x,self.r.x+self.r.w) and pygame.mouse.get_pos()[1] in range(self.r.y,self.r.y+self.r.h)
class Snake:
    def __init__(self,x,y,color = [1,255,1],r = 5,sp = 2,keys = [K_UP,K_DOWN,K_RIGHT,K_LEFT],multiplayer = False):
        x = x//sp
        y = y//sp
        print(x//p,y//p)
        while(file[x//p][y//p]):
            x,y = random.randint(0,(ww-1)//sp),random.randint(0,(hh-1)//sp)
        self.elements = [[x*sp,y*sp,color]]
        self.r = r
        self.speed = [0,0]
        self.b = [1,-1,1]
        self.sp = sp
        self.keys = keys
        self.t = 0
        self.ind = int(multiplayer)
        self.alive = 1
    def wcol(self):
        return file[self.elements[0][1]//p][self.elements[0][0]//p]
    def cc(self,cl):
        for i in range(3):
            if(cl[i]==0):
                self.b[i] = 1
            if(cl[i]==255):
                self.b[i] = -1
        return [self.b[i]+cl[i] for i in range(len(cl))]
    def draw(self):
        for element in self.elements:
            pygame.draw.circle(canvas,tuple(element[2]),(element[0],element[1]),self.r)
    def add(self):
        self.elements.insert(0,[self.elements[0][0]+self.speed[0],self.elements[0][1]+self.speed[1],self.cc(self.elements[0][2])])
    def pop(self):
        self.elements.pop(-1)
    def update(self):
        k = pygame.key.get_pressed()
        if k[self.keys[0]] and self.speed!=[0,self.sp]:
            self.speed = [0,-self.sp]
        if k[self.keys[1]] and self.speed!=[0,-self.sp]:
            self.speed = [0,self.sp]
        if k[self.keys[2]] and self.speed!=[-self.sp,0]:
            self.speed = [self.sp,0]
        if k[self.keys[3]] and self.speed!=[self.sp,0]:
            self.speed = [-self.sp,0]
        self.pop()
        global eaten
        self.add()
        if eaten[self.ind]>0:
            self.add()
            eaten[self.ind]-=1
            scores[self.ind]+=1
        if(self.wcol()):
            self.alive = 0
            return
            '''while 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()'''
        if(self.t==self.r*2//self.sp):
            for j in players:
                if(j==self):
                    for i in j.elements[self.r:]:
                        if(i[0] ==self.elements[0][0] and i[1] == self.elements[0][1]):
                            self.alive = 0
                            return
                        '''while 1:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()'''
                else:
                    for i in j.elements:
                        if(i[0] == self.elements[0][0] and i[1] == self.elements[0][1]):
                            self.alive = 0
                            return
        elif(self.speed!=[0,0]):
            self.t+=1
class Stone:
    def __init__(self,rect,color = (0,0,0)):
        self.r = rect
        self.c = color
    def draw(self,canvas):
        pygame.draw.rect(canvas,self.c,self.r)
class Food:
    def __init__(self):
        self.r = random.randint(5,20)
        self.c = [random.randint(100,255) for i in range(3)]
        self.ct = self.c
        #self.el = pygame.Rect(self.x,self.y,0,0)
        self.x,self.y = random.randint(0,ww),random.randint(0,hh)
        while(file[self.y//p][self.x//p]):
            self.x,self.y = random.randint(0,ww),random.randint(0,hh)
        print(self.x,self.y)
    def draw(self):
        pygame.draw.circle(canvas,tuple(self.c),(self.x,self.y),self.r)
    def update(self):
        for i in range(len(players)):
            if(dis(self.x,self.y,players[i].elements[0][0],players[i].elements[0][1])<self.r+players[i].r):
                global eaten
                eaten[i] += self.r
                self.r = random.randint(5,20)
                self.c = [random.randint(50,255) for i in range(3)]
                self.x,self.y = random.randint(0,ww),random.randint(0,hh)
                while(file[(self.y-(self.y==hh))//p][(self.x-(self.x==ww))//p]):
                    self.x,self.y = random.randint(0,ww),random.randint(0,hh)
keyboard = [[K_UP,K_DOWN,K_RIGHT,K_LEFT],[K_w,K_s,K_d,K_a]]
def main(x,n = 1):
    global players,scores
    scores = [0 for i in range(n)]
    scrt = [Button(ww+70,hh//2-100+50*i,"SCORE: "+str(scores[i]),w = 100) for i in range(n)]
    lvlvl = str(x)+str(random.randint(0,1)*(x==1))
    with open("map"+lvlvl+".txt") as f:
        global file
        file = [[j == '1' for j in i] for i in f]
    xy,yx = [random.randint(0,ww) for i in range(n)],[random.randint(0,hh) for i in range(n)]
    if(len(xy)==2):
        while (xy[0]==xy[1] and yx[0]==yx[1]) or (file[yx[0]//p][xy[0]//p] or file[yx[1]//p][xy[1]//p]):
            xy,yx = [random.randint(0,ww) for i in range(n)],[random.randint(0,hh) for i in range(n)]
    else:
        while file[yx[0]//p][xy[0]//p]:
            xy,yx = [random.randint(0,ww) for i in range(n)],[random.randint(0,hh) for i in range(n)]
    players = [Snake(xy[i],yx[i],keys = keyboard[i],multiplayer = i) for i in range(n)]
    #player2 = Snake(300,300,keys = [K_w,K_s,K_d,K_a])
    wall = [Stone(pygame.Rect(j*p,i*p,p,p),color = ((random.randint(100,255),random.randint(100,255),random.randint(100,255)))) for i in range(len(file)) for j in range(len(file[i])) if(file[i][j])]
    f = Food()
    started_time = 60
    tsurf = pygame.Surface([ww,hh],pygame.SRCALPHA,32).convert_alpha()
    tsurf.fill((0,0,0,0))
    clock = pygame.time.Clock()
    pygame.display.update()
    pause = Button(ww+150,hh//2,"Pause",w = 70)
    pause.l = 2
    t = pause.l
    for i in range(20):
        for j in players:
            j.add()
        #player2.add()
    print(pause.l)
    while started_time:
        scrt = [Button(ww+70,hh//2-100+50*i,"SCORE: "+str(scores[i]),w = 100) for i in range(n)]
        if(t!=pause.l):
            print(pause.l)
            t = pause.l
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        canvas.fill((0,0,0))
        for i in wall:
            i.draw(canvas)
        f.draw()
        f.update()
        pause.draw(canvas)
        k = 0
        for i in players:
            i.draw()
            if(i.alive):
                i.update()
        if k:
            gameover(x,n)
        if pause.get_pressed() or pygame.key.get_pressed()[K_p]:
            if pause.l ==2 or pause.l == 3:
                pause.l = 3
            else:
                pause.l = 1
        elif pause.l == 1:
            pause.l = 2
        elif pause.l == 3:
            pause.l = 0
        if(pause.l!=2):
            svb = Button(ww+50,hh//2,"Save",w = 80)
            svb.draw(canvas)
            if(svb.get_pressed()):
                with open("save.json","w") as fl:
                    json.dump({"players":[i.elements for i in players],"food" : [f.x,f.y,f.r,f.c],"lvl":lvlvl,"n":n},fl)
            continue
        tsurf.fill((0,0,0,started_time))
        for i in scrt:
            i.draw(canvas)
        pygame.display.update()
        canvas.blit(tsurf,(0,0))
        clock.tick(fps)
        started_time-=1
    del started_time
    del tsurf
    while 1:
        scrt = [Button(ww+70,hh//2-100+50*i,"SCORE: "+str(scores[i]),w = 100) for i in range(n)]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if pause.get_pressed() or pygame.key.get_pressed()[K_p]:
            if pause.l ==2 or pause.l == 3:
                pause.l = 3
            else:
                pause.l = 1
        elif pause.l == 1:
            pause.l = 2
        elif pause.l == 3:
            pause.l = 0
        if(pause.l!=2):
            svb = Button(ww+50,hh//2-50,"Save",w = 80)
            svb.draw(canvas)
            pygame.display.update()
            if(svb.get_pressed()):
                with open("save.json","w") as fl:
                    json.dump({"players":[i.elements for i in players],"food" : [f.x,f.y,f.r,f.c],"lvl":lvlvl,"n":n},fl)
            continue
        canvas.fill((0,0,0))
        for i in wall:
            i.draw(canvas)
        f.draw()
        f.update()
        k = 0
        for i in players:
            i.draw()
            if(i.alive):
                i.update()
                k+=1
        if k == 0:
            gameover(x,n)
        for i in scrt:
            i.draw(canvas)
        pause.draw(canvas)
        pygame.display.update()
        clock.tick(fps)
def playsav():
    with open("save.json","r") as fl:
        k = json.load(fl)
        name = "map"+k["lvl"]+".txt"
        x,n = k["lvl"][0],k["n"]
        with open(name,"r") as fl:
            global file
            file = [[i=="1" for i in j] for j in fl]
        global players
        lvlvl = k["lvl"]
        players = [Snake(0,0,keys = keyboard[i]) for i in range(len(k["players"]))]
        for i in range(len(players)):
            players[i].elements = k["players"][i]
        f = Food()
        f.x,f.y,f.r,f.c = k["food"]    
    wall = [Stone(pygame.Rect(j*p,i*p,p,p),color = ((random.randint(100,255),random.randint(100,255),random.randint(100,255)))) for i in range(len(file)) for j in range(len(file[i])) if(file[i][j])]
    started_time = 60
    tsurf = pygame.Surface([ww,hh],pygame.SRCALPHA,32).convert_alpha()
    tsurf.fill((0,0,0,0))
    clock = pygame.time.Clock()
    pygame.display.update()
    pause = Button(ww+150,hh//2,"Pause",w = 70)
    pause.l = 2
    t = pause.l
        #player2.add()
    print(pause.l)
    while started_time:
        scrt = [Button(ww+70,hh//2-100+50*i,"SCORE: "+str(scores[i]),w = 100) for i in range(n)]
        if(t!=pause.l):
            print(pause.l)
            t = pause.l
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        canvas.fill((0,0,0))
        for i in wall:
            i.draw(canvas)
        f.draw()
        f.update()
        pause.draw(canvas)
        k = 0
        for i in players:
            i.draw()
            if(i.alive):
                i.update()
        if k:
            gameover(x,n)
        if pause.get_pressed() or pygame.key.get_pressed()[K_p]:
            if pause.l ==2 or pause.l == 3:
                pause.l = 3
            else:
                pause.l = 1
        elif pause.l == 1:
            pause.l = 2
        elif pause.l == 3:
            pause.l = 0
        if(pause.l!=2):
            svb = Button(ww+50,hh//2+60,"Save",w = 80)
            svb.draw(canvas)
            if(svb.get_pressed()):
                with open("save.json","w") as fl:
                    json.dump({"players":[i.elements for i in players],"food" : [f.x,f.y,f.r,f.c],"lvl":lvlvl},fl)
            continue
        tsurf.fill((0,0,0,started_time))
        for i in scrt:
            i.draw(canvas)
        pygame.display.update()
        canvas.blit(tsurf,(0,0))
        clock.tick(fps)
        started_time-=1
    del started_time
    del tsurf
    while 1:
        scrt = [Button(ww+70,hh//2-100+50*i,"SCORE: "+str(scores[i]),w = 100) for i in range(n)]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if pause.get_pressed() or pygame.key.get_pressed()[K_p]:
            if pause.l ==2 or pause.l == 3:
                pause.l = 3
            else:
                pause.l = 1
        elif pause.l == 1:
            pause.l = 2
        elif pause.l == 3:
            pause.l = 0
        if(pause.l!=2):
            svb = Button(ww+50,hh//2-50,"Save",w = 80)
            svb.draw(canvas)
            pygame.display.update()
            if(svb.get_pressed()):
                with open("save.json","w") as fl:
                    json.dump({"players":[i.elements for i in players],"food" : [f.x,f.y,f.r,f.c],"lvl":lvlvl},fl)
            continue
        canvas.fill((0,0,0))
        for i in wall:
            i.draw(canvas)
        f.draw()
        f.update()
        k = 0
        for i in players:
            i.draw()
            if(i.alive):
                i.update()
                k+=1
        if k == 0:
            gameover(x,n)
        for i in scrt:
            i.draw(canvas)
        pause.draw(canvas)
        pygame.display.update()
        clock.tick(fps)
def menu():
    cl = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    gcl = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    canvas.fill(tuple(cl))
    font = pygame.font.SysFont("kalam",40)
    canvas.blit(font.render("Snake",1,(255,255,255)),(ww,0))
    pygame.draw.rect(canvas,(255,0,0),pygame.Rect(ww+20,hh//2,100,40))
    canvas.blit(font.render("Start",1,(255,255,255)),(ww+25,hh//2-5))
    easy = Button(ww+25,hh//2+60,"easy", w = 100)
    middle = Button(ww+25,hh//2+100,"middle",w = 100)
    hard = Button(ww+25,hh//2+140,"hard", w = 100)
    rct = pygame.Rect(-100,-200,100,30)
    rct2  = pygame.Rect(-100,-200,100,30)
    plays = Button(ww-50,hh//2-100,"Play saved game",w = 200)
    single = Button(ww-300,hh//2-50,"Singleplayer",w = 200)
    multi = Button(ww-300,hh//2,"Multiplayer",w = 200)
    n = 1
    c = pygame.time.Clock()
    lvl = 0
    easy.lvl,middle.lvl,hard.lvl = 0,1,2
    single.n = 1
    multi.n = 2
    while 1:
        if cl==gcl:
            gcl = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        for i in range(3):
            if cl[i]<gcl[i]:
                cl[i]+=1
            elif cl[i]>gcl[i]:
                cl[i]-=1
        canvas.fill(tuple(cl))
        font = pygame.font.SysFont("kalam",40)
        canvas.blit(font.render("Snake",1,(255,255,255)),(ww,0))
        pygame.draw.rect(canvas,(255,0,0),pygame.Rect(ww+20,hh//2,100,40))
        canvas.blit(font.render("Start",1,(255,255,255)),(ww+25,hh//2-5))
        easy.draw(canvas)
        middle.draw(canvas)
        hard.draw(canvas)
        plays.draw(canvas)
        single.draw(canvas)
        multi.draw(canvas)
        pygame.draw.rect(canvas,(255,255,255),rct,3)
        pygame.draw.rect(canvas,(255,255,255),rct2,3)
        for i in [easy,middle,hard]:
            if i.get_pressed():
                rct.x = i.r.x
                rct.y = i.r.y
                lvl = i.lvl
        for i in [single,multi]:
            if i.get_pressed():
                rct2.x = i.r.x
                rct2.y = i.r.y
                rct2.w = i.r.w
                rct2.h = i.r.h
                n = i.n
        if plays.get_pressed():
            return playsav()
        if sum(map(lambda x:x.type == pygame.QUIT,pygame.event.get())):
            pygame.quit()
            quit()
        if(pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0] in range(ww+20,ww+120) and pygame.mouse.get_pos()[1] in range(hh//2,hh//2+40)):
            return main(lvl,n)
        c.tick(50)
        pygame.display.update()
menu()
